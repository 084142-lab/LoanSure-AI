import streamlit as st
from groq import Groq


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

MODEL_NAME = "openai/gpt-oss-20b"


# ---------------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------------

def get_groq_client():
    """
    Create a Groq client using the API key stored
    securely in Streamlit secrets.
    """

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

    if not api_key:
        return None

    try:
        return Groq(api_key=api_key)
    except Exception:
        return None


# ---------------------------------------------------------
# LOCAL FALLBACK CHATBOT
# ---------------------------------------------------------

def fallback_response(question, assessment):
    """
    Local fallback assistant.

    This ensures the chatbot still works if the
    Groq API is unavailable.
    """

    question = question.strip().lower()

    score = assessment.get("score", 0)
    risk_level = assessment.get("risk_level", "Unknown")
    decision = assessment.get("decision", "Unknown")
    ml_prediction = assessment.get("ml_prediction", "Unknown")
    ml_confidence = assessment.get("ml_confidence", 0)
    dti = assessment.get("dti", 0)
    loan_to_income = assessment.get("loan_to_income", 0)

    positive_drivers = assessment.get("positive_drivers", [])
    negative_drivers = assessment.get("negative_drivers", [])

    if not question:
        return "Please enter a question about the loan assessment."

    if "score" in question:
        return (
            f"The explainable risk score is {score}/100. "
            "A higher score indicates a stronger profile "
            "under this academic scoring system."
        )

    if "risk" in question:
        return (
            f"The explainable assessment is {risk_level}. "
            f"The machine-learning model predicts "
            f"{ml_prediction} with approximately "
            f"{ml_confidence:.1f}% model confidence."
        )

    if "dti" in question or "debt" in question:
        return (
            f"The debt-to-income ratio is {dti:.1f}%. "
            "It represents the proportion of monthly income "
            "committed to existing EMI obligations."
        )

    if "loan to income" in question or "loan-to-income" in question:
        return (
            f"The loan-to-income ratio is approximately "
            f"{loan_to_income:.2f}x."
        )

    if "decision" in question or "approve" in question:
        return (
            f"The current preliminary decision is {decision}. "
            "This is an academic prototype result and is "
            "not a guarantee of actual loan approval."
        )

    if "positive" in question or "strength" in question:

        if positive_drivers:
            return (
                "The main positive factors are: "
                + "; ".join(positive_drivers)
                + "."
            )

        return "No major positive factors were identified."

    if (
        "negative" in question
        or "weakness" in question
        or "problem" in question
        or "concern" in question
    ):

        if negative_drivers:
            return (
                "The main factors that negatively affected "
                "the score are: "
                + "; ".join(negative_drivers)
                + "."
            )

        return "No major negative factors were identified."

    if (
        "model" in question
        or "machine learning" in question
        or "ml" in question
        or "prediction" in question
    ):
        return (
            f"The embedded Random Forest model predicts "
            f"{ml_prediction} with approximately "
            f"{ml_confidence:.1f}% model confidence. "
            "The model was trained using synthetic academic data."
        )

    if "credit score" in question or "cibil" in question:
        return (
            "Credit score is one of the important factors "
            "used by the explainable scoring system. "
            "Higher credit scores contribute more points."
        )

    if "why" in question or "explain" in question:

        response = (
            f"The applicant has an explainable score of "
            f"{score}/100 and is classified as {risk_level}. "
        )

        if positive_drivers:
            response += (
                "Positive factors include "
                + "; ".join(positive_drivers)
                + ". "
            )

        if negative_drivers:
            response += (
                "Factors reducing the score include "
                + "; ".join(negative_drivers)
                + "."
            )

        return response

    return (
        "I can explain the loan assessment, risk score, "
        "ML prediction, DTI, loan-to-income ratio, "
        "positive factors, negative factors, and "
        "preliminary decision."
    )


# ---------------------------------------------------------
# GROQ AI RESPONSE
# ---------------------------------------------------------

def ask_groq(question, assessment):
    """
    Ask Groq's generative AI model about the current
    loan assessment.

    Returns:
        response_text, used_groq
    """

    client = get_groq_client()

    if client is None:
        return fallback_response(question, assessment), False

    score = assessment.get("score", 0)
    risk_level = assessment.get("risk_level", "Unknown")
    decision = assessment.get("decision", "Unknown")
    ml_prediction = assessment.get("ml_prediction", "Unknown")
    ml_confidence = assessment.get("ml_confidence", 0)
    dti = assessment.get("dti", 0)
    loan_to_income = assessment.get("loan_to_income", 0)

    positive_drivers = assessment.get("positive_drivers", [])
    negative_drivers = assessment.get("negative_drivers", [])

    system_prompt = """
You are LoanSure AI, a conversational assistant inside
an academic loan-risk assessment application.

Your role is to explain the assessment clearly.

Rules:

1. Do not make a final real-world lending decision.
2. Do not claim that loan approval is guaranteed.
3. Do not invent applicant information.
4. Use only the assessment information provided.
5. Explain financial concepts in simple language.
6. Clearly distinguish the explainable score from the
   machine-learning prediction.
7. The Random Forest model was trained on synthetic
   academic data.
8. Do not provide financial, legal, or investment advice.
9. Do not mention or reveal API keys.
10. If the user asks something unrelated to the assessment,
    politely explain that you are focused on the loan assessment.
11. Keep responses concise and professional.
"""

    assessment_context = f"""
CURRENT ASSESSMENT:

Explainable Risk Score: {score}/100
Risk Level: {risk_level}
Preliminary Decision: {decision}

Machine-Learning Prediction: {ml_prediction}
ML Confidence: {ml_confidence:.1f}%

Debt-to-Income Ratio: {dti:.1f}%
Loan-to-Income Ratio: {loan_to_income:.2f}x

Positive Factors:
{positive_drivers}

Negative Factors:
{negative_drivers}
"""

    user_prompt = f"""
{assessment_context}

USER QUESTION:
{question}

Answer the user's question using the assessment above.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.3,
            max_tokens=1024
        )

        answer = response.choices[0].message.content

        if answer and answer.strip():
            return answer.strip(), True

        return fallback_response(question, assessment), False

    except Exception:
        return fallback_response(question, assessment), False


# ---------------------------------------------------------
# MAIN FUNCTION USED BY STREAMLIT APP
# ---------------------------------------------------------

def get_chatbot_response(question, assessment):
    """
    Main chatbot function used by app.py.
    """

    response, used_groq = ask_groq(
        question,
        assessment
    )

    return response, used_groq
