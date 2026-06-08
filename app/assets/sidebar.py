import streamlit as st

def render_sidebar(portion_default=150):
    """
    Renders the sidebar with:
    - Portion size slider
    - Daily meal tracker
    - About section
    Returns the selected portion size.
    """
    with st.sidebar:
        st.markdown("### ⚙️ Settings")

        portion = st.slider(
            "Portion size (grams)",
            min_value=50,
            max_value=600,
            value=portion_default,
            step=25,
            help="Adjust portion size to recalculate calories"
        )

        st.markdown("---")
        st.markdown("### 📋 Today's meals")

        # initialise session state
        if 'meals' not in st.session_state:
            st.session_state.meals = []

        if st.session_state.meals:
            total_cal = sum(m['calories'] for m in st.session_state.meals)

            for i, meal in enumerate(st.session_state.meals):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"**{meal['food']}**  \n"
                        f"{meal['calories']} kcal · {meal['portion']}g"
                    )
                with col2:
                    if st.button("✕", key=f"del_{i}"):
                        st.session_state.meals.pop(i)
                        st.rerun()

            st.markdown("---")
            st.markdown(f"**Total: {total_cal} kcal**")

            # progress bar toward 2000 kcal daily goal
            progress = min(total_cal / 2000, 1.0)
            st.progress(progress)
            st.caption(f"{total_cal} / 2000 kcal daily goal")

            if st.button("🗑️ Clear all meals"):
                st.session_state.meals = []
                st.rerun()
        else:
            st.caption(
                "No meals logged yet.\n"
                "Upload a food photo to get started."
            )

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.caption(
            "AI-powered food recognition using MobileNetV2 "
            "trained on Food-101.\n\n"
            "**Accuracy:** 92.4%  \n"
            "**Classes:** 10 food types"
        )

    return portion