import random
import pandas as pd

random.seed(42)

NUMBER_OF_APPLICANTS = 5000


def calculate_risk_label(
    credit_score,
    dti,
    employment_tenure,
    previous_default,
    monthly_income,
    loan_to_income
):
    """
    Generate a training label using transparent financial rules.

    This creates synthetic academic training data.
    It does NOT represent a real bank's lending policy.
    """

    risk_points = 0

    # Credit score
    if credit_score >= 750:
        risk_points += 0
    elif credit_score >= 700:
        risk_points += 1
    elif credit_score >= 650:
        risk_points += 2
    elif credit_score >= 600:
        risk_points += 3
    else:
        risk_points += 4

    # Debt-to-income ratio
    if dti <= 20:
        risk_points += 0
    elif dti <= 35:
        risk_points += 1
    elif dti <= 50:
        risk_points += 2
    else:
        risk_points += 4

    # Employment stability
    if employment_tenure >= 5:
        risk_points += 0
    elif employment_tenure >= 3:
        risk_points += 1
    elif employment_tenure >= 1:
        risk_points += 2
    else:
        risk_points += 3

    # Previous default
    if previous_default == "Yes":
        risk_points += 4

    # Monthly income
    if monthly_income >= 100000:
        risk_points += 0
    elif monthly_income >= 50000:
        risk_points += 1
    elif monthly_income >= 30000:
        risk_points += 2
    else:
        risk_points += 3

    # Loan-to-income ratio
    if loan_to_income <= 2:
        risk_points += 0
    elif loan_to_income <= 4:
        risk_points += 1
    elif loan_to_income <= 6:
        risk_points += 2
    else:
        risk_points += 3

    # Convert points into risk category
    if risk_points <= 5:
        return "Low Risk"
    elif risk_points <= 10:
        return "Medium Risk"
    else:
        return "High Risk"


rows = []

for _ in range(NUMBER_OF_APPLICANTS):

    age = random.randint(21, 65)

    employment_type = random.choice(
        ["Salaried", "Self-Employed", "Business Owner"]
    )

    employment_tenure = round(
        random.uniform(0.5, min(20, max(1, age - 18))),
        1
    )

    monthly_income = random.randint(20000, 200000)

    # Existing EMI is generated as a percentage of income
    emi_percentage = random.uniform(0.05, 0.70)
    existing_emi = round(monthly_income * emi_percentage)

    credit_score = random.randint(500, 850)

    previous_default = random.choices(
        ["No", "Yes"],
        weights=[85, 15],
        k=1
    )[0]

    loan_amount = random.randint(100000, 3000000)

    loan_tenure = random.randint(1, 15)

    # Derived financial features
    dti = (existing_emi / monthly_income) * 100

    annual_income = monthly_income * 12

    loan_to_income = loan_amount / annual_income

    risk_category = calculate_risk_label(
        credit_score=credit_score,
        dti=dti,
        employment_tenure=employment_tenure,
        previous_default=previous_default,
        monthly_income=monthly_income,
        loan_to_income=loan_to_income
    )

    rows.append(
        {
            "age": age,
            "employment_type": employment_type,
            "employment_tenure": employment_tenure,
            "monthly_income": monthly_income,
            "existing_emi": existing_emi,
            "credit_score": credit_score,
            "previous_default": previous_default,
            "loan_amount": loan_amount,
            "loan_tenure": loan_tenure,
            "dti": round(dti, 2),
            "loan_to_income": round(loan_to_income, 3),
            "risk_category": risk_category
        }
    )


dataset = pd.DataFrame(rows)

dataset.to_csv(
    "loan_training_data.csv",
    index=False
)

print("Synthetic dataset created successfully.")
print(f"Number of applicants: {len(dataset)}")
print()
print("Risk category distribution:")
print(dataset["risk_category"].value_counts())
print()
print("First 5 records:")
print(dataset.head())