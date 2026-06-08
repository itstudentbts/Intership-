import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
from PIL import Image

# paths
MODEL_PATH      = r"D:\cesi\ai food\Intership-\models\food_classifier.h5"
CLASS_NAMES_PATH= r"D:\cesi\ai food\Intership-\models\class_names.json"
DATABASE_PATH   = r"D:\cesi\ai food\Intership-\database\calories.csv"

# load model and data once
print("Loading model...")
model      = tf.keras.models.load_model(MODEL_PATH)
class_names= json.load(open(CLASS_NAMES_PATH))
cal_df     = pd.read_csv(DATABASE_PATH)
print("Model ready!")

def predict_food(image_path, portion_grams=100):
    """
    Takes an image path, returns food name,
    confidence, and nutrition info.
    """
    # load and preprocess image
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    # get prediction
    predictions = model.predict(arr, verbose=0)
    probabilities = predictions[0]

    # get top 3 predictions
    top3_idx = np.argsort(probabilities)[::-1][:3]
    top3 = [
        {
            'food': class_names[i],
            'confidence': float(probabilities[i])
        }
        for i in top3_idx
    ]

    # get best prediction
    best_idx  = top3_idx[0]
    food_name = class_names[best_idx]
    confidence= float(probabilities[best_idx])

    # look up nutrition from database
    row = cal_df[cal_df['food_name'] == food_name]

    if len(row) == 0:
        nutrition = {'error': 'Food not found in database'}
    else:
        row = row.iloc[0]
        factor = portion_grams / 100

        nutrition = {
            'food_name':   food_name,
            'portion_g':   portion_grams,
            'calories':    round(row['calories_per_100g'] * factor),
            'protein_g':   round(row['protein_g'] * factor, 1),
            'carbs_g':     round(row['carbs_g'] * factor, 1),
            'fat_g':       round(row['fat_g'] * factor, 1),
        }

    return {
        'prediction':  food_name,
        'confidence':  confidence,
        'top3':        top3,
        'nutrition':   nutrition
    }


# test it
if __name__ == "__main__":
    # test with a sample image
    test_image = r"D:\cesi\ai food\Intership-\data\processed\test\pizza\1001116.jpg"

    if os.path.exists(test_image):
        result = predict_food(test_image, portion_grams=150)
        print(f"\nPrediction:  {result['prediction']}")
        print(f"Confidence:  {result['confidence']:.1%}")
        print(f"\nTop 3 guesses:")
        for i, p in enumerate(result['top3']):
            print(f"  {i+1}. {p['food']}: {p['confidence']:.1%}")
        print(f"\nNutrition (150g portion):")
        n = result['nutrition']
        print(f"  Calories: {n['calories']} kcal")
        print(f"  Protein:  {n['protein_g']}g")
        print(f"  Carbs:    {n['carbs_g']}g")
        print(f"  Fat:      {n['fat_g']}g")
    else:
        print("Test image not found — update test_image path")