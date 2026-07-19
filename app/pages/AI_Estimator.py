"""
FEEDAI - AI Analyzer Page
Upload food → Get instant nutrition info powered by your model
"""

import streamlit as st
import os
import base64
import tempfile
import numpy as np
import pandas as pd
import json
from PIL import Image
import tensorflow as tf

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="FEEDAI - AI Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== PATHS ======================
MODEL_PATH       = r"D:\cesi\ai food\Intership-\models\food_classifier.h5"
CLASS_NAMES_PATH = r"D:\cesi\ai food\Intership-\models\class_names.json"
DATABASE_PATH    = r"D:\cesi\ai food\Intership-\database\calories.csv"

# ====================== LOAD MODEL (cached) ======================
@st.cache_resource(show_spinner="Loading AI model...")
def load_ai_assets():
    model = tf.keras.models.load_model(MODEL_PATH)
    class_names = json.load(open(CLASS_NAMES_PATH))
    cal_df = pd.read_csv(DATABASE_PATH)
    return model, class_names, cal_df

try:
    model, class_names, cal_df = load_ai_assets()
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    MODEL_ERROR = str(e)

# ====================== PREDICTION FUNCTION ======================
def predict_food(image_file, portion_grams=100):
    """Takes an uploaded image, returns prediction + nutrition."""
    img = Image.open(image_file).convert('RGB')
    img_resized = img.resize((224, 224))
    arr = np.array(img_resized) / 255.0
    arr = np.expand_dims(arr, axis=0)

    predictions = model.predict(arr, verbose=0)
    probabilities = predictions[0]

    top3_idx = np.argsort(probabilities)[::-1][:3]
    top3 = [
        {'food': class_names[i], 'confidence': float(probabilities[i])}
        for i in top3_idx
    ]

    best_idx = top3_idx[0]
    food_name = class_names[best_idx]
    confidence = float(probabilities[best_idx])

    row = cal_df[cal_df['food_name'] == food_name]
    if len(row) == 0:
        nutrition = {'error': 'Food not found in database'}
    else:
        row = row.iloc[0]
        factor = portion_grams / 100
        nutrition = {
            'food_name': food_name,
            'portion_g': portion_grams,
            'calories':  round(row['calories_per_100g'] * factor),
            'protein_g': round(row['protein_g'] * factor, 1),
            'carbs_g':   round(row['carbs_g'] * factor, 1),
            'fat_g':     round(row['fat_g'] * factor, 1),
        }

    return {
        'prediction': food_name,
        'confidence': confidence,
        'top3': top3,
        'nutrition': nutrition,
        'image': img,
    }

# ====================== LOAD LOGO ======================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def find_asset(filename):
    paths = [
        f"assets/{filename}", f"assetss/{filename}", f"./assets/{filename}",
        os.path.join(os.path.dirname(__file__), "assets", filename),
        os.path.join(os.path.dirname(__file__), "assetss", filename),
        os.path.join(os.path.dirname(__file__), "..", "assets", filename),
        os.path.join(os.path.dirname(__file__), "..", "assetss", filename),
    ]
    for p in paths:
        result = get_base64_image(p)
        if result:
            return result
    return None

