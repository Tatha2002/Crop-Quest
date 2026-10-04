from django.db import models
from accounts.models import User

class PlantDiseaseImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disease_predictions")
    image = models.ImageField(upload_to="plant_disease/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="PENDING")
    disease_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.image.name