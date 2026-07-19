"""
FEEDAI - Sign Up Page (Glassmorphism Edition)
Modern glass UI with frosted panels for every element
"""

import streamlit as st
import os
import base64

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="FEEDAI - Create Account",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== LOAD ASSETS ======================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def find_asset(filename):
    paths = [
        f"assets/{filename}",
        f"assetss/{filename}",
        f"./assets/{filename}",
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
    f'<img src="data:image/png;base64,{logo_base64}" style="height:70px; width:auto; display:block; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4));" alt="FEEDAI Logo"/>'
    if logo_base64
    else '<div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;color:white;">🍽️ FEEDAI</div>'
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    /* Hide Streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    /* ====== APP BACKGROUND ====== */
    .stApp {
        background: linear-gradient(135deg, #0d7a3f 0%, #044d2a 50%, #022818 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Wave decoration */
    .wave-bg {
        position: fixed;
        top: 0;
        right: 0;
        width: 55%;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.4;
    }
    .wave-bg svg { width: 100%; height: 100%; }
    
    /* ====== TOP BAR ====== */
    .top-bar {
        position: relative;
        z-index: 10;
        padding: 1.5rem 4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* NEW: Rounded glass "Back to Home" button */
    .back-btn {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1.5px solid rgba(255, 255, 255, 0.25);
        color: white;
        text-decoration: none;
        font-size: 0.92rem;
        font-weight: 600;
        padding: 0.65rem 1.5rem;
        border-radius: 50px;
        transition: all 0.35s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        letter-spacing: 0.3px;
    }
    
    .back-btn:hover {
        background: rgba(255, 255, 255, 0.22);
        border-color: rgba(255, 255, 255, 0.45);
        transform: translateX(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
        color: white;
    }
    
    .back-btn .arrow {
        font-size: 1.05rem;
        transition: transform 0.3s;
    }
    
    .back-btn:hover .arrow {
        transform: translateX(-3px);
    }
    
    /* ====== MAIN CONTAINER ====== */
    .signup-container {
        position: relative;
        z-index: 5;
        max-width: 820px;
        margin: 1rem auto 3rem auto;
        padding: 0 2rem;
    }
    
    .page-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .page-title {
        font-family: 'Syne', sans-serif;
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 0.6rem 0;
        text-shadow: 0 4px 25px rgba(0,0,0,0.4);
        letter-spacing: 0.5px;
    }
    
    .page-subtitle {
        color: #D1FAE5;
        font-size: 1.05rem;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.3px;
        opacity: 0.95;
    }
    
    /* ====== GLASS SECTION CARDS ====== */
    .glass-section {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1.5px solid rgba(255, 255, 255, 0.18);
        border-radius: 24px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transition: all 0.4s ease;
    }
    
    .glass-section:hover {
        border-color: rgba(255, 255, 255, 0.28);
        box-shadow: 
            0 25px 60px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Section heading */
    .section-heading {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.7rem;
        margin: 0 0 1.8rem 0;
        padding-bottom: 1rem;
        border-bottom: 1.5px solid rgba(255, 255, 255, 0.15);
    }
    
    .section-icon {
        font-size: 1.4rem;
        filter: drop-shadow(0 2px 6px rgba(0,0,0,0.3));
    }
    
    .section-title {
        color: white;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Field labels */
    .field-label {
        color: #ECFDF5;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 0 0 0.5rem 4px;
        display: block;
        letter-spacing: 0.4px;
    }
    
    /* ====== GLASS INPUTS — every field is its own glass panel ====== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background: rgba(255, 255, 255, 0.10) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.20) !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.1rem !important;
        font-size: 0.95rem !important;
        color: white !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: rgba(167, 243, 208, 0.7) !important;
        box-shadow: 
            0 0 0 3px rgba(167, 243, 208, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.55) !important;
        font-weight: 400 !important;
    }
    
    /* Glass selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.10) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.20) !important;
        border-radius: 14px !important;
        color: white !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stSelectbox > div > div:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(167, 243, 208, 0.5) !important;
    }
    
    .stSelectbox > div > div > div {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Selectbox dropdown arrow */
    .stSelectbox svg {
        fill: white !important;
        color: white !important;
    }
    
    /* Selectbox dropdown menu (when open) */
    [data-baseweb="popover"] {
        background: rgba(4, 77, 42, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 14px !important;
        border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] li {
        background: transparent !important;
        color: white !important;
    }
    
    [data-baseweb="popover"] li:hover {
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Hide default Streamlit labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stDateInput label {
        display: none !important;
    }
    
    /* Number input +/- buttons — glass style */
    .stNumberInput button {
        background: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        border: 1.5px solid rgba(255, 255, 255, 0.20) !important;
        transition: all 0.25s !important;
        border-radius: 10px !important;
    }
    
    .stNumberInput button:hover {
        background: rgba(167, 243, 208, 0.3) !important;
        border-color: rgba(167, 243, 208, 0.6) !important;
        color: white !important;
    }
    
    /* Password eye icon visibility */
    .stTextInput button {
        background: transparent !important;
        color: rgba(255,255,255,0.7) !important;
        border: none !important;
    }
    
    .stTextInput button:hover {
        color: white !important;
    }
    
    /* ====== PRIMARY CTA BUTTON ====== */
    div.stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
        padding: 1rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        border-radius: 50px !important;
        cursor: pointer !important;
        box-shadow: 
            0 10px 30px rgba(16, 185, 129, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.35s ease !important;
        width: 100% !important;
        backdrop-filter: blur(10px) !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 15px 40px rgba(16, 185, 129, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    }
    
    /* Helper text */
    .helper-text {
        color: rgba(236, 253, 245, 0.7);
        font-size: 0.82rem;
        margin: 0.5rem 0 0 4px;
        font-style: italic;
        letter-spacing: 0.2px;
    }
    
    /* ====== "ALREADY HAVE ACCOUNT" — Beige prominent link ====== */
    .signin-prompt-wrapper {
        text-align: center;
        margin-top: 2rem;
        padding: 1.2rem;
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1.5px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .signin-prompt-text {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1rem;
        margin: 0;
        font-weight: 400;
    }
    
    .signin-link {
        color: #F5E6C8;                /* warm beige — best contrast on dark green */
        font-weight: 700;
        text-decoration: none;
        margin-left: 8px;
        padding: 4px 12px;
        border-radius: 8px;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
        border-bottom: 2px solid transparent;
    }
    
    .signin-link:hover {
        color: #FFF7E0;
        background: rgba(245, 230, 200, 0.12);
        border-bottom-color: #F5E6C8;
        text-shadow: 0 0 12px rgba(245, 230, 200, 0.5);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .top-bar { padding: 1rem 1.5rem; }
        .signup-container { padding: 0 1rem; }
        .glass-section { padding: 1.5rem 1.2rem; }
        .page-title { font-size: 1.8rem; }
        .back-btn { padding: 0.5rem 1.1rem; font-size: 0.85rem; }
    }
</style>
""", unsafe_allow_html=True)

# ====================== DECORATIVE WAVE BG ======================
st.markdown("""
<div class="wave-bg">
    <svg viewBox="0 0 800 800" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
        <g fill="none" stroke="#10B981" stroke-width="1.5" opacity="0.6">
            <path d="M -50,400 Q 200,150 400,400 T 850,400" />
            <path d="M -50,400 Q 200,180 400,400 T 850,400" transform="translate(0,20)" />
            <path d="M -50,400 Q 200,210 400,400 T 850,400" transform="translate(0,40)" />
            <path d="M -50,400 Q 200,240 400,400 T 850,400" transform="translate(0,60)" />
            <path d="M -50,400 Q 200,270 400,400 T 850,400" transform="translate(0,80)" />
            <path d="M -50,400 Q 200,120 400,400 T 850,400" transform="translate(0,-20)" />
            <path d="M -50,400 Q 200,90 400,400 T 850,400" transform="translate(0,-40)" />
            <path d="M -50,400 Q 200,60 400,400 T 850,400" transform="translate(0,-60)" />
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# ====================== TOP BAR (with NEW rounded Back button) ======================
st.markdown(f"""
<div class="top-bar">
    <div>{logo_html}</div>
    <a href="/" class="back-btn" target="_self">
        <span class="arrow">←</span> Back to Home
    </a>
</div>
""", unsafe_allow_html=True)

# ====================== PAGE HEADER ======================
st.markdown("""
<div class="signup-container">
    <div class="page-header">
        <h1 class="page-title">Create Your Free Account</h1>
        <p class="page-subtitle">Personalize your nutrition goals based on who you are</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== FORM CONTAINER ======================
_, center, _ = st.columns([1, 4, 1])

with center:
    # ============= SECTION 1: ACCOUNT INFORMATION =============
    st.markdown("""
    <div class="glass-section">
        <div class="section-heading">
            <span class="section-icon">👤</span>
            <h3 class="section-title">Account Information</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<label class="field-label">First Name</label>', unsafe_allow_html=True)
        first_name = st.text_input("First Name", placeholder="e.g. Salma", label_visibility="collapsed", key="first_name")
    with col2:
        st.markdown('<label class="field-label">Last Name</label>', unsafe_allow_html=True)
        last_name = st.text_input("Last Name", placeholder="e.g. Elmoussadak", label_visibility="collapsed", key="last_name")
    
    st.markdown('<label class="field-label" style="margin-top:1rem;">Email Address</label>', unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="you@example.com", label_visibility="collapsed", key="email")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<label class="field-label" style="margin-top:1rem;">Password</label>', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="••••••••••", label_visibility="collapsed", key="password")
    with col4:
        st.markdown('<label class="field-label" style="margin-top:1rem;">Confirm Password</label>', unsafe_allow_html=True)
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••••", label_visibility="collapsed", key="confirm_password")
    
    st.markdown('<p class="helper-text">Password must be at least 8 characters long</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============= SECTION 2: PERSONAL INFORMATION =============
    st.markdown("""
    <div class="glass-section">
        <div class="section-heading">
            <span class="section-icon">📋</span>
            <h3 class="section-title">Personal Information</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    with col5:
        st.markdown('<label class="field-label">Age</label>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=10, max_value=100, value=25, step=1, label_visibility="collapsed", key="age")
    with col6:
        st.markdown('<label class="field-label">Sex</label>', unsafe_allow_html=True)
        sex = st.selectbox("Sex", ["Female", "Male", "Prefer not to say"], label_visibility="collapsed", key="sex")
    
    st.markdown('<label class="field-label" style="margin-top:1rem;">Date of Birth</label>', unsafe_allow_html=True)
    col7, col8, col9 = st.columns(3)
    with col7:
        day = st.selectbox("Day", list(range(1, 32)), label_visibility="collapsed", key="day")
    with col8:
        month = st.selectbox("Month",
            ["January","February","March","April","May","June",
             "July","August","September","October","November","December"],
            label_visibility="collapsed", key="month")
    with col9:
        year = st.selectbox("Year", list(range(2024, 1940, -1)), index=25, label_visibility="collapsed", key="year")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============= SECTION 3: BODY MEASUREMENTS =============
    st.markdown("""
    <div class="glass-section">
        <div class="section-heading">
            <span class="section-icon">📏</span>
            <h3 class="section-title">Body Measurements</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col10, col11 = st.columns(2)
    with col10:
        st.markdown('<label class="field-label">Weight (kg)</label>', unsafe_allow_html=True)
        weight = st.number_input("Weight", min_value=20.0, max_value=300.0, value=65.0, step=0.5, label_visibility="collapsed", key="weight")
    with col11:
        st.markdown('<label class="field-label">Height (cm)</label>', unsafe_allow_html=True)
        height = st.number_input("Height", min_value=80.0, max_value=250.0, value=165.0, step=0.5, label_visibility="collapsed", key="height")
    
    st.markdown('<p class="helper-text">We use this to calculate your daily calorie needs</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============= SECTION 4: ACTIVITY LEVEL =============
    st.markdown("""
    <div class="glass-section">
        <div class="section-heading">
            <span class="section-icon">🏃</span>
            <h3 class="section-title">Activity Level</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<label class="field-label">How active are you?</label>', unsafe_allow_html=True)
    activity = st.selectbox(
        "Activity",
        [
            "Sedentary (little to no exercise)",
            "Light (1-2 days/week exercise)",
            "Moderate (3-5 days/week exercise)",
            "Active (6-7 days/week exercise)",
            "Very Active (intense daily exercise)"
        ],
        index=2,
        label_visibility="collapsed",
        key="activity"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============= SECTION 5: YOUR GOAL =============
    st.markdown("""
    <div class="glass-section">
        <div class="section-heading">
            <span class="section-icon">🎯</span>
            <h3 class="section-title">Your Goal</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<label class="field-label">What are you aiming for?</label>', unsafe_allow_html=True)
    goal = st.selectbox(
        "Goal",
        [
            "Lose Weight",
            "Maintain Weight",
            "Gain Weight",
            "Build Muscle",
            "Improve Overall Health",
            "Track Nutrition"
        ],
        label_visibility="collapsed",
        key="goal"
    )
    
    st.markdown('<p class="helper-text">We\'ll personalize your daily calorie and nutrition recommendations</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============= SUBMIT BUTTON =============
    st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
    
    if st.button("CREATE MY ACCOUNT", key="create_account_btn"):
        if not first_name or not last_name:
            st.error("⚠️ Please enter your full name.")
        elif not email or "@" not in email:
            st.error("⚠️ Please enter a valid email address.")
        elif len(password) < 8:
            st.error("⚠️ Password must be at least 8 characters.")
        elif password != confirm_password:
            st.error("⚠️ Passwords do not match.")
        else:
            st.success(f"✅ Welcome to FEEDAI, {first_name}! Your account has been created.")
            st.balloons()
            st.session_state.user = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "age": age,
                "sex": sex,
                "birthday": f"{day} {month} {year}",
                "weight": weight,
                "height": height,
                "activity": activity,
                "goal": goal
            }
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============= "ALREADY HAVE ACCOUNT" — Beige prominent link =============
    st.markdown("""
    <div class="signin-prompt-wrapper">
        <p class="signin-prompt-text">
            Already have an account?
            <a href="/Sign_In" class="signin-link" target="_self">Sign In →</a>
        </p>
    </div>
    """, unsafe_allow_html=True)