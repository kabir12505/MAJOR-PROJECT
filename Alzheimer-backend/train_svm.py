
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline
import joblib

BASE_DIR = Path(__file__).resolve().parent

# Load extracted features and labels
data = np.load(BASE_DIR / "features.npz")
X = data["X"]
y = data["y"]

# Recreate the same split using metadata row order
df = pd.read_csv(BASE_DIR / "metadata.csv")

train_idx, temp_idx = train_test_split(
    np.arange(len(df)),
    test_size=0.30,
    random_state=42,
    stratify=df["label"],
)

val_idx, test_idx = train_test_split(
    temp_idx,
    test_size=0.50,
    random_state=42,
    stratify=df["label"].iloc[temp_idx],
)

# Train on training data only
X_train, y_train = X[train_idx], y[train_idx]
X_val, y_val = X[val_idx], y[val_idx]
X_test, y_test = X[test_idx], y[test_idx]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        kernel="rbf",
        probability=True,
        class_weight="balanced",
        random_state=42,
    )),
])

print("Training SVM...")
model.fit(X_train, y_train)

# Validation evaluation
val_pred = model.predict(X_val)
print("\nValidation accuracy:", accuracy_score(y_val, val_pred))
print(classification_report(y_val, val_pred, target_names=[
    "Non-Alzheimer's", "Alzheimer's"
]))

# Final test evaluation
test_pred = model.predict(X_test)
print("\nTest accuracy:", accuracy_score(y_test, test_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, test_pred))
print(classification_report(y_test, test_pred, target_names=[
    "Non-Alzheimer's", "Alzheimer's"
]))

# Save trained model
joblib.dump(model, BASE_DIR / "svm_resnet50.joblib")
print("\nSaved model: svm_resnet50.joblib")
