# LoanSure AI

## AI-Powered Loan Risk Assessment and Explanation System

LoanSure AI is an academic project that combines an explainable rule-based scoring system, a machine-learning model, and a conversational AI assistant to assess loan risk.

The system accepts applicant and loan information, calculates an explainable risk score, classifies the applicant into a risk category, provides a preliminary lending outcome, and allows the user to ask questions about the assessment through an AI chatbot.

---

## 1. Project Objective

The main objective of LoanSure AI is to demonstrate how artificial intelligence and machine learning can support loan-risk assessment in a simple, explainable, and user-friendly application.

The project focuses on:

- Applicant data collection
- Explainable loan-risk scoring
- Machine-learning-based risk classification
- Explanation of factors affecting the score
- Preliminary loan decision support
- Conversational AI assistance
- User-friendly web application deployment

---

## 2. Key Features

### Applicant Assessment

The application collects information such as:

- Age
- Employment type
- Employment tenure
- Monthly income
- Existing EMI
- Credit score
- Previous loan default
- Requested loan amount
- Loan tenure

### Explainable Risk Score

LoanSure AI calculates a score from 0 to 100 using predefined financial and applicant-related rules.

The score considers:

| Factor | Maximum Points |
|---|---:|
| Credit Score | 30 |
| Debt-to-Income Ratio | 25 |
| Monthly Income | 15 |
| Employment Stability | 15 |
| Previous Loan Default | 15 |
| **Total** | **100** |

### Risk Classification

The explainable score is converted into three risk categories:

| Score | Risk Category | Preliminary Outcome |
|---|---|---|
| 80–100 | Low Risk | Preliminary Approve |
| 60–79 | Medium Risk | Refer for Review |
| 0–59 | High Risk | Preliminary Reject |

### Machine Learning Model

The project also includes an embedded Random Forest Classifier.

The machine-learning model uses applicant and financial features to predict:

- Low Risk
- Medium Risk
- High Risk

The application displays the model prediction and its confidence.

### AI Chatbot

LoanSure AI includes a conversational assistant powered by Groq Generative AI.

The chatbot can explain:

- Risk score
- Risk category
- Preliminary decision
- Positive factors
- Negative factors
- Credit score
- Debt-to-income ratio
- Loan-to-income ratio
- Machine-learning prediction

A local fallback assistant is included so that basic explanations remain available if the generative AI service is unavailable.

---

## 3. System Architecture

The application follows a simple modular architecture:

```text
                 Applicant Information
                         |
                         v
                +-------------------+
                |    Streamlit UI   |
                +-------------------+
                         |
              +----------+----------+
              |                     |
              v                     v
    Explainable Scoring       ML Prediction
              |                     |
              v                     v
       Risk Score             Random Forest
              |                     |
              +----------+----------+
                         |
                         v
                Assessment Result
                         |
              +----------+----------+
              |                     |
              v                     v
       Score Explanation       AI Chatbot
                                   |
                            Groq / Local Fallback