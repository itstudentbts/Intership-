import sys

try:
    import tensorflow as tf
except ImportError as err:
    print("TensorFlow import failed.")
    print("Full error:", err)
    sys.exit(1)

import numpy as np
import json
import os
import matplotlib.pyplot as plt

# ══════════════════════════════════════════════════════════
# SETTINGS — only change these if needed
# ══════════════════════════════════════════════════════════

TRAIN_DIR    = r"D:\cesi\ai food\Intership-\data\processed\train"
VAL_DIR      = r"D:\cesi\ai food\Intership-\data\processed\val"
TEST_DIR     = r"D:\cesi\ai food\Intership-\data\processed\test"
MODEL_PATH   = r"D:\cesi\ai food\Intership-\models\food_classifier_101.h5"
HISTORY_PATH = r"D:\cesi\ai food\Intership-\models\training_history_101.json"
CLASS_NAMES_PATH = r"D:\cesi\ai food\Intership-\models\class_names.json"
PLOT_PATH    = r"D:\cesi\ai food\Intership-\models\training_plot_101.png"

IMAGE_SIZE  = (224, 224)
BATCH_SIZE  = 32
EPOCHS      = 15           # more epochs for 101 classes
NUM_CLASSES = 101          # ALL food-101 classes
# ══════════════════════════════════════════════════════════


def verify_directories():
    """Check all required folders exist before starting."""
    required = [TRAIN_DIR, VAL_DIR, TEST_DIR,
                os.path.dirname(MODEL_PATH)]
    missing = [p for p in required if not os.path.isdir(p)]
    if missing:
        print("ERROR: Missing directories:")
        for p in missing:
            print(f"  - {p}")
        print("\nRun organise_data_101.py first to set up all 101 classes.")
        sys.exit(1)


def count_classes(directory):
    """Count how many class folders exist."""
    return len([
        d for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ])


# ══════════════════════════════════════════════════════════
# STEP 1 — Load data
# ══════════════════════════════════════════════════════════
def load_data():
    """
    Load all 101 food classes.
    Apply augmentation to training set only.
    """
    print("Setting up data generators...")

    # augmentation — more aggressive for 101 classes
    # helps model generalise across varied photos
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=25,        # rotate up to 25 degrees
        horizontal_flip=True,     # mirror left-right
        zoom_range=0.20,          # zoom in/out 20%
        width_shift_range=0.15,   # shift left/right
        height_shift_range=0.15,  # shift up/down
        shear_range=0.10,         # slight shear distortion
        brightness_range=[0.8, 1.2],  # vary brightness
        fill_mode='nearest'       # fill empty pixels
    )

    # no augmentation for val/test — just normalise
    val_test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255
    )

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )

    val_gen = val_test_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    test_gen = val_test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False   # keep order for evaluation
    )

    print(f"  Train: {train_gen.samples} images, "
          f"{len(train_gen.class_indices)} classes")
    print(f"  Val:   {val_gen.samples} images")
    print(f"  Test:  {test_gen.samples} images")

    return train_gen, val_gen, test_gen


# ══════════════════════════════════════════════════════════
# STEP 2 — Build model
# ══════════════════════════════════════════════════════════
def build_model(num_classes):
    """
    MobileNetV2 base + custom head for num_classes.
    Identical architecture to your 10-class model —
    only the output layer size changes (10 → 101).
    """
    print("Loading MobileNetV2 pretrained weights...")

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False  # freeze all base layers

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.4),         # slightly higher for 101
        tf.keras.layers.Dense(256, activation='relu'),  # bigger for 101
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(num_classes, activation='softmax')
        #                      ^^^
        #                      101 output neurons — one per food class
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
        #                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #                     also track top-5 accuracy
        #                     (is correct class in top 5 guesses?)
    )

    return model, base_model


# ══════════════════════════════════════════════════════════
# STEP 3 — Callbacks
# ══════════════════════════════════════════════════════════
def get_callbacks():
    """Automatic model saving, early stopping, lr reduction."""

    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )

    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=4,              # wait 4 epochs before stopping
        restore_best_weights=True,
        verbose=1
    )

    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=2,
        min_lr=1e-7,
        verbose=1
    )

    # print progress every epoch
    class EpochLogger(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            print(
                f"\nEpoch {epoch+1} complete — "
                f"acc: {logs['accuracy']:.3f} | "
                f"val_acc: {logs['val_accuracy']:.3f} | "
                f"top5: {logs.get('top_k_categorical_accuracy', 0):.3f}"
            )

    return [checkpoint, early_stop, reduce_lr, EpochLogger()]


# ══════════════════════════════════════════════════════════
# STEP 4 — Fine tuning
# ══════════════════════════════════════════════════════════
def fine_tune(model, base_model, train_gen, val_gen):
    """
    Unfreeze last 50 layers of MobileNetV2 and retrain
    with very small learning rate.
    More layers unfrozen than before (30→50) because
    food-specific features need more adaptation.
    """
    print("\nFine tuning — unfreezing last 50 layers...")

    base_model.trainable = True
    # freeze everything except last 50 layers
    for layer in base_model.layers[:-50]:
        layer.trainable = False

    trainable_count = sum(
        1 for l in base_model.layers if l.trainable
    )
    print(f"  Trainable base layers: {trainable_count}")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
    )

    history_fine = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=8,
        callbacks=get_callbacks()
    )

    return history_fine


