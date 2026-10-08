import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

DATASET_FILE = "loan_training_data.csv"
MODEL_FILE = "loan_risk_model.joblib"

df = pd.read_csv(DATASET_FILE)

print("Dataset loaded successfully.")
print(f"Total records: {len(df)}")
print()


# ============================================================
# 2. SELECT FEATURES AND TARGET
# ============================================================

features = [
    "age",
    "employment_type",
    "employment_tenure",
    "monthly_income",
    "existing_emi",
    "credit_score",
    "previous_default",
    "loan_amount",
    "loan_tenure",
    "dti",
    "loan_to_income"
]

target = "risk_category"

X = df[features]
y = df[target]


# ============================================================
# 3. DEFINE FEATURE TYPES
# ============================================================

categorical_features = [
    "employment_type",
    "previous_default"
]

numeric_features = [
    "age",
    "employment_tenure",
    "monthly_income",
    "existing_emi",
    "credit_score",
    "loan_amount",
    "loan_tenure",
    "dti",
    "loan_to_income"
]


# ============================================================
# 4. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# ============================================================
# 5. RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# 6. CREATE ML PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ============================================================
# 7. SPLIT DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print()


# ============================================================
# 8. TRAIN MODEL
# ============================================================

print("Training Random Forest model...")

pipeline.fit(X_train, y_train)

print("Model training completed.")
print()


# ============================================================
# 9. MAKE PREDICTIONS
# ============================================================

y_pred = pipeline.predict(X_test)


# ============================================================
# 10. MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


print("=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy :  {accuracy:.4f}")
print(f"Precision:  {precision:.4f}")
print(f"Recall   :  {recall:.4f}")
print(f"F1 Score :  {f1:.4f}")

print()
print("Classification Report:")
print(classification_report(y_test, y_pred))

print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================================
# 11. SAVE MODEL
# ============================================================

joblib.dump(
    pipeline,
    MODEL_FILE
)

print()
print("=" * 60)
print(f"Model saved successfully as: {MODEL_FILE}")
print("=" * 60)