"""
FEEDAI - Sign In Page
Inspired by clean travel login card layout, FEEDAI green color scheme
"""

import streamlit as st
import os
import base64

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="FEEDAI - Sign In",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== LOAD IMAGES ======================
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

bg_base64 = None
for bg_name in ["background.jpg", "background.png", "bg.jpg", "bg.png",
                "food.jpg", "food.png", "hero.jpg", "hero.png", "brunch.jpg"]:
    bg_base64 = find_asset(bg_name)
    if bg_base64:
        break

bg_style = (
    f"background: linear-gradient(rgba(2, 40, 24, 0.52), rgba(4, 77, 42, 0.60)), "
    f"url('data:image/jpeg;base64,{bg_base64}') center/cover no-repeat fixed;"
    if bg_base64
    else "background: linear-gradient(135deg, #0d7a3f 0%, #044d2a 50%, #022818 100%);"
)

logo_html = (
    f'<img src="data:image/png;base64,{logo_base64}" '
    f'style="height:52px; width:auto; display:block; '
    f'filter: drop-shadow(0 2px 8px rgba(0,0,0,0.5));" alt="FEEDAI Logo"/>'
    if logo_base64
    else '<span style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:white;letter-spacing:2px;">🍽️ FEEDAI</span>'
)

# ====================== CSS ======================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    #MainMenu, footer, header {{ visibility: hidden; }}
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stToolbar"] {{ display: none; }}

    /* Full-bleed background */
    .stApp {{
        {bg_style}
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }}

    /* Remove all Streamlit padding so we control layout */
    .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }}

    /* ── LOGO: fixed top-left corner ── */
    .logo-fixed {{
        position: fixed;
        top: 1.4rem;
        left: 1.8rem;
        z-index: 999;
    }}

    /* ── BRAND TEXT: left side, vertically centered ── */
    .brand-block {{
        position: fixed;
        top: 50%;
        left: 5%;
        transform: translateY(-50%);
        max-width: 420px;
        color: white;
        z-index: 10;
    }}

    .brand-tagline {{
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #A7F3D0;
        margin: 0 0 1.2rem 0;
    }}

    .brand-headline {{
        font-family: 'Syne', sans-serif;
        font-size: 3.8rem;
        font-weight: 800;
        line-height: 1.0;
        text-transform: uppercase;
        margin: 0 0 1.2rem 0;
        color: white;
        text-shadow: 0 4px 24px rgba(0,0,0,0.5);
        letter-spacing: 2px;
    }}

    .brand-sub {{
        font-size: 1.15rem;
        font-weight: 500;
        margin-bottom: 0.6rem;
        color: white;
        text-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }}

    .brand-desc {{
        font-size: 0.95rem;
        line-height: 1.6;
        opacity: 0.9;
        color: white;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}

    /* ── CARD WRAPPER: right side, vertically centered ── */
    /* We float the Streamlit column content to the right */
    [data-testid="stColumns"] {{
        gap: 0 !important;
    }}

    /* Left column: invisible spacer */
    [data-testid="column"]:first-child {{
        visibility: hidden;
    }}

    /* Right column: the actual form */
    [data-testid="column"]:last-child {{
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        padding: 2rem 3rem 2rem 0 !important;
    }}

    [data-testid="column"]:last-child > div {{
        width: 100%;
    }}

    /* ── THE CARD ITSELF ── */
    /* Strategy: style ALL streamlit elements inside the right column
       to look like they're inside one card, using a wrapper div + 
       CSS that targets the stVerticalBlock */

    .card-shell {{
    background: rgba(240, 248, 244, 0.18);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 24px;
    padding: 3.2rem 3.2rem 2.8rem 3.2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    width: 100%;
    max-width: 560px;
    margin: 0 auto;
}}

    .form-title {{
        font-family: 'Syne', sans-serif;
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
        text-align: center;
    }}

    .form-welcome {{
        color: #A7F3D0;
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 1.6rem;
        font-weight: 400;
    }}

    .field-label {{
        color: white;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.4rem 0;
        display: block;
    }}

    /* ── INPUT FIELDS: white, clean like inspo ── */
    .stTextInput > div > div > input {{
        background: rgba(255, 255, 255, 0.92) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
        font-size: 0.98rem !important;
        color: #1a3d2b !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
    }}

    .stTextInput > div > div > input:focus {{
        background: white !important;
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2) !important;
    }}

    .stTextInput > div > div > input::placeholder {{
        color: #9ca3af !important;
    }}

    .stTextInput label {{ display: none !important; }}

    /* ── FORGOT PASSWORD ── */
    .forgot-row {{
        display: flex;
        justify-content: flex-end;
        margin: 0.2rem 0 1.2rem 0;
    }}

    .forgot-link {{
        color: #A7F3D0;
        font-size: 0.85rem;
        text-decoration: none;
        font-weight: 500;
    }}

    .forgot-link:hover {{
        color: white;
        text-decoration: underline;
    }}

    /* ── SIGN IN BUTTON: green, full width, rounded ── */
    div.stButton > button {{
        width: 100% !important;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.85rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45) !important;
        transition: all 0.3s ease !important;
    }}

    div.stButton > button:hover {{
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 10px 28px rgba(16, 185, 129, 0.55) !important;
        transform: translateY(-2px) !important;
    }}

    div.stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* ── DIVIDER ── */
    .divider-row {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 1.2rem 0;
    }}

    .divider-line {{
        flex: 1;
        height: 1px;
        background: rgba(255, 255, 255, 0.3);
    }}

    .divider-text {{
        color: rgba(255,255,255,0.7);
        font-size: 0.85rem;
        font-weight: 500;
    }}

    /* ── GOOGLE BUTTON: green rounded, matches Sign In ── */
    .google-btn {{
        width: 100%;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.8rem 1rem;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.65rem;
        transition: all 0.3s ease;
        text-decoration: none;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
        letter-spacing: 0.3px;
    }}

    .google-btn:hover {{
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(16, 185, 129, 0.5);
        color: white;
        text-decoration: none;
    }}

    .google-icon {{
        width: 20px;
        height: 20px;
        background: white;
        border-radius: 50%;
        padding: 2px;
        flex-shrink: 0;
    }}

    /* ── SIGN UP PROMPT ── */
    .signup-prompt {{
        text-align: center;
        margin-top: 1.4rem;
        color: rgba(255,255,255,0.82);
        font-size: 0.9rem;
    }}

    .signup-link {{
        color: #A7F3D0;
        font-weight: 600;
        text-decoration: none;
        margin-left: 4px;
    }}

    .signup-link:hover {{
        color: white;
        text-decoration: underline;
    }}

    /* Tighten Streamlit's default vertical gaps */
    [data-testid="stVerticalBlock"] > div {{
        padding-bottom: 0.3rem !important;
    }}

    .stTextInput {{
        margin-bottom: 0 !important;
    }}
