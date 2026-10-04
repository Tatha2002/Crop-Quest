from django.db import models
from accounts.models import User

class CropRecomendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crop_recommendations")
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    predicted_crop = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.predicted_crop