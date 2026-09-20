from functools import lru_cache
from torchvision.models import (
    resnet50,
    ResNet50_Weights,
    densenet121,
    DenseNet121_Weights,
    efficientnet_b0,
    EfficientNet_B0_Weights,
)
import os
import numpy as np
import torch
from PIL import Image
from torchvision import models
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import joblib
from torchvision.models import resnet50, ResNet50_Weights





@api_view(["GET"])
def test_api(request):
    return Response({
        "message": "Alzheimer Detection API is working!",
        "status": "success"
    })

from itertools import product
from rest_framework.decorators import api_view
from rest_framework.response import Response


FEATURE_EXTRACTORS = [
    "ResNet50",
    "DenseNet121",
    "EfficientNet-B0",
]

FEATURE_SELECTORS = [
    "Mutual Information",
    "RFE",
    "L1-based Selection",
]

CLASSIFIERS = [
    "SVM",
    "Random Forest",
    "MLP",
]


@api_view(["GET"])
def get_models(request):
    combinations = []

    for index, (extractor, selector, classifier) in enumerate(
        product(
            FEATURE_EXTRACTORS,
            FEATURE_SELECTORS,
            CLASSIFIERS
        ),
        start=1
    ):
        combinations.append({
            "id": index,
            "feature_extractor": extractor,
            "feature_selector": selector,
            "classifier": classifier,
        })

    return Response({
        "total_models": len(combinations),
        "models": combinations,
    })

# Base directory of the Django project
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = os.path.join(BASE_DIR, "trained_models")


@lru_cache(maxsize=27)
def load_trained_model(extractor, selector, classifier):

    extractor_name = extractor.replace("-", "_")
    selector_name = selector.replace(" ", "_")
    selector_name = selector_name.replace("-", "_")
    classifier_name = classifier.replace(" ", "_")

    model_filename = (
        f"{extractor_name}_{selector_name}_{classifier_name}.joblib"
    )

    model_path = os.path.join(MODEL_DIR, model_filename)

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Trained model not found: {model_filename}"
        )

    return joblib.load(model_path)


def load_feature_extractor(extractor):

    if extractor == "ResNet50":
        weights = ResNet50_Weights.DEFAULT
        model = resnet50(weights=weights)
        model.fc = torch.nn.Identity()

    elif extractor == "DenseNet121":
        weights = DenseNet121_Weights.DEFAULT
        model = densenet121(weights=DenseNet121_Weights.DEFAULT)
        model.classifier = torch.nn.Identity()

    elif extractor == "EfficientNet-B0":
        weights = EfficientNet_B0_Weights.DEFAULT
        model = efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
        model.classifier = torch.nn.Identity()

    else:
        raise ValueError("Invalid feature extractor")

    model.eval()
    return model, weights.transforms()


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def predict_mri(request):
    uploaded_file = request.FILES.get("image")

    extractor = request.data.get("extractor")
    selector = request.data.get("selector")
    classifier = request.data.get("classifier")

    if uploaded_file is None:
        return Response(
            {"error": "Please upload an MRI image using 'image' field."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not extractor or not selector or not classifier:
        return Response(
            {"error": "Please select all three model options."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if extractor not in FEATURE_EXTRACTORS:
        return Response(
            {"error": "Invalid feature extractor."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if selector not in FEATURE_SELECTORS:
        return Response(
            {"error": "Invalid feature selector."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if classifier not in CLASSIFIERS:
        return Response(
            {"error": "Invalid classifier."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Load selected trained pipeline
        trained_model = load_trained_model(
            extractor, selector, classifier
        )

        # Load matching feature extractor
        feature_extractor, preprocess = load_feature_extractor(
            extractor
        )

        # Process uploaded image
        image = Image.open(uploaded_file).convert("RGB")
        image_tensor = preprocess(image).unsqueeze(0)

        with torch.no_grad():
            features = feature_extractor(image_tensor)

        features = features.cpu().numpy()

        # Pipeline includes scaling, feature selection, classifier
        prediction = int(trained_model.predict(features)[0])

        label = (
            "Alzheimer's"
            if prediction == 1
            else "Non-Alzheimer's"
        )

        return Response({
            "prediction": label,
            "class_id": prediction,
            "model": f"{extractor} + {selector} + {classifier}",
            "note": (
                "Research prototype output, "
                "not a clinical diagnosis."
            )
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

import json

SUMMARY_PATH = os.path.join(
    BASE_DIR,
    "trained_models",
    "training_summary.json"
)

@api_view(["GET"])
def evaluation_summary(request):
    """
    Return evaluation metrics for all trained models.
    """

    if not os.path.exists(SUMMARY_PATH):
        return Response(
            {
                "error": "training_summary.json not found",
                "expected_path": SUMMARY_PATH
            },
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        with open(SUMMARY_PATH, "r", encoding="utf-8") as file:
            summary = json.load(file)

        return Response(summary)

    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON in training_summary.json"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )    