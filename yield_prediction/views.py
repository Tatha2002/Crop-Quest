from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from ml.train_model import train_model

from django.templatetags.static import static
import pandas as pd
import pickle
import os

from .forms import YieldPredictionForm
from .models import YieldPrediction

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.security.decorators import jwt_login_required


MODEL_PATH = os.path.join(settings.BASE_DIR,"ml","yield_model.pkl")

with open(MODEL_PATH, mode="rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
model_columns = model_data["columns"]


@never_cache
@login_required(login_url='login')
@jwt_login_required
def yield_display(request):
    # form = YieldPredictionForm()
    data = pd.read_csv("ml/dataset/crop-yield_selected_features.csv")
    soil_types = data["Soil Type"].dropna().unique().tolist()
    season_types = data["Season"].dropna().unique().tolist()
    crop_types = data["Crop Type"].dropna().unique().tolist()

    context:dict = {
        "soil_types": soil_types,
        "crop_types": crop_types,
        "season_types": season_types,
        # "form": form,
    }
    return render(request, "yield/yield.html", context)

@never_cache
@login_required(login_url='login')
@jwt_login_required
def yield_prediction(request):
    
    # Handle AJAX POST request
    if request.method == "POST":
        print(request.POST)
        form = YieldPredictionForm(request.POST)

        is_valid = form.is_valid()
        print("FORM VALID:", is_valid)
        print("FORM ERRORS:", form.errors)

        # Check form validation
        if not form.is_valid():

            return JsonResponse({
                "status": False,
                "errors": form.errors
            })

        try:
            # Get values from AJAX request
            crop_type = form.cleaned_data["crop_type"]
            soil_type = form.cleaned_data["soil_type"]
            temperature = form.cleaned_data["temperature"]
            humidity = form.cleaned_data["humidity"]
            rainfall = form.cleaned_data["rainfall"]
            season = form.cleaned_data["season"]

            print(".............................",crop_type)

            # Create DataFrame
            input_data = pd.DataFrame([{
                "Crop Type": crop_type,
                "Soil Type": soil_type,
                "Temperature": temperature,
                "Humidity": humidity,
                "Rainfall": rainfall,
                "Season": season,
            }])

            print("2. Before encoding:")
            print(input_data)

            # Apply same One-Hot Encoding used during training
            input_data = pd.get_dummies(input_data)

            # Make sure input has exactly the same columns as the training data
            input_data = input_data.reindex(columns=model_columns, fill_value=0)

            # Prediction
            prediction = model.predict(input_data)
            predicted_yield = float(prediction[0])


            # Save prediction history using Django ORM
            YieldPrediction.objects.create(
                user=request.user,
                crop_type=crop_type,
                soil_type=soil_type,
                temperature=temperature,
                humidity=humidity,
                rainfall=rainfall,
                season=season,
                predicted_yield=predicted_yield
            )

            # Send JSON response to JavaScript
            return JsonResponse({
                "status": True,
                "crop_yield": round(predicted_yield, 2)
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "error": str(e)
            })

    return JsonResponse({
        "status": False,
        "error": "Invalid request"
    })




