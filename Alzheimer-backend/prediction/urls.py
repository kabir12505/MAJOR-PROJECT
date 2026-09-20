
from django.urls import path

from .views import (
    test_api,
    get_models,
    predict_mri,
    evaluation_summary,
)

urlpatterns = [
    path("test/", test_api, name="test-api"),
    path("models/", get_models, name="get-models"),
    path("predict/", predict_mri, name="predict-mri"),
    path("evaluation/", evaluation_summary, name="evaluation-summary"),
]