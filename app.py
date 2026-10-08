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

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #f5f7ff 0%, #eef2ff 100%);
        border: 1px solid #dfe4ff;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        margin-bottom: 0.3rem;
        font-size: 2.4rem;
    }

    .hero p {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .result-box {
        padding: 1.3rem;
        border-radius: 15px;
        border: 1px solid #ddd;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .info-box {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background-color: #f8f9fa;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
    }

    .small-note {
        font-size: 0.85rem;
        color: #666;
    }

    .footer {
        text-align: center;
        color: #777;
        font-size: 0.82rem;
        padding: 2rem 0 1rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🏦 LoanSure AI</h1>
        <p>
            Intelligent Loan Risk Assessment & AI Explanation System
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if model is not None:
    st.success("🟢 AI Risk Model: Loaded and Ready")
else:
    st.warning(
        "🟡 Risk model could not be loaded. "
        "The explainable scoring system is still available."
    )


st.markdown(
    """
    <div class="info-box">
        <b>How it works:</b>
        Enter the applicant's financial information below.
        LoanSure AI evaluates the profile using an explainable
        risk-scoring system and an embedded machine-learning model.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# APPLICANT INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">👤 Applicant Information</div>',
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


# ============================================================
# VALIDATION
# ============================================================

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


# ============================================================
# ASSESS BUTTON
# ============================================================

st.markdown("---")

assess_button = st.button(
    "🔍 Assess Loan Risk",
    type="primary",
    use_container_width=True
)


if assess_button:

    if validation_errors:

        for error in validation_errors:
            st.error(error)

        st.stop()

    # --------------------------------------------------------
    # EXPLAINABLE SCORE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # MACHINE LEARNING PREDICTION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # STORE ASSESSMENT
    # --------------------------------------------------------

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


# ============================================================
# DISPLAY ASSESSMENT
# ============================================================

if st.session_state.assessment is not None:

    assessment = st.session_state.assessment

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Your Loan Assessment</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # MAIN RESULTS
    # --------------------------------------------------------

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric(
            "Risk Score",
            f'{assessment["score"]}/100'
        )

    with result_col2:
        st.metric(
            "Risk Level",
            assessment["risk_level"]
        )

    with result_col3:
        st.metric(
            "Preliminary Decision",
            assessment["decision"]
        )


    # --------------------------------------------------------
    # SCORE PROGRESS
    # --------------------------------------------------------

    st.progress(
        assessment["score"] / 100
    )


    # --------------------------------------------------------
    # CUSTOMER-FACING EXPLANATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">💡 Why did I get this result?</div>',
        unsafe_allow_html=True
    )

    explanation_text = (
        f"Your explainable risk score is "
        f"**{assessment['score']}/100**, which places the "
        f"application in the **{assessment['risk_level']}** category."
    )

    st.info(explanation_text)


    # --------------------------------------------------------
    # POSITIVE FACTORS
    # --------------------------------------------------------

    if assessment["positive_drivers"]:

        st.markdown("### ✅ Factors supporting the application")

        for driver in assessment["positive_drivers"]:
            st.write(f"• {driver}")


    # --------------------------------------------------------
    # NEGATIVE FACTORS
    # --------------------------------------------------------

    if assessment["negative_drivers"]:

        st.markdown("### ⚠️ Factors that reduced the score")

        for driver in assessment["negative_drivers"]:
            st.write(f"• {driver}")


    # --------------------------------------------------------
    # PRELIMINARY DECISION
    # --------------------------------------------------------

    if assessment["decision"] == "PRELIMINARY APPROVE":

        st.success(
            "🟢 Preliminary result: The application shows a "
            "relatively strong risk profile."
        )

    elif assessment["decision"] == "REFER FOR REVIEW":

        st.warning(
            "🟡 Preliminary result: The application should be "
            "reviewed further before a final decision."
        )

    else:

        st.error(
            "🔴 Preliminary result: The application shows a "
            "higher-risk profile under this assessment system."
        )


    # ========================================================
    # AI CHATBOT
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🤖 Ask LoanSure AI</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask questions about your assessment, score, risk factors, "
        "or financial ratios."
    )

    user_question = st.text_input(
        "Your question",
        placeholder="Why is my risk score this high?"
    )

    if st.button(
        "💬 Ask LoanSure AI",
        use_container_width=True
    ):

        if user_question.strip():

            with st.spinner("LoanSure AI is thinking..."):

                response, used_groq = get_chatbot_response(
                    user_question,
                    assessment
                )

            if used_groq:
                st.caption("🟢 Powered by Groq Generative AI")
            else:
                st.caption("🟡 Local fallback assistant")

            st.info(response)

        else:

            st.warning("Please enter a question first.")


    # ========================================================
    # ADVANCED TECHNICAL DETAILS
    # ========================================================

    st.markdown("---")

    with st.expander("🔬 Advanced Technical Details"):

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