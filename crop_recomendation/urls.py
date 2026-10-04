from django.urls import path
from . import views

urlpatterns = [
    path("", views.crop_recommendation, name="crop_recommendation"),
    path("predict/", views.predict_crop, name="predict_crop"),
]