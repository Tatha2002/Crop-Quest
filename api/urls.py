from django.urls import path
from .api_views import RegisterAPIView, LoginAPIView, TestAuthAPIView, CropRecommendationAPIView


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="api_register"),
    path("login/", LoginAPIView.as_view(), name="api_login"),
    path("test-auth/", TestAuthAPIView.as_view(), name="test_auth"),
    path("crop-recommendation/", CropRecommendationAPIView.as_view(), name="api_crop_recommendation"),

]



# POST http://127.0.0.1:8000/api/crop-recommendation/