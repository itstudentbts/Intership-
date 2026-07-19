"""
FEEDAI - AI Calorie Estimator
Adjusted: Logo + Nav + Hero pulled upward, perfectly aligned
"""

import streamlit as st
import os
import time
import base64

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="FEEDAI - AI Calories",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== LOAD LOGO ======================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

logo_paths = [
    "assets/logo.png",
    "assetss/logo.png",
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
    f'<img src="data:image/png;base64,{logo_base64}" style="height:95px; width:auto; display:block;" alt="FEEDAI Logo"/>'
    if logo_base64
    else '<div style="font-family:Syne,sans-serif;font-size:2.6rem;font-weight:800;color:white;">🍽️ FEEDAI</div>'
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    /* Hide Streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    
    /* Remove ALL top padding from main container */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .main .block-container {
        padding-top: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
    }
    
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Main App background */
    .stApp {
        background: linear-gradient(135deg, #0d7a3f 0%, #044d2a 50%, #022818 100%);
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    
    /* Wavy lines background */
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
    
    /* ====== TOP NAV — moved UP & aligned with logo ====== */
    .top-nav {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: space-between;
        align-items: center;       /* vertically center logo & links */
        padding: 1.2rem 4rem 0.5rem 4rem;   /* tighter top padding */
        background: transparent;
    }
    
    .logo-wrap {
        display: flex;
        align-items: center;
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
        letter-spacing: 0.5px;
        transition: opacity 0.3s;
    }
    
    .nav-links a:hover {
        opacity: 0.7;
    }
    
    /* ====== HERO — pulled UP, tighter spacing ====== */
    .hero-section {
        position: relative;
        z-index: 5;
        padding: 1.5rem 4rem 1rem 4rem;   /* MUCH less top padding */
        max-width: 760px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    
    .hero-title {
        font-family: 'Syne', sans-serif;
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.25;
        margin: 0 0 1.2rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .hero-subtitle {
        color: white;
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.6;
        margin: 0 0 2rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.95;
    }
    
    /* ====== BUTTON — directly under text ====== */
    div.stButton {
        padding: 0 4rem;             /* same left padding as hero */
        margin-top: -0.5rem;          /* pull button closer to text */
    }
    
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
    
    /* ====== RESPONSIVE ====== */
    @media (max-width: 768px) {
        .top-nav {
            flex-direction: column;
            gap: 1rem;
            padding: 1rem 1.5rem;
        }
        .nav-links {
            gap: 1.5rem;
        }
        .hero-section {
            padding: 1rem 1.5rem;
            max-width: 100%;
        }
        .hero-title {
            font-size: 1.6rem;
        }
        .hero-subtitle {
            font-size: 0.95rem;
        }
        div.stButton {
            padding: 0 1.5rem;
        }
        div.stButton > button {
            min-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ====================== WAVY BACKGROUND ======================
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

# ====================== TOP NAVIGATION (logo + links aligned) ======================
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

# ====================== HERO SECTION (pulled up) ======================
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

# ====================== ANALYZE BUTTON ======================
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

if st.button("📸  Analyze My Meal", key="analyze_btn"):
    st.session_state.show_uploader = True

# ====================== UPLOADER / RESULTS ======================
if st.session_state.get("show_uploader", False):
    st.markdown("<div style='padding: 1.5rem 4rem 0 4rem;'>", unsafe_allow_html=True)
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