from django.urls import path
from . import views

urlpatterns = [
    # path("", views.disease_display, name="disease_display"),
    path("predict/", views.plant_disease_prediction, name="plant_disease_prediction"),
    # path("prediction-yield/", views.yield_prediction, name="yield_prediction")
    path("status/<int:prediction_id>/", views.disease_prediction_status, name="disease_prediction_status"),
]