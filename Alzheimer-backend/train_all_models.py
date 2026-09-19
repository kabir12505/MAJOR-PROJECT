
from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
import joblib
import torch

from PIL import Image
from torchvision.models import (
    resnet50,
    ResNet50_Weights,
    densenet121,
    DenseNet121_Weights,
    efficientnet_b0,
    EfficientNet_B0_Weights,
)

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif, RFE, SelectFromModel
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BATCH_SIZE = 16
RANDOM_STATE = 42
TOP_K = 256

OUTPUT_DIR = BASE_DIR / "trained_models"
OUTPUT_DIR.mkdir(exist_ok=True)

METADATA_PATH = BASE_DIR / "metadata.csv"

# --------------------------------------------------
# LOAD METADATA
# --------------------------------------------------

df = pd.read_csv(METADATA_PATH)

required_columns = {"image_path", "label"}
if not required_columns.issubset(df.columns):
    raise ValueError(
        "metadata.csv must contain image_path and label columns."
    )

df = df.dropna(subset=["image_path", "label"]).reset_index(drop=True)

paths = df["image_path"].astype(str).tolist()
y = df["label"].astype(int).to_numpy()

print("Images:", len(paths))
print("Labels:", np.unique(y, return_counts=True))
print("Device:", DEVICE)


# --------------------------------------------------
# TRAIN / VALIDATION / TEST SPLIT
# --------------------------------------------------

indices = np.arange(len(df))

train_idx, temp_idx = train_test_split(
    indices,
    test_size=0.30,
    random_state=RANDOM_STATE,
    stratify=y,
)

val_idx, test_idx = train_test_split(
    temp_idx,
    test_size=0.50,
    random_state=RANDOM_STATE,
    stratify=y[temp_idx],
)

print(
    f"Train: {len(train_idx)}, "
    f"Validation: {len(val_idx)}, "
    f"Test: {len(test_idx)}"
)


# --------------------------------------------------
# FEATURE EXTRACTORS
# --------------------------------------------------

def build_extractor(name):
    if name == "ResNet50":
        weights = ResNet50_Weights.DEFAULT
        model = resnet50(weights=weights)
        model.fc = torch.nn.Identity()

    elif name == "DenseNet121":
        weights = DenseNet121_Weights.DEFAULT
        model = densenet121(weights=weights)
        model.classifier = torch.nn.Identity()

    elif name == "EfficientNet-B0":
        weights = EfficientNet_B0_Weights.DEFAULT
        model = efficientnet_b0(weights=weights)
        model.classifier = torch.nn.Identity()

    else:
        raise ValueError(f"Unknown extractor: {name}")

    model = model.to(DEVICE)
    model.eval()

    return model, weights.transforms()


def extract_features(model, transform, image_paths):
    all_features = []

    for start in range(0, len(image_paths), BATCH_SIZE):
        batch_paths = image_paths[start:start + BATCH_SIZE]
        images = []

        for path in batch_paths:
            image_path = Path(path)

            if not image_path.is_absolute():
                image_path = BASE_DIR / image_path

            if not image_path.exists():
                raise FileNotFoundError(
                    f"Image not found: {image_path}"
                )

            image = Image.open(image_path).convert("RGB")
            images.append(transform(image))

        batch = torch.stack(images).to(DEVICE)

        with torch.no_grad():
            features = model(batch)

        all_features.append(features.cpu().numpy())

        print(
            f"Extracted {min(start + BATCH_SIZE, len(image_paths))}"
            f"/{len(image_paths)}",
            end="\r",
        )

    print()
    return np.concatenate(all_features, axis=0)


# --------------------------------------------------
# FEATURE SELECTORS
# --------------------------------------------------

