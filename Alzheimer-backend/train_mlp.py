
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent

data = np.load(BASE_DIR / "features.npz")
X, y = data["X"], data["y"]

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

X_train, y_train = X[train_idx], y[train_idx]
X_val, y_val = X[val_idx], y[val_idx]
X_test, y_test = X[test_idx], y[test_idx]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("mlp", MLPClassifier(
        hidden_layer_sizes=(256, 64),
        max_iter=100,
        early_stopping=True,
        random_state=42,
        verbose=True,
    )),
])

print("Training MLP...")
model.fit(X_train, y_train)

val_pred = model.predict(X_val)
print("\nValidation accuracy:", accuracy_score(y_val, val_pred))

test_pred = model.predict(X_test)
print("\nTest accuracy:", accuracy_score(y_test, test_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, test_pred))
print(classification_report(
    y_test,
    test_pred,
    target_names=["Non-Alzheimer's", "Alzheimer's"]
))

joblib.dump(model, BASE_DIR / "mlp_resnet50.joblib")
print("\nSaved: mlp_resnet50.joblib")