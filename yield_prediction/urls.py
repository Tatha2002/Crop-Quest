from django.urls import path
from . import views

urlpatterns = [
    path("", views.yield_display, name="yield_display"),
    path("prediction-yield/", views.yield_prediction, name="yield_prediction")
]