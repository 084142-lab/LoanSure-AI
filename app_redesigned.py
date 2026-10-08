import streamlit as st
import pandas as pd
import joblib

from scoring import calculate_risk_score
from chatbot import get_chatbot_response


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LoanSure AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #F2F5F4;
        --shell: #FFFFFF;
        --shell-border: #DDE6E2;
        --surface-2: #F3F6F5;
        --ink: #12211D;
        --ink-muted: #5E6F6B;

        --accent: #0F4C43;
        --accent-strong: #0B3B34;
        --accent-ink: #FFFFFF;
        --gold: #B8893B;

        --low: #1F7A4D;
        --low-tint: #E4F2E9;
        --medium: #A6760A;
        --medium-tint: #FBF0DC;
        --high: #B3261E;
        --high-tint: #FBE6E4;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp {
        background: var(--bg);
    }

    .main {
        padding-top: 0.6rem;
    }

    /* -------------------- TOP BAR -------------------- */

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.4rem 0.2rem 1.3rem 0.2rem;
        flex-wrap: wrap;
        gap: 0.6rem;
    }

    .topbar .brand {
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--ink);
    }

    .topbar .brand .crumb-sep {
        color: var(--ink-muted);
        font-weight: 400;
        margin: 0 0.35rem;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        font-size: 0.83rem;
        font-weight: 500;
        border: 1px solid var(--shell-border);
        background: var(--shell);
        color: var(--ink-muted);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .status-dot.ok { background: var(--low); }
    .status-dot.warn { background: var(--gold); }

    /* -------------------- SHELL PANELS -------------------- */

    .st-key-left_shell, .st-key-right_shell {
        background: var(--shell);
        border: 1px solid var(--shell-border);
        border-radius: 18px;
        padding: 1.5rem 1.6rem 1.7rem 1.6rem;
    }

    .st-key-right_shell {
        position: sticky;
        top: 1rem;
    }

    .panel-header h2 {
        font-size: 1.32rem;
        font-weight: 700;
        color: var(--ink);
        margin: 0 0 0.5rem 0;
    }

    .panel-header .chip-row {
        display: flex;
        gap: 0.6rem;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .panel-sub {
        color: var(--ink-muted);
        font-size: 0.88rem;
        margin: 0 0 1rem 0;
        max-width: 56ch;
    }

    /* -------------------- PAPER CARD (FORM + RESULTS) -------------------- */

    .st-key-paper_card {
        background: #FFFFFF;
        border: 1px solid var(--shell-border);
        border-radius: 14px;
        padding: 1.5rem 1.6rem 1.7rem 1.6rem;
    }

    .form-section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--ink);
        margin: 0 0 0.9rem 0;
    }

    /* -------------------- CHIPS -------------------- */

    .chip {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 600;
        width: fit-content;
        text-transform: capitalize;
    }

    .chip.low { background: var(--low-tint); color: var(--low); }
    .chip.medium { background: var(--medium-tint); color: var(--medium); }
    .chip.high { background: var(--high-tint); color: var(--high); }
    .chip.neutral { background: var(--surface-2); color: var(--ink-muted); border: 1px solid var(--shell-border); }

    /* -------------------- SCORE CARD -------------------- */

    .score-card {
        display: flex;
        align-items: center;
        gap: 1.8rem;
        flex-wrap: wrap;
        padding: 1.4rem 1.5rem;
        border-radius: 14px;
        background: var(--surface-2);
        border: 1px solid var(--shell-border);
        margin-bottom: 1.1rem;
    }

    .score-number {
        font-weight: 800;
        font-size: 3.1rem;
        line-height: 1;
        color: var(--ink);
    }

    .score-number span {
        font-size: 1.2rem;
        font-weight: 500;
        color: var(--ink-muted);
    }

    .score-meta {
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }

    .score-bar-track {
        width: 100%;
        height: 8px;
        border-radius: 999px;
        background: var(--shell-border);
        margin-top: 1.1rem;
        overflow: hidden;
    }

    .score-bar-fill {
        height: 100%;
        border-radius: 999px;
    }

    .score-bar-fill.low { background: var(--low); }
    .score-bar-fill.medium { background: var(--medium); }
    .score-bar-fill.high { background: var(--high); }

    /* -------------------- ASSISTANT PANEL -------------------- */

    .context-card {
        background: var(--surface-2);
        border: 1px solid var(--shell-border);
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 1rem;
    }

    .context-card h4 {
        margin: 0 0 0.25rem 0;
        font-size: 1rem;
        font-weight: 600;
        color: var(--ink);
    }

    .context-card p {
        margin: 0;
        font-size: 0.85rem;
        color: var(--ink-muted);
    }

    .st-key-chat_transcript {
        background: transparent;
    }

    .chat-hint {
        color: var(--ink-muted);
        font-size: 0.89rem;
        padding: 0.4rem 0.1rem 1rem 0.1rem;
        line-height: 1.55;
    }

    .msg-question {
        color: var(--ink-muted);
        font-size: 0.85rem;
        margin: 0.9rem 0 0.4rem 0;
    }

    div[class*="st-key-msg_"] {
        background: var(--surface-2);
        border: 1px solid var(--shell-border);
        border-radius: 12px;
        padding: 0.95rem 1.05rem;
        color: var(--ink);
        font-size: 0.92rem;
        line-height: 1.58;
        margin-bottom: 0.6rem;
    }

    .msg-source {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
    }

    .msg-source.groq { color: var(--low); background: var(--low-tint); }
    .msg-source.fallback { color: var(--gold); background: var(--medium-tint); }

    .chat-disclaimer {
        text-align: center;
        color: var(--ink-muted);
        font-size: 0.74rem;
        margin-top: 0.7rem;
    }

    /* Pill input + send button for the chat form */

    .st-key-chat_form_wrap div[data-baseweb="input"] {
        background: var(--surface-2) !important;
        border-radius: 999px !important;
        border: 1px solid var(--shell-border) !important;
    }

    .st-key-chat_form_wrap div[data-baseweb="input"] input {
        color: var(--ink) !important;
    }

    .st-key-chat_form_wrap input::placeholder {
        color: var(--ink-muted) !important;
        opacity: 1 !important;
    }

    .st-key-chat_form_wrap .stButton button,
    .st-key-chat_form_wrap button {
        background: var(--accent) !important;
        color: var(--accent-ink) !important;
        border-radius: 999px !important;
        border: none !important;
        font-weight: 700 !important;
        width: 100% !important;
    }

    .st-key-chat_form_wrap .stButton button:hover,
    .st-key-chat_form_wrap button:hover {
        background: var(--accent-strong) !important;
    }

    /* Primary action button (Assess Loan Risk) */

    button[kind="primary"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
        color: var(--accent-ink) !important;
        font-weight: 700 !important;
    }

    button[kind="primary"]:hover {
        background: var(--accent-strong) !important;
        border-color: var(--accent-strong) !important;
    }

    /* -------------------- FOOTER -------------------- */

    .footer {
        text-align: center;
        color: var(--ink-muted);
        font-size: 0.82rem;
        padding: 2rem 0 1rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

def risk_tier(risk_level):
    """Map a risk-level label to a CSS tier class (low / medium / high)."""

    if risk_level == "Low Risk":
        return "low"

    if risk_level == "Medium Risk":
        return "medium"

    return "high"


# ============================================================
# LOAD ML MODEL
# ============================================================

@st.cache_resource
def load_model():
    try:
        return joblib.load("loan_risk_model.joblib")
    except Exception:
        return None


model = load_model()


# ============================================================
# SESSION STATE
# ============================================================

if "assessment" not in st.session_state:
    st.session_state.assessment = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# TOP BAR
# ============================================================

if model is not None:
    model_status_html = (
        '<div class="status-pill ok">'
        '<span class="status-dot ok"></span> AI Risk Model — Loaded and Ready</div>'
    )
else:
    model_status_html = (
        '<div class="status-pill warn">'
        '<span class="status-dot warn"></span> Risk model unavailable — explainable scoring only</div>'
    )

st.markdown(
    f"""
    <div class="topbar">
        <div class="brand">LoanSure AI <span class="crumb-sep">·</span>
            <span style="color: var(--ink-muted); font-weight: 400;">Loan Risk Assessment</span>
        </div>
        {model_status_html}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MAIN LAYOUT — ANALYSIS (LEFT) / ASSISTANT (RIGHT)
# ============================================================

analysis_col, chat_col = st.columns([3, 2], gap="medium")


# ------------------------------------------------------------
# LEFT COLUMN — APPLICANT INFORMATION & ANALYSIS
# ------------------------------------------------------------

with analysis_col:

    with st.container(key="left_shell", border=False):

        if st.session_state.assessment is not None:
            header_tier = risk_tier(st.session_state.assessment["risk_level"])
            header_chip = (
                f'<span class="chip {header_tier}">'
                f'{st.session_state.assessment["risk_level"]}</span>'
            )
        else:
            header_chip = '<span class="chip neutral">Not Assessed</span>'

        st.markdown(
            f"""
            <div class="panel-header">
                <div class="chip-row">{header_chip}</div>
                <h2>Applicant Assessment</h2>
                <p class="panel-sub">
                    Enter the applicant's financial details to generate an
                    explainable risk score and a machine-learning prediction.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(key="paper_card", border=False):

            with st.expander("Application", expanded=(st.session_state.assessment is None)):
                # ====================================================
                # APPLICANT INFORMATION
                # ====================================================

                st.markdown(
                    '<div class="form-section-title">Applicant Information</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    age = st.number_input(
                        "Age",
                        min_value=18,
                        max_value=80,
                        value=30,
                        step=1
                    )

                    employment_type = st.selectbox(
                        "Employment Type",
                        [
                            "Salaried",
                            "Self-Employed",
                            "Business Owner"
                        ]
                    )

                    employment_tenure = st.number_input(
                        "Employment Tenure (years)",
                        min_value=0.0,
                        max_value=50.0,
                        value=3.0,
                        step=0.5
                    )


                with col2:
                    monthly_income = st.number_input(
                        "Monthly Income (₹)",
                        min_value=0.0,
                        value=50000.0,
                        step=5000.0
                    )

                    existing_emi = st.number_input(
                        "Existing Monthly EMI (₹)",
                        min_value=0.0,
                        value=10000.0,
                        step=1000.0
                    )

                    credit_score = st.number_input(
                        "Credit Score",
                        min_value=300,
                        max_value=900,
                        value=700,
                        step=1
                    )


                with col3:
                    previous_default = st.selectbox(
                        "Previous Loan Default",
                        [
                            "No",
                            "Yes"
                        ]
                    )

                    loan_amount = st.number_input(
                        "Requested Loan Amount (₹)",
                        min_value=0.0,
                        value=500000.0,
                        step=50000.0
                    )

                    loan_tenure = st.number_input(
                        "Loan Tenure (years)",
                        min_value=1.0,
                        max_value=30.0,
                        value=5.0,
                        step=1.0
                    )


                # ====================================================
                # VALIDATION
                # ====================================================

                validation_errors = []

                if monthly_income <= 0:
                    validation_errors.append("Monthly income must be greater than zero.")

                if existing_emi > monthly_income:
                    validation_errors.append(
                        "Existing EMI cannot be greater than monthly income."
                    )

                if loan_amount <= 0:
                    validation_errors.append(
                        "Requested loan amount must be greater than zero."
                    )

                if employment_tenure > age:
                    validation_errors.append(
                        "Employment tenure cannot be greater than the applicant's age."
                    )


                # ====================================================
                # ASSESS BUTTON
                # ====================================================

                st.markdown("---")

                assess_button = st.button(
                    "Assess Loan Risk",
                    type="primary",
                    use_container_width=True
                )


                if assess_button:

                    if validation_errors:

                        for error in validation_errors:
                            st.error(error)

                        st.stop()

                    # ------------------------------------------------
                    # EXPLAINABLE SCORE
                    # ------------------------------------------------

                    result = calculate_risk_score(
                        age=age,
                        employment_type=employment_type,
                        employment_tenure=employment_tenure,
                        monthly_income=monthly_income,
                        existing_emi=existing_emi,
                        credit_score=credit_score,
                        previous_default=previous_default,
                        loan_amount=loan_amount,
                        loan_tenure=loan_tenure
                    )

                    # ------------------------------------------------
                    # MACHINE LEARNING PREDICTION
                    # ------------------------------------------------

                    ml_prediction = "Unavailable"
                    ml_confidence = 0.0
                    ml_probabilities = {}

                    if model is not None:

                        applicant_data = pd.DataFrame(
                            [{
                                "age": age,
                                "employment_type": employment_type,
                                "employment_tenure": employment_tenure,
                                "monthly_income": monthly_income,
                                "existing_emi": existing_emi,
                                "credit_score": credit_score,
                                "previous_default": previous_default,
                                "loan_amount": loan_amount,
                                "loan_tenure": loan_tenure,
                                "dti": result["dti"],
                                "loan_to_income": result["loan_to_income"]
                            }]
                        )

                        try:

                            ml_prediction = model.predict(applicant_data)[0]

                            probabilities = model.predict_proba(applicant_data)[0]

                            classes = model.classes_

                            ml_probabilities = dict(
                                zip(classes, probabilities)
                            )

                            ml_confidence = max(probabilities) * 100

                        except Exception as error:

                            ml_prediction = "Unavailable"
                            ml_confidence = 0.0
                            ml_probabilities = {}

                            st.warning(
                                f"Machine-learning prediction could not be generated: {error}"
                            )

                    # ------------------------------------------------
                    # STORE ASSESSMENT
                    # ------------------------------------------------

                    st.session_state.assessment = {
                        **result,
                        "ml_prediction": ml_prediction,
                        "ml_confidence": ml_confidence,
                        "ml_probabilities": ml_probabilities,
                        "age": age,
                        "employment_type": employment_type,
                        "employment_tenure": employment_tenure,
                        "monthly_income": monthly_income,
                        "existing_emi": existing_emi,
                        "credit_score": credit_score,
                        "previous_default": previous_default,
                        "loan_amount": loan_amount,
                        "loan_tenure": loan_tenure
                    }

                    st.session_state.chat_history = []

                    st.rerun()


            # ====================================================
            # DISPLAY ASSESSMENT
            # ====================================================

            if st.session_state.assessment is not None:

                with st.expander("Results", expanded=True):
                    assessment = st.session_state.assessment

                    tier = risk_tier(assessment["risk_level"])

                    st.markdown("---")

                    st.markdown(
                        '<div class="form-section-title">Your Loan Assessment</div>',
                        unsafe_allow_html=True
                    )

                    # ------------------------------------------------
                    # SCORE CARD
                    # ------------------------------------------------

                    st.markdown(
                        f"""
                        <div class="score-card">
                            <div class="score-number">
                                {assessment["score"]}<span>/100</span>
                                <div class="score-bar-track">
                                    <div class="score-bar-fill {tier}" style="width:{assessment['score']}%;"></div>
                                </div>
                            </div>
                            <div class="score-meta">
                                <span class="chip {tier}">{assessment["risk_level"]}</span>
                                <span class="chip {tier}">{assessment["decision"].title()}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ------------------------------------------------
                    # CUSTOMER-FACING EXPLANATION
                    # ------------------------------------------------

                    st.markdown(
                        '<div class="form-section-title">Why did I get this result?</div>',
                        unsafe_allow_html=True
                    )

                    explanation_text = (
                        f"Your explainable risk score is "
                        f"**{assessment['score']}/100**, which places the "
                        f"application in the **{assessment['risk_level']}** category."
                    )

                    st.info(explanation_text)


                    # ------------------------------------------------
                    # POSITIVE FACTORS
                    # ------------------------------------------------

                    if assessment["positive_drivers"]:

                        st.markdown("### Factors supporting the application")

                        for driver in assessment["positive_drivers"]:
                            st.write(f"• {driver}")


                    # ------------------------------------------------
                    # NEGATIVE FACTORS
                    # ------------------------------------------------

                    if assessment["negative_drivers"]:

                        st.markdown("### Factors that reduced the score")

                        for driver in assessment["negative_drivers"]:
                            st.write(f"• {driver}")


                    # ------------------------------------------------
                    # PRELIMINARY DECISION
                    # ------------------------------------------------

                    if assessment["decision"] == "PRELIMINARY APPROVE":

                        st.success(
                            "Preliminary result: The application shows a "
                            "relatively strong risk profile."
                        )

                    elif assessment["decision"] == "REFER FOR REVIEW":

                        st.warning(
                            "Preliminary result: The application should be "
                            "reviewed further before a final decision."
                        )

                    else:

                        st.error(
                            "Preliminary result: The application shows a "
                            "higher-risk profile under this assessment system."
                        )


                    # ====================================================
                    # ADVANCED TECHNICAL DETAILS
                    # ====================================================

                    st.markdown("---")

                    with st.expander("Advanced Technical Details"):

                        st.markdown(
                            """
                            This section is intended for academic demonstration
                            and technical evaluation of the project.
                            """
                        )

                        st.markdown("### Machine-Learning Prediction")

                        technical_col1, technical_col2 = st.columns(2)

                        with technical_col1:

                            st.metric(
                                "ML Prediction",
                                assessment["ml_prediction"]
                            )

                        with technical_col2:

                            st.metric(
                                "ML Confidence",
                                f'{assessment["ml_confidence"]:.1f}%'
                            )


                        st.markdown("### Financial Ratios")

                        ratio_col1, ratio_col2 = st.columns(2)

                        with ratio_col1:

                            st.metric(
                                "Debt-to-Income Ratio",
                                f'{assessment["dti"]:.1f}%'
                            )

                        with ratio_col2:

                            st.metric(
                                "Loan-to-Income Ratio",
                                f'{assessment["loan_to_income"]:.2f}x'
                            )


                        st.markdown("### ML Probability Distribution")

                        if assessment["ml_probabilities"]:

                            probability_data = pd.DataFrame(
                                {
                                    "Risk Category": list(
                                        assessment["ml_probabilities"].keys()
                                    ),
                                    "Probability": [
                                        f"{value * 100:.2f}%"
                                        for value in assessment["ml_probabilities"].values()
                                    ]
                                }
                            )

                            st.dataframe(
                                probability_data,
                                use_container_width=True,
                                hide_index=True
                            )

                        else:

                            st.write("ML probability information is unavailable.")


                        st.markdown("### Explainable Scoring Methodology")

                        st.write(
                            """
                            The explainable score is calculated on a 100-point scale.

                            • Credit Score: up to 30 points
                            • Debt-to-Income Ratio: up to 25 points
                            • Monthly Income: up to 15 points
                            • Employment Stability: up to 15 points
                            • Previous Loan Default: up to 15 points
                            """
                        )


                        st.markdown("### Risk Classification")

                        classification_data = pd.DataFrame(
                            {
                                "Score Range": [
                                    "80–100",
                                    "60–79",
                                    "0–59"
                                ],
                                "Risk Category": [
                                    "Low Risk",
                                    "Medium Risk",
                                    "High Risk"
                                ],
                                "Preliminary Outcome": [
                                    "Preliminary Approve",
                                    "Refer for Review",
                                    "Preliminary Reject"
                                ]
                            }
                        )

                        st.dataframe(
                            classification_data,
                            use_container_width=True,
                            hide_index=True
                        )


                        st.markdown("### Machine-Learning Model")

                        st.write(
                            """
                            Model: Random Forest Classifier

                            The model uses applicant financial and demographic
                            features to classify the applicant into a risk category.

                            The training dataset used by this academic prototype
                            is synthetically generated.
                            """
                        )


                        st.markdown("### Applicant Data Used by the Model")

                        technical_applicant_data = pd.DataFrame(
                            {
                                "Feature": [
                                    "Age",
                                    "Employment Type",
                                    "Employment Tenure",
                                    "Monthly Income",
                                    "Existing EMI",
                                    "Credit Score",
                                    "Previous Default",
                                    "Loan Amount",
                                    "Loan Tenure",
                                    "DTI",
                                    "Loan-to-Income"
                                ],
                                "Value": [
                                    assessment["age"],
                                    assessment["employment_type"],
                                    assessment["employment_tenure"],
                                    assessment["monthly_income"],
                                    assessment["existing_emi"],
                                    assessment["credit_score"],
                                    assessment["previous_default"],
                                    assessment["loan_amount"],
                                    assessment["loan_tenure"],
                                    f'{assessment["dti"]:.2f}%',
                                    f'{assessment["loan_to_income"]:.2f}x'
                                ]
                            }
                        )

                        st.dataframe(
                            technical_applicant_data,
                            use_container_width=True,
                            hide_index=True
                        )


# ------------------------------------------------------------
# RIGHT COLUMN — AI ASSISTANT
# ------------------------------------------------------------

with chat_col:

    with st.container(key="right_shell", border=False):

        if st.session_state.assessment is not None:

            assessment = st.session_state.assessment

            context_subtitle = (
                f'{assessment["risk_level"]} · Score {assessment["score"]}/100 · '
                f'{assessment["decision"].title()}'
            )

        else:

            context_subtitle = "No assessment yet — run one on the left to begin."

        st.markdown(
            f"""
            <div class="context-card">
                <h4>Risk Consultation</h4>
                <p>{context_subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(key="chat_transcript", height=360, border=False):

            if not st.session_state.chat_history:

                st.markdown(
                    """
                    <div class="chat-hint">
                        Ask about the risk score, financial ratios, positive
                        and negative factors, or the machine-learning
                        prediction. Responses appear here.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                for turn_index, turn in enumerate(st.session_state.chat_history):

                    source_class = "groq" if turn["used_groq"] else "fallback"
                    source_label = (
                        "Groq Generative AI" if turn["used_groq"]
                        else "Local fallback assistant"
                    )

                    st.markdown(
                        f'<div class="msg-question">You asked: {turn["question"]}</div>',
                        unsafe_allow_html=True
                    )

                    with st.container(key=f"msg_{turn_index}", border=False):

                        st.markdown(
                            f'<span class="msg-source {source_class}">{source_label}</span>',
                            unsafe_allow_html=True
                        )

                        st.markdown(turn["answer"])

        with st.container(key="chat_form_wrap", border=False):

            with st.form(key="chat_form", clear_on_submit=True, border=False):

                input_col, send_col = st.columns([5, 1], gap="small")

                with input_col:
                    user_question = st.text_input(
                        "Your question",
                        placeholder="Ask me anything...",
                        label_visibility="collapsed"
                    )

                with send_col:
                    ask_clicked = st.form_submit_button("➜", use_container_width=True)

                if ask_clicked and user_question.strip():

                    if st.session_state.assessment is None:

                        st.session_state.chat_history.append({
                            "question": user_question.strip(),
                            "answer": (
                                "Please run a loan assessment on the left "
                                "first — I need that data to answer questions."
                            ),
                            "used_groq": False
                        })

                    else:

                        with st.spinner("LoanSure AI is thinking..."):

                            response, used_groq = get_chatbot_response(
                                user_question,
                                st.session_state.assessment
                            )

                        st.session_state.chat_history.append({
                            "question": user_question.strip(),
                            "answer": response,
                            "used_groq": used_groq
                        })

                    st.rerun()

        st.markdown(
            '<div class="chat-disclaimer">'
            'LoanSure AI can make mistakes, so double-check the response.'
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    <b>LoanSure AI</b> — Academic Loan Risk Assessment Prototype

    <br><br>

    This application is designed for educational and demonstration
    purposes. It uses synthetic data and should not be treated as
    a real-world lending decision or financial advice.

    <br>

    A preliminary assessment does not guarantee loan approval.

    </div>
    """,
    unsafe_allow_html=True
)
