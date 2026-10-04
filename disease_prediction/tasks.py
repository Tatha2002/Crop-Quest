from celery import shared_task

from .models import PlantDiseaseImage
from ml.disease_prediction import predict_plant_disease


@shared_task
def predict_disease_task(image_id):
    plant_image = PlantDiseaseImage.objects.get(id=image_id)

    try:
        plant_image.status = "PROCESSING"
        plant_image.save()

        image_path = plant_image.image.path
        disease_name = predict_plant_disease(image_path)

        plant_image.disease_name = disease_name
        plant_image.status = "COMPLETED"
        plant_image.save()

    except Exception as e:
        plant_image.status = "FAILED"
        plant_image.save()

        print("Prediction error:", e)