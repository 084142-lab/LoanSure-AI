def calculate_risk_score(
    age,
    employment_type,
    employment_tenure,
    monthly_income,
    existing_emi,
    credit_score,
    previous_default,
    loan_amount,
    loan_tenure
):
    """
    Transparent 100-point loan risk scoring system.

    Academic prototype only.
    This is NOT a real-world lending decision system.

    Maximum score = 100
    """

    score = 0

    positive_drivers = []
    negative_drivers = []

    # ============================================================
    # 1. CREDIT SCORE - 30 POINTS
    # ============================================================

    if credit_score >= 750:
        score += 30
        positive_drivers.append(
            "Excellent credit score (750+)"
        )

    elif credit_score >= 700:
        score += 25
        positive_drivers.append(
            "Good credit score (700–749)"
        )

    elif credit_score >= 650:
        score += 18
        positive_drivers.append(
            "Moderate credit score (650–699)"
        )

    elif credit_score >= 600:
        score += 10
        negative_drivers.append(
            "Relatively low credit score (600–649)"
        )

    else:
        score += 0
        negative_drivers.append(
            "Very low credit score (below 600)"
        )

    # ============================================================
    # 2. DEBT-TO-INCOME RATIO - 25 POINTS
    # ============================================================

    if monthly_income > 0:
        dti = (existing_emi / monthly_income) * 100
    else:
        dti = 100

    if dti <= 20:
        score += 25
        positive_drivers.append(
            f"Low debt-to-income ratio ({dti:.1f}%)"
        )

    elif dti <= 35:
        score += 20
        positive_drivers.append(
            f"Manageable debt-to-income ratio ({dti:.1f}%)"
        )

    elif dti <= 50:
        score += 12
        negative_drivers.append(
            f"Moderately high debt-to-income ratio ({dti:.1f}%)"
        )

    else:
        score += 0
        negative_drivers.append(
            f"High debt-to-income ratio ({dti:.1f}%)"
        )

    # ============================================================
    # 3. MONTHLY INCOME - 15 POINTS
    # ============================================================

    if monthly_income >= 100000:
        score += 15
        positive_drivers.append(
            "Strong monthly income"
        )

    elif monthly_income >= 50000:
        score += 12
        positive_drivers.append(
            "Healthy monthly income"
        )

    elif monthly_income >= 30000:
        score += 8
        positive_drivers.append(
            "Moderate monthly income"
        )

    else:
        score += 4
        negative_drivers.append(
            "Relatively low monthly income"
        )

    # ============================================================
    # 4. EMPLOYMENT STABILITY - 15 POINTS
    # ============================================================

    if employment_tenure >= 5:
        score += 15
        positive_drivers.append(
            "Strong employment stability (5+ years)"
        )

    elif employment_tenure >= 3:
        score += 12
        positive_drivers.append(
            "Good employment stability (3–5 years)"
        )

    elif employment_tenure >= 1:
        score += 8
        positive_drivers.append(
            "Moderate employment stability (1–3 years)"
        )

    else:
        score += 3
        negative_drivers.append(
            "Limited employment history (less than 1 year)"
        )

    # ============================================================
    # 5. PREVIOUS DEFAULT - 15 POINTS
    # ============================================================

    if previous_default == "No":
        score += 15
        positive_drivers.append(
            "No previous loan default"
        )

    else:
        score += 0
        negative_drivers.append(
            "Previous loan default reported"
        )

    # ============================================================
    # FINAL SCORE
    # ============================================================

    # Safety: keep score within 0–100
    score = max(0, min(100, score))

    # ============================================================
    # LOAN-TO-INCOME RATIO
    # ============================================================

    if monthly_income > 0:
        annual_income = monthly_income * 12
        loan_to_income = loan_amount / annual_income
    else:
        loan_to_income = 0

    # ============================================================
    # RISK LEVEL AND DECISION
    # ============================================================

    if score >= 80:
        risk_level = "Low Risk"
        decision = "PRELIMINARY APPROVE"

    elif score >= 60:
        risk_level = "Medium Risk"
        decision = "REFER FOR REVIEW"

    else:
        risk_level = "High Risk"
        decision = "PRELIMINARY REJECT"

    # ============================================================
    # RETURN RESULTS
    # ============================================================

    return {
        "score": score,
        "risk_level": risk_level,
        "decision": decision,
        "dti": dti,
        "loan_to_income": loan_to_income,
        "positive_drivers": positive_drivers,
        "negative_drivers": negative_drivers
    }