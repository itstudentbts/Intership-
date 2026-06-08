import sys

try:
    import tensorflow as tf
except ImportError as err:
    print("TensorFlow import failed. Check your Python environment and native dependencies.")
    print(" - On Windows, install the Microsoft Visual C++ Redistributable.")
    print(" - Make sure your TensorFlow version matches your Python version.")
    print(" - In Anaconda, a fresh environment with tensorflow and openssl often fixes this.")
    print("Full error:", err)
    sys.exit(1)

import numpy as np
import json
import os
import matplotlib.pyplot as plt

# ── settings ──────────────────────────────────────────────
TRAIN_DIR    = r"D:\cesi\ai food\Intership-\data\processed\train"
VAL_DIR      = r"D:\cesi\ai food\Intership-\data\processed\val"
TEST_DIR     = r"D:\cesi\ai food\Intership-\data\processed\test"
MODEL_PATH   = r"D:\cesi\ai food\Intership-\models\food_classifier.h5"
HISTORY_PATH = r"D:\cesi\ai food\Intership-\models\training_history.json"

IMAGE_SIZE  = (224, 224)   # MobileNetV2 expects 224x224
BATCH_SIZE  = 32           # how many images to process at once
EPOCHS      = 10           # how many times to go through all data
NUM_CLASSES = 10           # we have 10 food classes
# ──────────────────────────────────────────────────────────


def verify_directories():
    required = [TRAIN_DIR, VAL_DIR, TEST_DIR, os.path.dirname(MODEL_PATH)]
    missing = [path for path in required if not os.path.isdir(path)]
    if missing:
        print("ERROR: Required directories are missing:")
        for path in missing:
            print(" -", path)
        sys.exit(1)


# ── STEP 1: Load and prepare images ───────────────────────
def load_data():
    """
    Load images from folders.
    Resize to 224x224 and normalize pixel values 0-1.
    Apply augmentation to training data only.
    """

    # augmentation for training — makes model more robust
    # by showing slightly different versions of each image
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,          # normalize: 0-255 → 0-1
        rotation_range=20,       # randomly rotate up to 20 degrees
        horizontal_flip=True,    # randomly flip left-right
        zoom_range=0.15,         # randomly zoom in/out
        width_shift_range=0.1,   # randomly shift left/right
        height_shift_range=0.1   # randomly shift up/down
    )

    # no augmentation for val/test — just normalize
    val_test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255
    )

    # load training images from folders
    # class name = folder name automatically
    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMAGE_SIZE,   # resize all images to 224x224
        batch_size=BATCH_SIZE,
        class_mode='categorical'  # multiple classes (not binary)
    )

    # load validation images
    val_gen = val_test_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    # load test images
    # shuffle=False so results stay in order for evaluation
    test_gen = val_test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    return train_gen, val_gen, test_gen


# ── STEP 2: Build the model ───────────────────────────────
def build_model(num_classes):
    """
    Build transfer learning model using MobileNetV2.

    Structure:
    MobileNetV2 (frozen) → GlobalAveragePooling → Dropout → Dense output
    """

    # load MobileNetV2 pretrained on ImageNet
    # include_top=False means we remove Google's original
    # classification head (1000 classes) and add our own
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),  # 224x224 RGB image
        include_top=False,           # remove original top layer
        weights='imagenet'           # use pretrained weights
    )

    # freeze all layers in base model
    # frozen = weights don't change during training
    # we keep Google's learned knowledge intact
    base_model.trainable = False

    # build our custom model on top
    model = tf.keras.Sequential([

        # 1. the pretrained base — extracts features from images
        base_model,

        # 2. global average pooling
        # converts 3D feature maps → 1D vector
        # like summarising what the model found
        tf.keras.layers.GlobalAveragePooling2D(),

        # 3. batch normalisation
        # keeps values stable during training
        tf.keras.layers.BatchNormalization(),

        # 4. dropout — randomly turns off 30% of neurons
        # prevents overfitting (memorising instead of learning)
        tf.keras.layers.Dropout(0.3),

        # 5. dense hidden layer — 128 neurons
        # learns combinations of features
        tf.keras.layers.Dense(128, activation='relu'),

        # 6. another dropout
        tf.keras.layers.Dropout(0.2),

        # 7. output layer — one neuron per food class
        # softmax converts to probabilities that add up to 1.0
        # e.g. pizza=0.91, sushi=0.05, hamburger=0.04
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    # compile — set how model learns
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',  # loss for multi-class
        metrics=['accuracy']
    )

    return model, base_model


# ── STEP 3: Set up callbacks ──────────────────────────────
def get_callbacks():
    """
    Callbacks watch training and take actions automatically.
    """

    # save the best model automatically
    # only saves when val_accuracy improves
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor='val_accuracy',   # watch validation accuracy
        save_best_only=True,      # only save if it improved
        verbose=1                 # print when it saves
    )

    # stop training early if model stops improving
    # patience=3 means stop after 3 epochs with no improvement
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=3,
        restore_best_weights=True,  # go back to best version
        verbose=1
    )

    # reduce learning rate when stuck
    # if no improvement for 2 epochs, divide lr by 10
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.1,       # multiply lr by this
        patience=2,
        verbose=1
    )

    return [checkpoint, early_stop, reduce_lr]


# ── STEP 4: Fine tuning ───────────────────────────────────
def fine_tune(model, base_model, train_gen, val_gen):
    """
    Phase 2 of training.
    Unfreeze last 30 layers of MobileNetV2 and retrain
    with a very small learning rate.
    This improves accuracy significantly.
    """
    print("\nStarting fine tuning...")

    # unfreeze the last 30 layers
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    # recompile with much smaller learning rate
    # small lr prevents destroying pretrained weights
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # train for 5 more epochs
    history_fine = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=5,
        callbacks=get_callbacks()
    )

    return history_fine


# ── STEP 5: Plot results ──────────────────────────────────
def plot_history(history):
    """
    Draw graphs showing training progress.
    Saves to models folder.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # accuracy graph
    ax1.plot(history.history['accuracy'], label='train accuracy')
    ax1.plot(history.history['val_accuracy'], label='val accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()

    # loss graph
    ax2.plot(history.history['loss'], label='train loss')
    ax2.plot(history.history['val_loss'], label='val loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(r"D:\cesi\ai food\Intership-\models\training_plot.png")
    print("Training plot saved")


# ── STEP 6: Evaluate on test set ─────────────────────────
def evaluate(model, test_gen):
    """
    Final evaluation on test data.
    This is the true performance measure.
    """
    print("\nEvaluating on test set...")
    loss, accuracy = model.evaluate(test_gen)
    print(f"Test Loss:     {loss:.4f}")
    print(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    return accuracy


# ── MAIN — runs everything in order ──────────────────────
def main():

    print("="*50)
    print("FOOD CALORIE AI — MODEL TRAINING")
    print("="*50)

    # 1. load data
    print("\nStep 1: Loading data...")
    verify_directories()
    train_gen, val_gen, test_gen = load_data()

    # save class names for use in prediction later
    class_names = list(train_gen.class_indices.keys())
    print(f"Classes found: {class_names}")

    # 2. build model
    print("\nStep 2: Building model...")
    model, base_model = build_model(NUM_CLASSES)
    model.summary()

    # 3. phase 1 training — frozen base
    print("\nStep 3: Training (Phase 1 — frozen base)...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=get_callbacks()
    )

    # 4. phase 2 — fine tuning
    print("\nStep 4: Fine tuning (Phase 2)...")
    fine_tune(model, base_model, train_gen, val_gen)

    # 5. evaluate on test set
    print("\nStep 5: Evaluating...")
    evaluate(model, test_gen)

    # 6. save training history
    print("\nStep 6: Saving history...")
    with open(HISTORY_PATH, 'w') as f:
        json.dump(history.history, f)
    print("History saved")

    # 7. plot graphs
    print("\nStep 7: Plotting results...")
    plot_history(history)

    # 8. save class names
    class_names_path = r"D:\cesi\ai food\Intership-\models\class_names.json"
    with open(class_names_path, 'w') as f:
        json.dump(class_names, f)
    print(f"Class names saved: {class_names}")

    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)


if __name__ == "__main__":
    main()