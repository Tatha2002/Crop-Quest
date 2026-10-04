from django.shortcuts import render
from django.http import JsonResponse

from .models import PlantDiseaseImage
from .tasks import predict_disease_task

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.security.decorators import jwt_login_required


@never_cache
@login_required(login_url='login')
@jwt_login_required
def plant_disease_prediction(request):
    if request.method == "POST":
        image = request.FILES.get("plant_image")
        if image:
            uploaded_image = PlantDiseaseImage.objects.create(user=request.user, image=image)

            # Start Celery task
            predict_disease_task.delay(uploaded_image.id)

            return JsonResponse({
                "status": True,
                "image_url": uploaded_image.image.url,
                "prediction_id": uploaded_image.id
            })

    return render(request, "disease/disease.html")


@never_cache
@login_required(login_url='login')
@jwt_login_required
def disease_prediction_status(request, prediction_id):
    prediction = PlantDiseaseImage.objects.get(id=prediction_id)

    return JsonResponse({
        "status": prediction.status,
        "disease_name": prediction.disease_name
    })