logo_base64 = find_asset("logo.png")
logo_html = (
    f'<img src="data:image/png;base64,{logo_base64}" style="height:60px;width:auto;display:block;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.4));" alt="FEEDAI Logo"/>'
    if logo_base64
    else '<div style="font-family:Syne,sans-serif;font-size:1.6rem;font-weight:800;color:white;">🍽️ FEEDAI</div>'
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0d7a3f 0%, #044d2a 50%, #022818 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* ====== TOP NAVBAR (replaces sidebar) ====== */
    .top-navbar {
        position: sticky;
        top: 0;
        z-index: 100;
        background: rgba(2, 40, 24, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255,255,255,0.12);
        padding: 1rem 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .nav-tagline {
        color: #A7F3D0;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        padding-left: 0.7rem;
        border-left: 1.5px solid rgba(167,243,208,0.4);
        margin-left: 0.3rem;
    }
    
    .nav-links {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    
    .nav-link {
        color: rgba(255,255,255,0.85);
        text-decoration: none;
        font-size: 0.92rem;
        font-weight: 500;
        padding: 0.55rem 1.1rem;
        border-radius: 50px;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .nav-link:hover {
        background: rgba(255,255,255,0.10);
        color: white;
    }
    
    .nav-link.active {
        background: rgba(16,185,129,0.25);
        color: white;
        border: 1px solid rgba(167,243,208,0.4);
    }
    
    .nav-link.cta {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(16,185,129,0.35);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .nav-link.cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16,185,129,0.5);
    }
    
    /* ====== PAGE CONTAINER ====== */
    .analyzer-container {
        max-width: 1200px;
        margin: 2.5rem auto 4rem auto;
        padding: 0 2rem;
        position: relative;
        z-index: 5;
    }
    
    /* Wave bg decoration */
    .wave-bg {
        position: fixed;
        top: 0;
        right: 0;
        width: 50%;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.3;
    }
    .wave-bg svg { width: 100%; height: 100%; }
    
    /* ====== PAGE HEADER ====== */
    .page-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .page-eyebrow {
        color: #A7F3D0;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    
    .page-title {
        font-family: 'Syne', sans-serif;
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0 0 0.6rem 0;
        text-shadow: 0 4px 25px rgba(0,0,0,0.4);
        letter-spacing: 0.5px;
    }
    
    .page-subtitle {
        color: #ECFDF5;
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0 auto;
        max-width: 620px;
        opacity: 0.92;
        line-height: 1.6;
    }
    
    /* ====== GLASS CARDS ====== */
    .glass-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1.5px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 20px 50px rgba(0,0,0,0.25),
            inset 0 1px 0 rgba(255,255,255,0.15);
        transition: all 0.4s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(255,255,255,0.28);
    }
    
    .card-title {
        color: white;
        font-family: 'Syne', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 1.2rem 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding-bottom: 0.8rem;
        border-bottom: 1.5px solid rgba(255,255,255,0.12);
    }
    
    /* ====== STREAMLIT INPUTS - glass style ====== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.10) !important;
        backdrop-filter: blur(10px) !important;
        border: 1.5px solid rgba(255,255,255,0.20) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: rgba(167,243,208,0.7) !important;
        box-shadow: 0 0 0 3px rgba(167,243,208,0.2) !important;
    }
    
    /* ====== SLIDER ====== */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #10B981 0%, #A7F3D0 100%) !important;
    }
    
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: white !important;
        border: 3px solid #10B981 !important;
        box-shadow: 0 4px 12px rgba(16,185,129,0.4) !important;
    }
    
    /* ====== FILE UPLOADER - glass style ====== */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.05);
        border: 2px dashed rgba(167,243,208,0.4);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(255,255,255,0.10);
        border-color: rgba(167,243,208,0.7);
    }
    
    [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
        padding: 1rem !important;
    }
    
    [data-testid="stFileUploader"] section > div {
        color: white !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.55rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 18px rgba(16,185,129,0.4) !important;
        transition: all 0.3s !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 9px 25px rgba(16,185,129,0.55) !important;
    }
    
    /* Uploaded file label color */
    [data-testid="stFileUploader"] small {
        color: rgba(255,255,255,0.7) !important;
    }
    
    /* ====== PRIMARY BUTTONS ====== */
    div.stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border: 1.5px solid rgba(255,255,255,0.25) !important;
        padding: 0.85rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
        border-radius: 50px !important;
        box-shadow: 0 10px 25px rgba(16,185,129,0.4) !important;
        transition: all 0.35s ease !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 14px 35px rgba(16,185,129,0.55) !important;
    }
    
    /* ====== RESULT - PREDICTION BADGE ====== */
    .prediction-badge {
        text-align: center;
        padding: 2rem 1.5rem;
        background: linear-gradient(135deg, rgba(16,185,129,0.25) 0%, rgba(5,150,105,0.15) 100%);
        border: 1.5px solid rgba(167,243,208,0.4);
        border-radius: 20px;
        margin-bottom: 1.5rem;
    }
    
    .prediction-label {
        color: #A7F3D0;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .prediction-name {
        color: white;
        font-family: 'Syne', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        text-transform: capitalize;
        margin: 0 0 0.6rem 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .prediction-conf {
        color: white;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .prediction-conf .conf-value {
        color: #A7F3D0;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    /* ====== NUTRITION GRID ====== */
    .nutrition-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .nutri-card {
        background: rgba(255,255,255,0.10);
        backdrop-filter: blur(10px);
        border: 1.5px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 1.3rem 0.8rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .nutri-card:hover {
        transform: translateY(-4px);
        background: rgba(255,255,255,0.15);
        border-color: rgba(167,243,208,0.5);
    }
    
    .nutri-icon {
        font-size: 1.7rem;
        margin-bottom: 0.4rem;
    }
    
    .nutri-value {
        color: white;
        font-family: 'Syne', sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.3rem 0;
    }
    
    .nutri-unit {
        color: #A7F3D0;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    
    .nutri-label {
        color: rgba(255,255,255,0.85);
        font-size: 0.88rem;
        font-weight: 500;
        margin-top: 0.3rem;
    }
    
    /* ====== TOP 3 GUESSES ====== */
    .top-guess {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.85rem 1.2rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        margin-bottom: 0.6rem;
        transition: all 0.3s ease;
    }
    
    .top-guess:hover {
        background: rgba(255,255,255,0.12);
        border-color: rgba(167,243,208,0.4);
    }
    
    .top-guess-left {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .guess-rank {
        background: rgba(16,185,129,0.3);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid rgba(167,243,208,0.5);
    }
    
    .guess-name {
        color: white;
        font-weight: 500;
        text-transform: capitalize;
        font-size: 0.98rem;
    }
    
    .guess-conf {
        color: #A7F3D0;
        font-weight: 700;
        font-family: 'Syne', sans-serif;
    }
    
    /* Confidence bar mini */
    .conf-bar-bg {
        width: 100px;
        height: 6px;
        background: rgba(255,255,255,0.15);
        border-radius: 10px;
        overflow: hidden;
        margin-right: 0.8rem;
    }
    
    .conf-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #10B981, #A7F3D0);
        border-radius: 10px;
    }
    
    /* ====== INFO HINT BOX ====== */
    .info-hint {
        background: rgba(167,243,208,0.10);
        border: 1px solid rgba(167,243,208,0.25);
        border-left: 3px solid #A7F3D0;
        padding: 0.85rem 1.2rem;
        border-radius: 12px;
        color: #ECFDF5;
        font-size: 0.92rem;
        margin-top: 1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    
    /* ====== HOW IT WORKS ====== */
    .how-it-works {
        margin-top: 3rem;
    }
    
    .hiw-title {
        font-family: 'Syne', sans-serif;
        color: white;
        font-size: 1.6rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .hiw-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.2rem;
    }
    
    .hiw-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 1.8rem 1.4rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .hiw-card:hover {
        transform: translateY(-5px);
        border-color: rgba(167,243,208,0.4);
    }
    
    .hiw-icon {
        font-size: 2.2rem;
        margin-bottom: 0.7rem;
    }
    
    .hiw-card-title {
        color: white;
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
    }
    
    .hiw-card-desc {
        color: rgba(255,255,255,0.8);
        font-size: 0.88rem;
        line-height: 1.5;
    }
    
    /* Image preview */
    [data-testid="stImage"] img {
        border-radius: 18px !important;
        border: 1.5px solid rgba(255,255,255,0.2) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    }
    
    /* Streamlit success/error/info boxes */
    .stAlert {
        background: rgba(255,255,255,0.10) !important;
        backdrop-filter: blur(10px) !important;
        border: 1.5px solid rgba(255,255,255,0.2) !important;
        border-radius: 14px !important;
        color: white !important;
    }
    
    /* RESPONSIVE */
    @media (max-width: 900px) {
        .top-navbar { padding: 0.8rem 1.2rem; flex-wrap: wrap; gap: 0.8rem; }
        .nav-tagline { display: none; }
        .nav-link { padding: 0.45rem 0.8rem; font-size: 0.85rem; }
        .analyzer-container { padding: 0 1rem; }
        .page-title { font-size: 1.9rem; }
        .nutrition-grid { grid-template-columns: repeat(2, 1fr); }
        .hiw-grid { grid-template-columns: 1fr; }
        .prediction-name { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ====================== WAVE BG ======================
st.markdown("""
<div class="wave-bg">
    <svg viewBox="0 0 800 800" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
        <g fill="none" stroke="#10B981" stroke-width="1.5" opacity="0.55">
            <path d="M -50,400 Q 200,150 400,400 T 850,400" />
            <path d="M -50,400 Q 200,180 400,400 T 850,400" transform="translate(0,25)" />
            <path d="M -50,400 Q 200,210 400,400 T 850,400" transform="translate(0,50)" />
            <path d="M -50,400 Q 200,240 400,400 T 850,400" transform="translate(0,75)" />
            <path d="M -50,400 Q 200,120 400,400 T 850,400" transform="translate(0,-25)" />
            <path d="M -50,400 Q 200,90 400,400 T 850,400" transform="translate(0,-50)" />
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# ====================== TOP NAVBAR ======================
st.markdown(f"""
<div class="top-navbar">
    <div class="nav-left">
        {logo_html}
        <span class="nav-tagline">AI CALORIES</span>
    </div>
    <div class="nav-links">
        <a href="/" class="nav-link" target="_self">🏠 Home</a>
        <a href="/AI_Analyzer" class="nav-link active" target="_self">🔬 AI Analyzer</a>
        <a href="/Recommendations" class="nav-link" target="_self">⭐ Recommendations</a>
        <a href="/Sign_In" class="nav-link" target="_self">🔐 Sign In</a>
        <a href="/Sign_Up" class="nav-link cta" target="_self">Sign Up</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== PAGE HEADER ======================
st.markdown("""
<div class="analyzer-container">
    <div class="page-header">
        <div class="page-eyebrow">🤖 Powered by MobileNetV2 · 92.4% Accuracy</div>
        <h1 class="page-title">AI Food Analyzer</h1>
        <p class="page-subtitle">
            Upload a photo of any meal and let our AI instantly identify the dish, 
            estimate the portion, and break down the nutrition.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== MODEL STATUS CHECK ======================
if not MODEL_LOADED:
    st.markdown(f"""
    <div class="analyzer-container">
        <div class="glass-card">
            <h3 class="card-title">⚠️ Model Not Loaded</h3>
            <p style="color:white;">Could not load the AI model. Please check the paths.</p>
            <p style="color:#FCA5A5;font-family:monospace;font-size:0.85rem;">{MODEL_ERROR}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ====================== MAIN LAYOUT (2 columns) ======================
_, main_col, _ = st.columns([1, 10, 1])

with main_col:
    # Top: Upload & Settings (2 columns)
    left, right = st.columns([1.2, 1])
    
    # ----- UPLOAD CARD -----
    with left:
        st.markdown("""
        <div class="glass-card">
            <h3 class="card-title">📸 Upload Your Meal</h3>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a food photo",
            type=["jpg", "jpeg", "png", "webp", "jfif"],
            label_visibility="collapsed",
            key="food_uploader"
        )
        
        st.markdown("""
            <div class="info-hint">
                <span>💡</span>
                <span>Supports JPG, PNG, WEBP, JFIF — up to 200MB</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ----- SETTINGS CARD -----
    with right:
        st.markdown("""
        <div class="glass-card">
            <h3 class="card-title">⚙️ Portion Settings</h3>
        """, unsafe_allow_html=True)
        
        portion = st.slider(
            "Portion size (grams)",
            min_value=50,
            max_value=500,
            value=150,
            step=10,
            key="portion_slider"
        )
        
        st.markdown(f"""
            <div style="text-align:center;padding:1rem;background:rgba(167,243,208,0.10);
                        border-radius:14px;margin-top:0.5rem;">
                <div style="color:#A7F3D0;font-size:0.8rem;font-weight:600;letter-spacing:2px;">CURRENT PORTION</div>
                <div style="color:white;font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;">
                    {portion}<span style="font-size:1.2rem;color:#A7F3D0;margin-left:5px;">g</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ====================== ANALYZE & RESULTS ======================
    if uploaded_file is not None:
        # Show preview + analyze button
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='card-title'>🖼️ Your Uploaded Meal</h3>", unsafe_allow_html=True)
        
        prev_col1, prev_col2 = st.columns([1, 1])
        with prev_col1:
            st.image(uploaded_file, use_container_width=True)
        with prev_col2:
            st.markdown("""
            <div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:1rem;">
                <h4 style="color:white;font-family:'Syne',sans-serif;font-size:1.4rem;margin-bottom:1rem;">
                    Ready to Analyze?
                </h4>
                <p style="color:#ECFDF5;line-height:1.6;margin-bottom:1.5rem;">
                    Our AI will identify the dish, show its top 3 best guesses, and calculate 
                    the full nutrition breakdown for your chosen portion size.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            analyze_clicked = st.button("🔬 Analyze My Meal", key="analyze_btn")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Run prediction
        if analyze_clicked:
            with st.spinner("🧠 AI is analyzing your meal..."):
                try:
                    # Reset file pointer
                    uploaded_file.seek(0)
                    result = predict_food(uploaded_file, portion_grams=portion)
                    st.session_state.last_result = result
                except Exception as e:
                    st.error(f"❌ Prediction failed: {e}")
                    st.session_state.last_result = None
        
        # Display result
        if st.session_state.get("last_result"):
            result = st.session_state.last_result
            
            # MAIN PREDICTION
            food_display = result['prediction'].replace('_', ' ').title()
            conf_pct = result['confidence'] * 100
            
            st.markdown(f"""
            <div class="glass-card">
                <div class="prediction-badge">
                    <div class="prediction-label">✨ AI Prediction</div>
                    <h2 class="prediction-name">{food_display}</h2>
                    <p class="prediction-conf">
                        Confidence: <span class="conf-value">{conf_pct:.1f}%</span>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # NUTRITION GRID
            nutri = result['nutrition']
            if 'error' not in nutri:
                st.markdown(f"""
                <h3 class="card-title" style="border:none;padding:0;margin-top:1rem;">
                    🥗 Nutrition Breakdown <span style="color:#A7F3D0;font-size:0.85rem;font-weight:500;margin-left:0.5rem;">({nutri['portion_g']}g portion)</span>
                </h3>
                <div class="nutrition-grid">
                    <div class="nutri-card">
                        <div class="nutri-icon">🔥</div>
                        <div class="nutri-value">{nutri['calories']}</div>
                        <div class="nutri-unit">KCAL</div>
                        <div class="nutri-label">Calories</div>
                    </div>
                    <div class="nutri-card">
                        <div class="nutri-icon">💪</div>
                        <div class="nutri-value">{nutri['protein_g']}</div>
                        <div class="nutri-unit">GRAMS</div>
                        <div class="nutri-label">Protein</div>
                    </div>
                    <div class="nutri-card">
                        <div class="nutri-icon">🌾</div>
                        <div class="nutri-value">{nutri['carbs_g']}</div>
                        <div class="nutri-unit">GRAMS</div>
                        <div class="nutri-label">Carbs</div>
                    </div>
                    <div class="nutri-card">
                        <div class="nutri-icon">🥑</div>
                        <div class="nutri-value">{nutri['fat_g']}</div>
                        <div class="nutri-unit">GRAMS</div>
                        <div class="nutri-label">Fat</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-hint" style="background:rgba(252,165,165,0.1);border-color:rgba(252,165,165,0.3);border-left-color:#FCA5A5;">
                    <span>⚠️</span>
                    <span>{nutri['error']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # TOP 3 GUESSES
            st.markdown("""
            <div class="glass-card">
                <h3 class="card-title">🎯 Top 3 AI Guesses</h3>
            """, unsafe_allow_html=True)
            
            for i, guess in enumerate(result['top3']):
                guess_name = guess['food'].replace('_', ' ').title()
                guess_pct = guess['confidence'] * 100
                st.markdown(f"""
                <div class="top-guess">
                    <div class="top-guess-left">
                        <div class="guess-rank">{i+1}</div>
                        <div class="guess-name">{guess_name}</div>
                    </div>
                    <div style="display:flex;align-items:center;">
                        <div class="conf-bar-bg">
                            <div class="conf-bar-fill" style="width:{guess_pct}%;"></div>
                        </div>
                        <div class="guess-conf">{guess_pct:.1f}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # No image yet — show drop placeholder card
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:3rem 2rem;">
            <div style="font-size:4rem;margin-bottom:1rem;">🍱</div>
            <h3 style="color:white;font-family:'Syne',sans-serif;font-size:1.5rem;margin-bottom:0.5rem;">
                Drop your food photo here
            </h3>
            <p style="color:rgba(255,255,255,0.7);margin:0;">
                Upload a meal photo above to get started with AI nutrition analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ====================== HOW IT WORKS ======================
    st.markdown("""
    <div class="how-it-works">
        <h3 class="hiw-title">How It Works</h3>
        <div class="hiw-grid">
            <div class="hiw-card">
                <div class="hiw-icon">📸</div>
                <h4 class="hiw-card-title">1. Snap It</h4>
                <p class="hiw-card-desc">Take or upload a photo of your meal — any angle, any lighting.</p>
            </div>
            <div class="hiw-card">
                <div class="hiw-icon">🧠</div>
                <h4 class="hiw-card-title">2. AI Reads It</h4>
                <p class="hiw-card-desc">Our MobileNetV2 model identifies the dish with 92.4% accuracy.</p>
            </div>
            <div class="hiw-card">
                <div class="hiw-icon">📊</div>
                <h4 class="hiw-card-title">3. Track It</h4>
                <p class="hiw-card-desc">Get calories + macros breakdown and log your daily meals.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)