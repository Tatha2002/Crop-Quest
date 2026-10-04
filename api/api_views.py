from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from accounts.security.jwt_auth import (create_access_token,create_refresh_token,)

from .serializers import RegisterSerializer, LoginSerializer, CropRecommendationSerializer

import os
import pickle
import pandas as pd
from django.conf import settings
from django.templatetags.static import static
from crop_recomendation.models import CropRecomendation




class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "Registration successful.",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "phone": user.phone,
                        "role": user.role,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if not user:
            return Response(
                {
                    "message": "Invalid email/phone or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = create_access_token(
            user.id,
            user.role
        )

        refresh_token = create_refresh_token(
            user.id,
            user.role
        )

        return Response(
            {
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                },
                "tokens": {
                    "access": access_token,
                    "refresh": refresh_token,
                }
            },
            status=status.HTTP_200_OK
        )

    
class TestAuthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "message": "Authentication successful.",
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "phone": request.user.phone,
                "role": request.user.role,
            }
        })



class CropRecommendationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Validate input
        serializer = CropRecommendationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get validated data
        data = serializer.validated_data

        nitrogen = data["nitrogen"]
        phosphorus = data["phosphorus"]
        potassium = data["potassium"]
        temperature = data["temperature"]
        humidity = data["humidity"]
        ph = data["ph"]
        rainfall = data["rainfall"]

        # Model paths
        model_path = os.path.join(
            settings.BASE_DIR,
            "ml",
            "model.pkl"
        )

        scaler_path = os.path.join(
            settings.BASE_DIR,
            "ml",
            "scaler.pkl"
        )

        # Load model
        with open(model_path, "rb") as file:
            model_data = pickle.load(file)

        model = model_data["model"]

        # Load scaler
        with open(scaler_path, "rb") as file:
            scaler = pickle.load(file)

        # Prepare input
        input_data = pd.DataFrame([{
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall,
        }])

        # Scale only when required
        if (
            model_data["model_name"] == "Logistic Regression"
            or model_data["model_name"] == "SVM"
        ):
            input_data = scaler.transform(input_data)

        # Prediction
        prediction = model.predict(input_data)

        predicted_crop = prediction[0].lower()

        # Crop image
        image_url = static(
            f"images/crops/{predicted_crop}.jpg"
        )

        # Save prediction
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

        return Response(
            {
                "status": True,
                "prediction": predicted_crop,
                "image_url": image_url,
            },
            status=status.HTTP_200_OK
        )