# ══════════════════════════════════════════════════════════
# STEP 5 — Plot results
# ══════════════════════════════════════════════════════════
def plot_history(history, suffix=""):
    """Save accuracy and loss graphs."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # accuracy
    axes[0].plot(history.history['accuracy'],     label='train')
    axes[0].plot(history.history['val_accuracy'], label='val')
    axes[0].set_title('Top-1 Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].legend()

    # top-5 accuracy
    if 'top_k_categorical_accuracy' in history.history:
        axes[1].plot(history.history['top_k_categorical_accuracy'],
                     label='train top-5')
        axes[1].plot(history.history['val_top_k_categorical_accuracy'],
                     label='val top-5')
        axes[1].set_title('Top-5 Accuracy')
        axes[1].set_xlabel('Epoch')
        axes[1].legend()

    # loss
    axes[2].plot(history.history['loss'],     label='train')
    axes[2].plot(history.history['val_loss'], label='val')
    axes[2].set_title('Loss')
    axes[2].set_xlabel('Epoch')
    axes[2].legend()

    plt.tight_layout()
    save_path = PLOT_PATH.replace('.png', f'{suffix}.png')
    plt.savefig(save_path)
    print(f"Plot saved: {save_path}")
    plt.close()


# ══════════════════════════════════════════════════════════
# STEP 6 — Evaluate
# ══════════════════════════════════════════════════════════
def evaluate(model, test_gen):
    """Final test set evaluation."""
    print("\nEvaluating on test set...")
    results = model.evaluate(test_gen, verbose=1)

    print("\n" + "="*40)
    print(f"Test Loss:          {results[0]:.4f}")
    print(f"Test Accuracy:      {results[1]:.4f} ({results[1]*100:.1f}%)")
    if len(results) > 2:
        print(f"Test Top-5 Acc:     {results[2]:.4f} ({results[2]*100:.1f}%)")
    print("="*40)
    return results


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    print("=" * 55)
    print("  FOOD CALORIE AI — TRAINING ON ALL 101 CLASSES")
    print("=" * 55)

    # check folders exist
    verify_directories()

    # check actual class count
    actual_classes = count_classes(TRAIN_DIR)
    print(f"\nClasses found in train folder: {actual_classes}")

    if actual_classes < 101:
        print(
            f"\nWARNING: Only {actual_classes} classes found.\n"
            "Run organise_data_101.py first to set up all 101 classes."
        )
        if actual_classes < 10:
            sys.exit(1)
        else:
            print(f"Continuing with {actual_classes} classes...")
            global NUM_CLASSES
            NUM_CLASSES = actual_classes

    # ── Step 1: Load data ──────────────────────────────────
    print("\nStep 1: Loading data...")
    train_gen, val_gen, test_gen = load_data()

    # save class names
    class_names = list(train_gen.class_indices.keys())
    with open(CLASS_NAMES_PATH, 'w') as f:
        json.dump(class_names, f)
    print(f"Saved {len(class_names)} class names")

    # ── Step 2: Build model ────────────────────────────────
    print("\nStep 2: Building model...")
    model, base_model = build_model(len(class_names))
    model.summary()

    total     = model.count_params()
    trainable = sum(
        tf.size(w).numpy() for w in model.trainable_weights
    )
    print(f"\nTotal params:     {total:,}")
    print(f"Trainable params: {trainable:,}")
    print(f"Frozen params:    {total - trainable:,}")

    # ── Step 3: Phase 1 training ───────────────────────────
    print("\nStep 3: Phase 1 training (frozen MobileNetV2)...")
    print("This will take 2-8 hours on CPU.")
    print("Consider using Google Colab for GPU speed.\n")

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=get_callbacks()
    )

    # save phase 1 history
    with open(HISTORY_PATH, 'w') as f:
        # convert float32 to regular float for JSON
        h = {k: [float(v) for v in vals]
             for k, vals in history.history.items()}
        json.dump(h, f)
    plot_history(history, suffix="_phase1")

    # ── Step 4: Fine tuning ────────────────────────────────
    print("\nStep 4: Fine tuning (unfreezing last 50 layers)...")
    fine_tune(model, base_model, train_gen, val_gen)

    # ── Step 5: Evaluate ───────────────────────────────────
    print("\nStep 5: Final evaluation...")
    evaluate(model, test_gen)

    # ── Step 6: Save ───────────────────────────────────────
    print("\nStep 6: Saving final model...")
    model.save(MODEL_PATH)
    print(f"Model saved: {MODEL_PATH}")
    print(f"Class names: {CLASS_NAMES_PATH}")

    print("\n" + "=" * 55)
    print("  TRAINING COMPLETE!")
    print("=" * 55)


if __name__ == "__main__":
    main()
