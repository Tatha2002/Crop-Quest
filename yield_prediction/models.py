from django.db import models
from accounts.models import User

class YieldPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="yield_predictions")
    crop_type = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    predicted_yield = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_type} - {self.predicted_yield}"