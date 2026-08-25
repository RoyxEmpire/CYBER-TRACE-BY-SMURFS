from pathlib import Path
import json

import pandas as pd
import numpy as np
import shap

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


# ===== STEP 1: File paths =====

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "TEST DATA GENERATOR"
    / "synthetic_complaints.csv"
)

MODEL_PATH = BASE_DIR / "withdrawal_zone_model.json"
ENCODER_PATH = BASE_DIR / "zone_label_encoder.json"


# ===== STEP 2: Load data and prepare features =====

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at:\n{DATA_PATH}\n"
        "Run data_generate.py first."
    )

df = pd.read_csv(DATA_PATH)

print("Loaded data from:")
print(DATA_PATH)

print("\nLoaded data:")
print(df.head())
print(f"\nTotal complaints: {len(df)}")

features = [
    "hop_count",
    "amount",
    "delay_minutes",
    "account_age_days",
    "kyc_verified",
    "num_source_accounts",
    "device_change_count",
    "ip_zone_mismatch",
    "round_amount_flag",
    "common_final_account"
]

target = "withdrawal_zone"

required_columns = features + [target]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}\n"
        f"Available columns: {df.columns.tolist()}"
    )

df = df.dropna(subset=required_columns)

X = df[features]
y = df[target].astype(str)

print("\nFeature data types:")
print(X.dtypes)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("\nZone name to number mapping:")
for zone, number in zip(
    label_encoder.classes_,
    range(len(label_encoder.classes_))
):
    print(f"{zone} -> {number}")


# ===== STEP 3: Split data =====

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print(f"\nTraining data size: {len(X_train)}")
print(f"Testing data size: {len(X_test)}")


# ===== STEP 4: Train the model =====

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    objective="multi:softprob",
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("\nModel training completed!")


# ===== STEP 5: Evaluate the model =====

predictions = model.predict(X_test).astype(int)

accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=range(len(label_encoder.classes_)),
        target_names=label_encoder.classes_,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))


# ===== STEP 6: Save model and encoder =====

model.save_model(str(MODEL_PATH))

with open(ENCODER_PATH, "w", encoding="utf-8") as file:
    json.dump(
        {
            "classes": label_encoder.classes_.tolist()
        },
        file,
        indent=4
    )

print(f"\nModel saved as:")
print(MODEL_PATH)

print("\nLabel encoder saved as:")
print(ENCODER_PATH)


# ===== STEP 7: Top-3 zone prediction =====

probabilities = model.predict_proba(X_test)

sample_index = 0
sample_probs = probabilities[sample_index]

zone_names = label_encoder.classes_

top_3_indices = np.argsort(sample_probs)[::-1][:3]

print(f"\n--- Prediction for Complaint #{sample_index} ---")
print("Top 3 Likely Withdrawal Zones:")

for rank, index in enumerate(top_3_indices, start=1):
    zone = zone_names[index]
    confidence = sample_probs[index] * 100

    print(
        f"{rank}. Zone {zone} "
        f"- Confidence: {confidence:.2f}%"
    )


# ===== STEP 8: SHAP explainability =====

try:
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(
        X_test.iloc[[sample_index]]
    )

    print(
        f"\n--- Why did we predict this for Complaint "
        f"#{sample_index}? ---"
    )

    print("Feature values for this complaint:")
    print(X_test.iloc[sample_index])

    print("\nSHAP explanation generated successfully.")

except Exception as error:
    print("\nSHAP explanation could not be generated:")
    print(error)