def build_selector(name):
    if name == "Mutual Information":
        return SelectKBest(
            score_func=mutual_info_classif,
            k=TOP_K,
        )

    elif name == "RFE":
        estimator = ExtraTreesClassifier(
            n_estimators=100,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

        return RFE(
            estimator=estimator,
            n_features_to_select=TOP_K,
            step=0.2,
        )

    elif name == "L1-based Selection":
        estimator = SVC(
            kernel="linear",
            C=0.01,
            random_state=RANDOM_STATE,
        )

        return SelectFromModel(
            estimator=estimator,
            threshold="median",
        )

    raise ValueError(f"Unknown selector: {name}")


# --------------------------------------------------
# CLASSIFIERS
# --------------------------------------------------

def build_classifier(name):
    if name == "SVM":
        return SVC(
            kernel="rbf",
            probability=True,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        )

    elif name == "Random Forest":
        return RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

    elif name == "MLP":
        return MLPClassifier(
            hidden_layer_sizes=(256, 64),
            max_iter=100,
            early_stopping=True,
            random_state=RANDOM_STATE,
        )

    raise ValueError(f"Unknown classifier: {name}")


# --------------------------------------------------
# ALL 27 COMBINATIONS
# --------------------------------------------------

extractor_names = [
    "ResNet50",
    "DenseNet121",
    "EfficientNet-B0",
]

selector_names = [
    "Mutual Information",
    "RFE",
    "L1-based Selection",
]

classifier_names = [
    "SVM",
    "Random Forest",
    "MLP",
]

results = []

for extractor_name in extractor_names:
    print("\n" + "=" * 60)
    print("EXTRACTOR:", extractor_name)
    print("=" * 60)

    extractor, transform = build_extractor(extractor_name)

    feature_cache = OUTPUT_DIR / f"{extractor_name}_features.npy"

    if feature_cache.exists():
        X = np.load(feature_cache)
        print("Loaded cached features:", X.shape)
    else:
        X = extract_features(extractor, transform, paths)
        np.save(feature_cache, X)
        print("Saved features:", X.shape)

    del extractor
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    X_train, y_train = X[train_idx], y[train_idx]
    X_val, y_val = X[val_idx], y[val_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    for selector_name in selector_names:
        for classifier_name in classifier_names:
            print(
                "\nTraining:",
                extractor_name,
                "+",
                selector_name,
                "+",
                classifier_name,
            )

            pipeline = Pipeline([
                ("scaler", StandardScaler()),
                ("selector", build_selector(selector_name)),
                ("classifier", build_classifier(classifier_name)),
            ])

            try:
                pipeline.fit(X_train, y_train)

                val_pred = pipeline.predict(X_val)
                test_pred = pipeline.predict(X_test)

                val_accuracy = accuracy_score(y_val, val_pred)
                test_accuracy = accuracy_score(y_test, test_pred)

                print("Validation accuracy:", val_accuracy)
                print("Test accuracy:", test_accuracy)
                print("Confusion matrix:")
                print(confusion_matrix(y_test, test_pred))
                print(
                    classification_report(
                        y_test,
                        test_pred,
                        target_names=[
                            "Non-Alzheimer's",
                            "Alzheimer's",
                        ],
                    )
                )

                model_filename = (
                    f"{extractor_name}_{selector_name}_{classifier_name}"
                    .replace(" ", "_")
                    .replace("-", "_")
                    .replace("(", "")
                    .replace(")", "")
                    + ".joblib"
                )

                model_path = OUTPUT_DIR / model_filename
                joblib.dump(pipeline, model_path)

                results.append({
                    "extractor": extractor_name,
                    "selector": selector_name,
                    "classifier": classifier_name,
                    "validation_accuracy": val_accuracy,
                    "test_accuracy": test_accuracy,
                    "model_path": str(model_path),
                    "status": "trained",
                })

                print("Saved:", model_path)

            except Exception as error:
                print("FAILED:", error)

                results.append({
                    "extractor": extractor_name,
                    "selector": selector_name,
                    "classifier": classifier_name,
                    "status": "failed",
                    "error": str(error),
                })


# --------------------------------------------------
# SAVE SUMMARY
# --------------------------------------------------

summary_path = OUTPUT_DIR / "training_summary.json"

with open(summary_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)

print("\nTraining finished.")
print("Summary:", summary_path)
print(
    "Successfully trained:",
    sum(item["status"] == "trained" for item in results),
    "/ 27",
)