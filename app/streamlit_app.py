import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import os
import time

# ── page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Food Calorie AI",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Manrope:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
    color: #1E293B;
}

.stApp {
    background: #F8FAFC;
}

/* ── hero section ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    color: #1E293B;
    line-height: 1.1;
    margin: 0;
}
.hero-title span {
    color: #10B981;
}
.hero-slang {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #FB923C;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0.4rem 0 0.2rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #64748B;
    font-weight: 300;
    margin: 0.4rem 0 0;
}

/* ── cards ── */
.card {
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.4rem;
    margin: 0.6rem 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.card-green {
    border-color: #10B98133;
    background: #F0FDF4;
}

/* ── food name ── */
.food-name {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #1E293B;
    margin: 0;
}
.conf-badge {
    display: inline-block;
    font-size: 0.75rem;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-weight: 600;
    margin-top: 0.4rem;
    letter-spacing: 0.04em;
}

/* ── calorie number ── */
.cal-number {
    font-family: 'Syne', sans-serif;
    font-size: 3.8rem;
    font-weight: 800;
    color: #10B981;
    line-height: 1;
    margin: 0;
}
.cal-unit {
    font-size: 0.75rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 500;
}

/* ── macro boxes ── */
.macro-box {
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.9rem;
    text-align: center;
}
.macro-val { font-size: 1.4rem; font-weight: 600; }
.macro-lbl { font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em; }

/* ── top3 row ── */
.t3-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid #F1F5F9;
}

/* ── empty state ── */
.empty-zone {
    border: 2px dashed #CBD5E1;
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    background: #fff;
    margin: 1rem 0;
}

/* ── how it works ── */
.how-card {
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    height: 100%;
}

/* ── signin form ── */
.signin-hero {
    text-align: center;
    padding: 1rem 0 2rem;
}
.signin-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #1E293B;
}
.signin-sub {
    color: #64748B;
    font-size: 0.9rem;
    font-weight: 300;
}
.form-card {
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 2rem 2rem;
    max-width: 500px;
    margin: 0 auto;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #10B981;
    margin: 1.2rem 0 0.4rem;
}
.tip-box {
    background: #FFF7ED;
    border: 1px solid #FB923C44;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: #92400E;
    margin: 0.5rem 0;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #fff;
    border-right: 1px solid #E2E8F0;
}
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #1E293B;
    font-family: 'Syne', sans-serif;
}

/* ── buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 600 !important;
}

/* ── progress bar color ── */
.stProgress > div > div {
    background: #10B981 !important;
}

/* ── slider ── */
.stSlider > div > div > div {
    background: #10B981 !important;
}

/* ── hide streamlit chrome ── */
#MainMenu {visibility:hidden;}
footer    {visibility:hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# ── paths ─────────────────────────────────────────────────
BASE_DIR         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH       = os.path.join(BASE_DIR, "models", "food_classifier.h5")
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "models", "class_names.json")
DATABASE_PATH    = os.path.join(BASE_DIR, "database", "calories.csv")

# ── session state init ────────────────────────────────────
if 'meals'    not in st.session_state: st.session_state.meals    = []
if 'page'     not in st.session_state: st.session_state.page     = 'home'
if 'user'     not in st.session_state: st.session_state.user     = None
if 'signed_in'not in st.session_state: st.session_state.signed_in= False

# ── load model (cached) ───────────────────────────────────
@st.cache_resource
def load_everything():
    try:
        model      = tf.keras.models.load_model(MODEL_PATH)
        class_names= json.load(open(CLASS_NAMES_PATH))
        cal_df     = pd.read_csv(DATABASE_PATH)
        return model, class_names, cal_df, None
    except Exception as e:
        return None, None, None, str(e)

