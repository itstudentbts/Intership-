"""
FEEDAI - AI Calorie Estimator
Exact Match to Design (Second Picture)
"""

import streamlit as st
import os
import sys
import time
import base64
from pathlib import Path

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="FEEDAI - AI Calories",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== LOAD LOGO ======================
def get_base64_image(image_path):
    """Convert local image to base64 for embedding in HTML/CSS"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Try multiple possible logo paths
logo_paths = [
    "assets/logo.png",
    "assetss/logo.png",  # in case of typo in your folder
    "./assets/logo.png",
    os.path.join(os.path.dirname(__file__), "assets", "logo.png"),
    os.path.join(os.path.dirname(__file__), "assetss", "logo.png"),
]

logo_base64 = None
for path in logo_paths:
    logo_base64 = get_base64_image(path)
    if logo_base64:
        break

logo_html = (
    f'<img src="data:image/png;base64,{logo_base64}" style="height:110px; width:auto;" alt="FEEDAI Logo"/>'
    if logo_base64
    else '<div style="font-family:Syne,sans-serif;font-size:3rem;font-weight:800;color:white;">🍽️ FEEDAI</div>'
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    /* Hide Streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Main App background - dark green gradient */
    .stApp {
        background: linear-gradient(135deg, #0d7a3f 0%, #044d2a 50%, #022818 100%);
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    
    /* Wavy lines background (decorative) */
    .wave-container {
        position: fixed;
        top: 0;
        right: 0;
        width: 65%;
        height: 100vh;
        z-index: 1;
        pointer-events: none;
        overflow: hidden;
    }
    
    .wave-svg {
        position: absolute;
        top: 50%;
        right: -5%;
        transform: translateY(-50%);
        width: 110%;
        height: 90%;
        opacity: 0.55;
    }
    
    /* Top Navigation */
    .top-nav {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 4rem 1rem 4rem;
        background: transparent;
    }
    
    .nav-links {
        display: flex;
        gap: 4rem;
        align-items: center;
    }
    
    .nav-links a {
        color: white;
        text-decoration: none;
        font-size: 1.05rem;
        font-weight: 500;
        transition: opacity 0.3s;
        letter-spacing: 0.5px;
    }
    
    .nav-links a:hover {
        opacity: 0.7;
    }
    
    /* Hero Content - Left aligned */
    .hero-section {
        position: relative;
        z-index: 5;
        padding: 4rem 4rem 2rem 4rem;
        max-width: 720px;
        min-height: 60vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .hero-title {
        font-family: 'Syne', sans-serif;
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .hero-subtitle {
        color: white;
        font-size: 1.15rem;
        font-weight: 400;
        line-height: 1.6;
        margin-bottom: 3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.95;
    }
    
    /* Analyze Button - White pill */
    div.stButton > button {
        background: white !important;
        color: #044d2a !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        cursor: pointer !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
        min-width: 280px !important;
        text-align: left !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4) !important;
        background: #f8f8f8 !important;
    }
    
    /* Logo container styling */
    .logo-wrap {
        display: flex;
        align-items: center;
    }
    
    /* Hide file uploader visually but keep functional */
    .uploader-hidden {
        position: absolute;
        opacity: 0;
        height: 1px;
        width: 1px;
        overflow: hidden;
    }
    
    /* Results section */
    .results-box {
        position: relative;
        z-index: 10;
        background: rgba(255,255,255,0.95);
        margin: 2rem 4rem;
        padding: 2rem;
        border-radius: 16px;
        color: #044d2a;
    }
</style>
""", unsafe_allow_html=True)

# ====================== WAVY BACKGROUND (SVG) ======================
st.markdown("""
<div class="wave-container">
    <svg class="wave-svg" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
        <g fill="none" stroke="#0a6b35" stroke-width="2.5" opacity="0.9">
            <path d="M -50,300 Q 150,80 350,300 T 750,300 T 1150,300" />
            <path d="M -50,300 Q 150,110 350,300 T 750,300 T 1150,300" transform="translate(0,15)" />
            <path d="M -50,300 Q 150,140 350,300 T 750,300 T 1150,300" transform="translate(0,30)" />
            <path d="M -50,300 Q 150,170 350,300 T 750,300 T 1150,300" transform="translate(0,45)" />
            <path d="M -50,300 Q 150,200 350,300 T 750,300 T 1150,300" transform="translate(0,60)" />
            <path d="M -50,300 Q 150,230 350,300 T 750,300 T 1150,300" transform="translate(0,75)" />
            <path d="M -50,300 Q 150,260 350,300 T 750,300 T 1150,300" transform="translate(0,90)" />
            <path d="M -50,300 Q 150,80 350,300 T 750,300 T 1150,300" transform="translate(0,-15)" />
            <path d="M -50,300 Q 150,50 350,300 T 750,300 T 1150,300" transform="translate(0,-30)" />
            <path d="M -50,300 Q 150,20 350,300 T 750,300 T 1150,300" transform="translate(0,-45)" />
            <path d="M -50,300 Q 150,-10 350,300 T 750,300 T 1150,300" transform="translate(0,-60)" />
            <path d="M -50,300 Q 150,-40 350,300 T 750,300 T 1150,300" transform="translate(0,-75)" />
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# ====================== TOP NAVIGATION ======================
st.markdown(f"""
<div class="top-nav">
    <div class="logo-wrap">
        {logo_html}
    </div>
    <div class="nav-links">
        <a href="#">AI analyzer</a>
        <a href="#">sign up</a>
        <a href="#">sign in</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== HERO SECTION ======================
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">
        WATCH YOUR CALORIES
    </h1>
    <p class="hero-subtitle">
        UPLOAD OR SNAP ANY MEAL PHOTO. OUR AI IDENTIFIES DISHES,<br>
        INGREDIENTS, AND PORTION SIZES WITH HIGH ACCURACY.
    </p>
</div>
""", unsafe_allow_html=True)

# ====================== ANALYZE BUTTON + UPLOADER ======================
# Place button inside a left-padded container
col1, col2, col3 = st.columns([1, 4, 5])

with col1:
    st.write("")  # spacer

with col2:
    # Toggle uploader visibility via session state
    if "show_uploader" not in st.session_state:
        st.session_state.show_uploader = False
    
    if st.button("📸  Analyze My Meal", key="analyze_btn"):
        st.session_state.show_uploader = True

# Show uploader after button click
if st.session_state.get("show_uploader", False):
    st.markdown("<div style='padding: 1rem 4rem;'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your meal photo",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="visible"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        st.markdown("<div class='results-box'>", unsafe_allow_html=True)
        st.image(uploaded_file, caption="Your uploaded meal", use_container_width=True)
        
        with st.spinner("🔍 Analyzing your meal with AI..."):
            time.sleep(1.5)
        
        st.success("✅ Analysis Complete!")
        st.info("Connect your prediction model here.")
        st.markdown("</div>", unsafe_allow_html=True)