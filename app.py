
import streamlit as st
import joblib
import base64
from pathlib import Path

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="NewsCheck - Fake News Detector",
    page_icon="📰",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

# ==================================================
# 2. LOAD MODEL AND VECTORIZER
# ==================================================

try:
    vectorizer = joblib.load(BASE_DIR / "vectorizer.jb")
    model = joblib.load(BASE_DIR / "model.jb")
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# ==================================================
# 3. BACKGROUND IMAGE
# ==================================================

image_path = BASE_DIR / "newsroom.jpg"

if image_path.exists():
    extension = image_path.suffix.lower()
    mime_type = "image/png" if extension == ".png" else "image/jpeg"

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    background = f'url("data:{mime_type};base64,{encoded}")'
else:
    background = "linear-gradient(135deg, #020617, #0f172a, #172554)"

# ==================================================
# 4. CUSTOM DESIGN
# ==================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(
                rgba(2, 8, 23, 0.88),
                rgba(2, 8, 23, 0.94)
            ),
            {background};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1200px;
        padding-top: 2rem;
    }}

    h1, h2, h3, h4, p, label {{
        color: white;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-radius: 16px;
    }}

    .stTextArea textarea {{
        background-color: #111c32 !important;
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }}

    .stButton button {{
        background: linear-gradient(90deg, #0284c7, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        height: 48px;
        font-weight: bold;
        width: 100%;
    }}

    .stButton button:hover {{
        background: #0369a1;
        color: white;
        border: 1px solid #38bdf8;
    }}

    div[data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# 5. SESSION STATE
# ==================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==================================================
# 6. HEADER
# ==================================================

header1, header2 = st.columns([2, 1])

with header1:
    st.title("📰 NEWS :blue[CHECK]")
    st.caption("YOUR DIGITAL NEWS VERIFICATION PLATFORM")

with header2:
    st.markdown("### 🔴 LIVE NEWS DESK")
    st.caption("AI-POWERED NEWS ANALYSIS")

st.divider()

# ==================================================
# 7. BREAKING NEWS TICKER
# ==================================================

st.error(
    "🔴 BREAKING NEWS  |  THINK BEFORE YOU SHARE  "
    "◆  VERIFY BEFORE YOU TRUST  "
    "◆  STOP THE SPREAD OF MISINFORMATION"
)

# ==================================================
# 8. HERO SECTION
# ==================================================

st.markdown(
    """
    <div style="text-align:center; padding:25px 5px;">
    """,
    unsafe_allow_html=True
)

st.title("STOP. CHECK. TRUST.")

st.markdown(
    """
    <div style="text-align:center;">
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "In a world full of information, know what deserves your trust."
)

st.write(
    "Analyze news articles and detect potential misinformation "
    "using Machine Learning and Natural Language Processing."
)

st.divider()

# ==================================================
# 9. MAIN DASHBOARD
# ==================================================

left, right = st.columns([1.4, 1], gap="large")

with left:

    with st.container(border=True):

        st.subheader("📡 News Analysis Desk")

        st.write(
            "Submit a news article below to analyze its authenticity."
        )

        st.caption("PASTE YOUR NEWS ARTICLE")

        news_input = st.text_area(
            "News Article",
            placeholder=(
                "Paste your complete news article here...\n\n"
                "Enter the article to check whether it is Fake or Real."
            ),
            height=230,
            label_visibility="collapsed"
        )

        analyze = st.button(
            "🔍 ANALYZE NEWS NOW",
            use_container_width=True
        )

with right:

    with st.container(border=True):

        st.subheader("🛡️ Verification Center")

        st.write(
            "Our machine learning model analyzes the submitted article."
        )

        st.divider()

        st.markdown("### 🔵 HOW IT WORKS")

        st.markdown("📝 **01. Submit**")
        st.caption("Enter your news article.")

        st.markdown("⚙️ **02. Analyze**")
        st.caption("Text is processed using NLP and machine learning.")

        st.markdown("🎯 **03. Predict**")
        st.caption("Get your Fake or Real classification.")

        st.divider()

        st.success("AI-powered news classification system")

# ==================================================
# 10. PREDICTION
# ==================================================

if analyze:

    if not news_input.strip():

        st.warning("⚠️ Please enter a news article first.")

    else:

        st.divider()

        st.markdown("## 📊 NEWS ANALYSIS REPORT")

        try:

            with st.spinner("Analyzing your news article..."):

                transformed = vectorizer.transform([news_input])

                prediction = model.predict(transformed)

            # Original model mapping:
            # 1 = Real
            # 0 = Fake

            if prediction[0] == 1:

                result = "REAL NEWS"

                with st.container(border=True):

                    st.success("### ✅ REAL NEWS")

                    st.subheader(
                        "The model classified this article as REAL."
                    )

                    st.write(
                        "The article matches the Real News classification."
                    )

            else:

                result = "FAKE NEWS"

                with st.container(border=True):

                    st.error("### 🚨 FAKE NEWS")

                    st.subheader(
                        "The model classified this article as FAKE."
                    )

                    st.write(
                        "The article matches the Fake News classification."
                    )

            # ----------------------------------
            # CONFIDENCE SCORE
            # ----------------------------------

            if hasattr(model, "predict_proba"):

                probabilities = model.predict_proba(transformed)[0]

                classes = list(model.classes_)

                predicted_class = prediction[0]

                confidence = probabilities[
                    classes.index(predicted_class)
                ] * 100

                st.markdown("### 🎯 Model Confidence")

                st.progress(float(confidence / 100))

                st.write(f"Prediction confidence: **{confidence:.2f}%**")

            # ----------------------------------
            # SAVE HISTORY
            # ----------------------------------

            st.session_state.history.insert(
                0,
                {
                    "article": news_input[:120],
                    "result": result
                }
            )

            st.session_state.history = (
                st.session_state.history[:2]
            )

            st.info(
                "Disclaimer: This is a machine learning prediction, "
                "not independent fact-checking. Always verify information "
                "through reliable news sources."
            )

        except Exception as e:

            st.error(f"Prediction error: {e}")

# ==================================================
# 11. RECENT ANALYSIS HISTORY
# ==================================================

if st.session_state.history:

    st.divider()

    st.markdown("## 📚 Recent Analysis History")

    for index, item in enumerate(st.session_state.history):

        with st.container(border=True):

            st.write(f"**Article {index + 1}**")

            st.write(item["article"])

            if item["result"] == "REAL NEWS":
                st.success("✅ REAL NEWS")
            else:
                st.error("🚨 FAKE NEWS")

# ==================================================
# 12. FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
    """,
    unsafe_allow_html=True
)

st.title("📰 NEWS :blue[CHECK]")

st.caption("THINK BEFORE YOU SHARE. VERIFY BEFORE YOU TRUST.")

st.caption(
    "Fake News Detection System | Powered by Machine Learning & NLP"
)

st.caption("© 2026 NewsCheck. All Rights Reserved.")
