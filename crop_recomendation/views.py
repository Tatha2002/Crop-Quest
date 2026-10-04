from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from ml.train_model import train_model

from django.templatetags.static import static
from .forms import CropPredictionForm
from .models import CropRecomendation
import pandas as pd
import pickle
import os

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.security.decorators import jwt_login_required


@never_cache
@login_required(login_url='login')
@jwt_login_required
def home(request):
    return render(request, "home.html")

@never_cache
@login_required(login_url='login')
@jwt_login_required
def crop_recommendation(request):
    return render(request, "crop/crop.html")


@never_cache
# @login_required(login_url='login')
@jwt_login_required
def predict_crop(request):
    # print("========== PREDICT CROP VIEW CALLED ==========")
    # print("METHOD:", request.method)
    # print("POST:", request.POST)

    if request.method == "POST":
        print(request.POST)
        form = CropPredictionForm(request.POST)

        if not form.is_valid(): 
            return JsonResponse({ 
                "status": False, 
                "errors": form.errors 
            })

        model_path = os.path.join(settings.BASE_DIR, "ml", "model.pkl")
        scaler_path = os.path.join(settings.BASE_DIR,"ml","scaler.pkl")

        # Train model if pickle files don't exist
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            train_model(os.path.join(settings.BASE_DIR,"ml","dataset","crop_recommendation_dataset.csv"))

        with open(model_path, mode="rb") as file:
            model_data = pickle.load(file)

        model: dict = model_data["model"]

        # Load scaler
        with open(scaler_path, mode="rb") as file:
            scaler = pickle.load(file)


        nitrogen = form.cleaned_data["nitrogen"] 
        phosphorus = form.cleaned_data["phosphorus"] 
        potassium = form.cleaned_data["potassium"] 
        temperature = form.cleaned_data["temperature"] 
        humidity = form.cleaned_data["humidity"] 
        ph = form.cleaned_data["ph"] 
        rainfall = form.cleaned_data["rainfall"]


        # Get user input
        input_data = pd.DataFrame([{ 
            "N": nitrogen, 
            "P": phosphorus, 
            "K": potassium, 
            "temperature": temperature, 
            "humidity": humidity, 
            "ph": ph, 
            "rainfall": rainfall, 
        }])


        print("INPUT FROM USER:")
        print(input_data)

        # Scale input
        if model_data["model_name"] == "Logistic Regression" or model_data["model_name"] == "SVM":
            input_data = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_data)

        # for image url
        predicted_crop = prediction[0].lower()
        image_url = static(f"images/crops/{predicted_crop}.jpg")


        print("Model:", model_data["model_name"])
        print("Prediction:", prediction[0])
        # print("Image:", image_url)


        CropRecomendation.objects.create(
            user=request.user,
            nitrogen=nitrogen, 
            phosphorus=phosphorus, 
            potassium=potassium, 
            temperature=temperature, 
            humidity=humidity, 
            ph=ph, 
            rainfall=rainfall, 
            predicted_crop=predicted_crop, 
        )

        return JsonResponse({
            "status": True,
            # "prediction": prediction[0],
            "prediction": predicted_crop,
            "image_url": image_url,
        })


    return JsonResponse({
        "status": False,
        "errors": "Invalid Request"
    })