</style>
""", unsafe_allow_html=True)

# ── LOGO: absolutely top-left ──
st.markdown(f"""
<div class="logo-fixed">
    {logo_html}
</div>
""", unsafe_allow_html=True)

# ── BRAND TEXT: left side ──
st.markdown("""
<div class="brand-block">
    <div class="brand-tagline">AI-Powered Nutrition</div>
    <h1 class="brand-headline">EAT<br>SMART</h1>
    <p class="brand-sub">Discover What's On Your Plate.</p>
    <p class="brand-desc">
        Snap any meal and let our AI instantly identify dishes,
        ingredients, and portion sizes — making healthy eating
        effortless and intelligent.
    </p>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT: left spacer | right form ──
_, right_col = st.columns([1, 1], gap="small")

with right_col:
    # Card top (pure HTML — no Streamlit widgets yet)
    st.markdown("""
    <div class="card-shell">
        <h2 class="form-title">Welcome Back</h2>
        <p class="form-welcome">Sign in to continue your nutrition journey</p>
        <label class="field-label">Email</label>
    </div>
    """, unsafe_allow_html=True)

    # Email input — Streamlit renders this AFTER the div closes, so we use
    # negative margin trick to pull it visually inside the card
    st.markdown("""
    <style>
        /* Pull the two text inputs UP into the card shell visually */
        [data-testid="column"]:last-child .stTextInput:nth-of-type(1) {{
            margin-top: -1rem;
        }}
    </style>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "Email", placeholder="Enter your email",
        label_visibility="collapsed", key="email_input"
    )

    st.markdown('<label class="field-label">Password</label>', unsafe_allow_html=True)

    password = st.text_input(
        "Password", type="password", placeholder="••••••••••",
        label_visibility="collapsed", key="password_input"
    )

    st.markdown("""
    <div class="forgot-row">
        <a href="#" class="forgot-link">Forgot password?</a>
    </div>
    """, unsafe_allow_html=True)

    if st.button("SIGN IN", key="signin_btn"):
        if email and password:
            st.success("✅ Signed in successfully!")
        else:
            st.error("Please fill in both fields.")

    st.markdown("""
    <div class="divider-row">
        <div class="divider-line"></div>
        <div class="divider-text">or</div>
        <div class="divider-line"></div>
    </div>

    <a href="/?google_auth=true" class="google-btn">
        <svg class="google-icon" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C12.955 4 4 12.955 4 24s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>
            <path fill="#FF3D00" d="M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C16.318 4 9.656 8.337 6.306 14.691z"/>
            <path fill="#4CAF50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.91 11.91 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>
            <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002l6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z"/>
        </svg>
        Sign in with Google
    </a>

    <div class="signup-prompt">
        New to FEEDAI?
        <a href="#" class="signup-link">Create an Account</a>
    </div>
    """, unsafe_allow_html=True)