# ── prediction ────────────────────────────────────────────
def predict(image, model, class_names, cal_df, portion_g):
    img  = image.convert('RGB').resize((224, 224))
    arr  = np.array(img) / 255.0
    arr  = np.expand_dims(arr, 0)
    probs= model.predict(arr, verbose=0)[0]
    top3_idx = np.argsort(probs)[::-1][:3]
    top3 = [
        {'food':       class_names[i].replace('_',' ').title(),
         'confidence': float(probs[i]),
         'raw':        class_names[i]}
        for i in top3_idx
    ]
    food_key   = top3[0]['raw']
    confidence = top3[0]['confidence']
    food_name  = top3[0]['food']
    row = cal_df[cal_df['food_name'] == food_key]
    if len(row) == 0:
        nutrition = None
    else:
        r = row.iloc[0]
        f = portion_g / 100
        nutrition = {
            'calories': round(r['calories_per_100g'] * f),
            'protein':  round(r['protein_g'] * f, 1),
            'carbs':    round(r['carbs_g'] * f, 1),
            'fat':      round(r['fat_g'] * f, 1),
            'per_100g': round(r['calories_per_100g']),
        }
    return food_name, confidence, top3, nutrition

# ── calorie goal based on profile ─────────────────────────
def get_calorie_goal(user):
    """Harris-Benedict formula for daily calorie goal."""
    if not user:
        return 2000
    try:
        w = user.get('weight', 70)
        h = user.get('height', 170)
        a = user.get('age', 25)
        sex = user.get('sex', 'Male')
        condition = user.get('condition', 'None')

        if sex == 'Female':
            bmr = 447.6 + (9.25 * w) + (3.10 * h) - (4.33 * a)
        else:
            bmr = 88.36 + (13.40 * w) + (4.80 * h) - (5.68 * a)

        goal = round(bmr * 1.55)  # moderate activity

        # adjust for special conditions
        if condition == 'Pregnant':
            goal += 300
        elif condition == 'Breastfeeding':
            goal += 500

        return goal
    except:
        return 2000

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:

    # greeting
    if st.session_state.signed_in and st.session_state.user:
        name = st.session_state.user.get('name', '').split()[0]
        st.markdown(f"### 👋 Hey, {name}!")
        if st.button("Sign out", use_container_width=True):
            st.session_state.signed_in = False
            st.session_state.user      = None
            st.session_state.page      = 'home'
            st.rerun()
    else:
        st.markdown("### 🍽️ Food Calorie AI")
        if st.button("🔐 Sign in / Create account",
                     use_container_width=True,
                     type="primary"):
            st.session_state.page = 'signin'
            st.rerun()

    st.markdown("---")

    # navigation
    st.markdown("### 📍 Navigation")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    with col2:
        if st.button("📊 Log", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    st.markdown("---")

    # portion slider
    st.markdown("### ⚙️ Settings")
    portion = st.slider(
        "Portion size (g)",
        min_value=50, max_value=600,
        value=150, step=25
    )

    st.markdown("---")

    # meal tracker
    st.markdown("### 📋 Today's meals")
    goal = get_calorie_goal(st.session_state.user)

    if st.session_state.meals:
        total_cal = sum(m['calories'] for m in st.session_state.meals)

        for i, meal in enumerate(st.session_state.meals):
            c1, c2 = st.columns([3,1])
            with c1:
                st.markdown(
                    f"**{meal['food']}**  \n"
                    f"{meal['calories']} kcal · {meal['portion']}g"
                )
            with c2:
                if st.button("✕", key=f"del_{i}"):
                    st.session_state.meals.pop(i)
                    st.rerun()

        st.markdown("---")
        progress = min(total_cal / goal, 1.0)
        st.progress(progress)

        color = "#10B981" if total_cal < goal * 0.9 else \
                "#FB923C" if total_cal < goal else "#EF4444"
        st.markdown(
            f"<p style='font-size:0.85rem;font-weight:600;color:{color}'>"
            f"{total_cal} / {goal} kcal</p>",
            unsafe_allow_html=True
        )

        if st.button("🗑️ Clear all", use_container_width=True):
            st.session_state.meals = []
            st.rerun()
    else:
        st.caption("No meals yet. Upload a food photo!")

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("MobileNetV2 · Food-101 · **92.4% accuracy**")


# ══════════════════════════════════════════════════════════
# PAGE: SIGN IN
# ══════════════════════════════════════════════════════════
if st.session_state.page == 'signin':

    st.markdown("""
    <div class="signin-hero">
        <p class="signin-title">Create your profile</p>
        <p class="signin-sub">
            Personalise your calorie goals based on who you are
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signin_form"):

        # ── personal info ──────────────────────────────
        st.markdown('<p class="section-label">👤 Personal info</p>',
                    unsafe_allow_html=True)

        name  = st.text_input("Full name", placeholder="e.g. Sofia Martin")
        email = st.text_input("Email address", placeholder="sofia@email.com")

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=13, max_value=100, value=25)
        with col2:
            sex = st.selectbox("Sex", ["Male", "Female"])

        # ── body measurements ──────────────────────────
        st.markdown('<p class="section-label">📏 Body measurements</p>',
                    unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            weight = st.number_input(
                "Weight (kg)", min_value=30.0,
                max_value=250.0, value=70.0, step=0.5
            )
        with col4:
            height = st.number_input(
                "Height (cm)", min_value=100.0,
                max_value=250.0, value=170.0, step=0.5
            )

        # ── female specific options ────────────────────
        condition = "None"
        if sex == "Female":
            st.markdown('<p class="section-label">🌸 Female health</p>',
                        unsafe_allow_html=True)

            st.markdown("""
            <div class="tip-box">
                💡 These options adjust your daily calorie goal automatically.
                Pregnant women need ~300 extra kcal/day.
                Breastfeeding women need ~500 extra kcal/day.
            </div>
            """, unsafe_allow_html=True)

            condition = st.selectbox(
                "Health condition",
                ["None", "Pregnant", "Breastfeeding"],
                help="We adjust your calorie goal accordingly"
            )

        # ── activity level ─────────────────────────────
        st.markdown('<p class="section-label">🏃 Activity level</p>',
                    unsafe_allow_html=True)

        activity = st.selectbox(
            "How active are you?",
            [
                "Sedentary (desk job, little exercise)",
                "Light (1-3 days/week exercise)",
                "Moderate (3-5 days/week exercise)",
                "Active (6-7 days/week exercise)",
                "Very active (physical job + training)"
            ],
            index=2
        )

        # ── goal ──────────────────────────────────────
        st.markdown('<p class="section-label">🎯 Your goal</p>',
                    unsafe_allow_html=True)

        goal_type = st.selectbox(
            "What are you aiming for?",
            ["Lose weight", "Maintain weight", "Gain muscle", "Eat healthier"]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "✅ Save my profile",
            use_container_width=True,
            type="primary"
        )

    if submitted:
        if not name or not email:
            st.error("Please fill in your name and email.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            # save user to session state
            st.session_state.user = {
                'name':      name,
                'email':     email,
                'age':       age,
                'sex':       sex,
                'weight':    weight,
                'height':    height,
                'condition': condition,
                'activity':  activity,
                'goal':      goal_type,
            }
            st.session_state.signed_in = True
            st.session_state.page      = 'home'

            # calculate their personalised goal
            personal_goal = get_calorie_goal(st.session_state.user)

            st.success(f"Welcome, {name.split()[0]}! 🎉")
            st.info(
                f"Based on your profile, your daily calorie goal "
                f"is **{personal_goal} kcal**."
                + (f" (+300 kcal for pregnancy 🤰)" if condition == 'Pregnant' else "")
                + (f" (+500 kcal for breastfeeding 🤱)" if condition == 'Breastfeeding' else "")
            )
            time.sleep(1.5)
            st.rerun()

    # back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to home"):
        st.session_state.page = 'home'
        st.rerun()


# ══════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════
elif st.session_state.page == 'home':

    # ── hero ──────────────────────────────────────────────
    user = st.session_state.user
    if user:
        first = user['name'].split()[0]
        st.markdown(f"""
        <div class="hero-wrap">
            <p class="hero-title">What did you eat,<br><span>{first}?</span></p>
            <p class="hero-slang">keep up with your calories, no cap 🔥</p>
            <p class="hero-sub">Snap it. Track it. Own your nutrition.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hero-wrap">
            <p class="hero-title">🍽️ Food<br><span>Calorie AI</span></p>
            <p class="hero-slang">keep up with your calories, no cap 🔥</p>
            <p class="hero-sub">Upload a photo · Get instant nutrition info</p>
        </div>
        """, unsafe_allow_html=True)

    # prompt sign in if not signed in
    if not st.session_state.signed_in:
        st.markdown("""
        <div style="background:#EFF6FF;border:1px solid #2563EB33;
                    border-radius:14px;padding:1rem 1.2rem;
                    margin:0.5rem 0 1.5rem;font-size:0.875rem;color:#1E40AF">
            💡 <strong>Sign in</strong> to get a personalised calorie goal
            based on your age, weight, height and health status.
            Hit the button in the sidebar!
        </div>
        """, unsafe_allow_html=True)

    # ── load model ────────────────────────────────────────
    model, class_names, cal_df, error = load_everything()

    if error:
        st.error(f"Could not load model: {error}")
        st.info(
            f"Make sure these files exist:\n"
            f"- `{MODEL_PATH}`\n"
            f"- `{CLASS_NAMES_PATH}`\n"
            f"- `{DATABASE_PATH}`"
        )
        st.stop()

    # ── upload ────────────────────────────────────────────
    with st.expander("📖 Supported foods (10 classes)"):
        foods = [
            "🎂 Chocolate Cake", "🍩 Donuts",
            "🍟 French Fries",   "🍔 Hamburger",
            "🌭 Hot Dog",        "🍦 Ice Cream",
            "🍕 Pizza",          "🍜 Ramen",
            "🥩 Steak",          "🍣 Sushi"
        ]
        c1, c2 = st.columns(2)
        for i, f in enumerate(foods):
            (c1 if i % 2 == 0 else c2).markdown(f)

    uploaded = st.file_uploader(
        "Drop a food photo here",
        type=["jpg","jpeg","png","webp"]
    )

    # ── results ───────────────────────────────────────────
    if uploaded:
        from PIL import Image as PILImage
        image = PILImage.open(uploaded)

        col_img, _ = st.columns([1,1])
        with col_img:
            st.image(image, caption="Your photo",
                     use_container_width=True)

        st.markdown("---")

        with st.spinner("Analysing your food... hang tight 👀"):
            time.sleep(0.4)
            food_name, confidence, top3, nutrition = predict(
                image, model, class_names, cal_df, portion
            )

        # food name + confidence
        conf_pct   = confidence * 100
        conf_color = (
            "#10B981" if conf_pct > 70 else
            "#FB923C" if conf_pct > 40 else
            "#EF4444"
        )
        conf_bg = (
            "#F0FDF4" if conf_pct > 70 else
            "#FFF7ED" if conf_pct > 40 else
            "#FEF2F2"
        )
        st.markdown(
            f'<p class="food-name">{food_name}</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<span class="conf-badge" '
            f'style="background:{conf_bg};color:{conf_color}">'
            f'⬤ {conf_pct:.1f}% confident</span>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # calories + macros
        if nutrition:
            goal_val = get_calorie_goal(st.session_state.user)
            pct_of_goal = round(nutrition['calories'] / goal_val * 100)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="card card-green">
                    <p class="cal-number">{nutrition['calories']}</p>
                    <p class="cal-unit">kcal · {portion}g</p>
                    <p style="font-size:0.72rem;color:#10B981;
                               margin:0.4rem 0 0;font-weight:600">
                        {pct_of_goal}% of your daily goal
                    </p>
                </div>
                """, unsafe_allow_html=True)

            macros = [
                (col2, nutrition['protein'], "Protein",  "#2563EB"),
                (col3, nutrition['carbs'],   "Carbs",    "#FB923C"),
                (col4, nutrition['fat'],     "Fat",      "#10B981"),
            ]
            for col, val, lbl, clr in macros:
                with col:
                    st.markdown(f"""
                    <div class="macro-box">
                        <div class="macro-val" style="color:{clr}">{val}g</div>
                        <div class="macro-lbl">{lbl}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.caption(f"Per 100g: {nutrition['per_100g']} kcal")

        else:
            st.warning("Food not found in calorie database.")

        st.markdown("---")

        # top 3
        st.markdown("#### 🔍 Top 3 predictions")
        for i, pred in enumerate(top3):
            pct   = pred['confidence'] * 100
            color = "#10B981" if i == 0 else "#CBD5E1"
            st.markdown(f"""
            <div class="t3-row">
                <span style="font-size:0.75rem;color:#94A3B8;width:20px">#{i+1}</span>
                <span style="flex:1;font-size:0.9rem;color:#1E293B">{pred['food']}</span>
                <div style="width:110px;height:5px;background:#F1F5F9;border-radius:3px">
                    <div style="width:{int(pct)}%;height:5px;
                                background:{color};border-radius:3px"></div>
                </div>
                <span style="font-size:0.8rem;color:#64748B;
                             width:45px;text-align:right">{pct:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # add to meals
        if nutrition:
            cb, _ = st.columns([1,2])
            with cb:
                if st.button("➕ Add to today's meals",
                             use_container_width=True,
                             type="primary"):
                    st.session_state.meals.append({
                        'food':     food_name,
                        'calories': nutrition['calories'],
                        'portion':  portion
                    })
                    st.success(
                        f"Added {food_name} "
                        f"({nutrition['calories']} kcal) ✅"
                    )
                    st.rerun()

        # low confidence tip
        if confidence < 0.5:
            st.warning(
                f"⚠️ The model isn't super sure ({conf_pct:.0f}%). "
                "Try a clearer photo — good lighting, one food item, "
                "centred in frame."
            )

    else:
        # empty state
        st.markdown("""
        <div class="empty-zone">
            <p style="font-size:3.5rem;margin:0">📸</p>
            <p style="color:#1E293B;font-weight:600;
                      margin:0.5rem 0 0.2rem;font-size:1.1rem">
                Drop your food photo here
            </p>
            <p style="color:#94A3B8;font-size:0.85rem;margin:0">
                JPG · PNG · WEBP supported
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # how it works
        st.markdown(
            "<p style='font-family:Syne,serif;font-size:1.2rem;"
            "font-weight:700;color:#1E293B;margin-bottom:1rem'>"
            "How it works</p>",
            unsafe_allow_html=True
        )
        h1, h2, h3 = st.columns(3)
        steps = [
            (h1, "📷", "Snap it",
             "Take or upload a photo of your meal"),
            (h2, "🤖", "AI reads it",
             "MobileNetV2 identifies the food with 92.4% accuracy"),
            (h3, "📊", "Track it",
             "Get calories + macros and log your daily meals"),
        ]
        for col, icon, title, desc in steps:
            with col:
                st.markdown(f"""
                <div class="how-card">
                    <p style="font-size:2rem;margin:0">{icon}</p>
                    <p style="font-weight:700;font-size:0.95rem;
                               color:#1E293B;margin:0.5rem 0 0.2rem">{title}</p>
                    <p style="color:#64748B;font-size:0.8rem;margin:0">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # stats strip
        st.markdown("<br>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        stats = [
            (s1, "92.4%",  "Model accuracy",   "#10B981"),
            (s2, "10",     "Food categories",  "#2563EB"),
            (s3, "101K+",  "Training images",  "#FB923C"),
        ]
        for col, val, lbl, clr in stats:
            with col:
                st.markdown(f"""
                <div style="text-align:center;padding:1rem">
                    <p style="font-family:'Syne',sans-serif;font-size:2rem;
                               font-weight:800;color:{clr};margin:0">{val}</p>
                    <p style="font-size:0.75rem;color:#94A3B8;
                               text-transform:uppercase;letter-spacing:0.08em;
                               margin:0">{lbl}</p>
                </div>
                """, unsafe_allow_html=True)
