from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import test_api, get_models


@api_view(["GET"])
def test_api(request):
    return Response({
        "message": "Alzheimer Detection API is working!",
        "status": "success"
    })


urlpatterns = [
    path("test/", test_api, name="test-api"),
     path("models/", get_models, name="get-models"),
]
from django.urls import path
from .views import test_api, get_models, predict_mri

urlpatterns = [
    path("test/", test_api, name="test-api"),
    path("models/", get_models, name="get-models"),
    path("predict/", predict_mri, name="predict-mri"),
]