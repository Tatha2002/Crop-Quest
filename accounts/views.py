from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.security.decorators import jwt_login_required

from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from.models import User

from accounts.security.jwt_auth import (create_access_token, create_refresh_token, decode_access_token, decode_refresh_token)
from crop_recomendation.models import CropRecomendation
from yield_prediction.models import YieldPrediction
from disease_prediction.models import PlantDiseaseImage
from django.db.models import QuerySet


def register_view(request):
    if request.method == 'POST':
        print(f"Request POST: {request.POST}")

        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Password and Confirm Password do not match.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect("register")

        User.objects.create_user(email=email, phone=phone, password=password, role=role)

        messages.success(request, "Registration Successful. Please Login")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request: HttpRequest):
    context: dict = {
        "error": "",
    }

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if not user:
            context["error"] = "Invalid Email/Phone or Password"
            return render(request, "accounts/login.html", context)

        login(request, user)

        access_token = create_access_token(user.id, user.role)
        refresh_token = create_refresh_token(user.id, user.role)

        response: HttpResponseRedirect = redirect('dashboard')

        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="Lax")
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="Lax")
        return response

    return render(request, "accounts/login.html", context)


@never_cache
@login_required
@jwt_login_required
def dashboard(request):
    token = request.COOKIES.get("access_token")

    if not token:
        return redirect("login")

    try:
        user_id = decode_access_token(token)
        user = User.objects.get(id=user_id)

        # Get user's predictions
        crop_predictions: QuerySet = CropRecomendation.objects.filter(user=user)
        yield_predictions: QuerySet = YieldPrediction.objects.filter(user=user)
        disease_predictions: QuerySet = PlantDiseaseImage.objects.filter(user=user)

        # Prediction counts
        crop_count = crop_predictions.count()
        yield_count = yield_predictions.count()
        disease_count = disease_predictions.count()
        total_predictions = crop_count + yield_count + disease_count

        # Recent activity
        recent_activities: list = list()
        for prediction in crop_predictions:
            recent_activities.append({
                "date": prediction.created_at,
                "type": "Crop Recommendation",
                "result": prediction.predicted_crop,
            })

        for prediction in yield_predictions:
            recent_activities.append({
                "date": prediction.created_at,
                "type": "Yield Prediction",
                "result": f"{round(prediction.predicted_yield, 2)} t/ha",
            })

        # Disease Prediction
        for prediction in disease_predictions:
            recent_activities.append({
                "date": prediction.uploaded_at,
                "type": "Disease Prediction",
                "result": prediction.disease_name,
            })

        # Newest First
        recent_activities.sort(key=lambda x: x["date"], reverse=True)

        # Only latest 5
        recent_activities = recent_activities[:5]

    except AuthenticationFailed:
        return redirect("refresh_token")

    except User.DoesNotExist:
        response = redirect("login")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


    print(f"Total predictions: {total_predictions}")
    print(f"Crop count: {crop_count}")
    print(f"Yield count: {yield_count}")
    print(f"Disease count: {disease_count}")
    # print(recent_activities)


    response = render(request, "accounts/dashboard.html", {
            "user": user,
            "is_authenticated": True,

            "total_predictions": total_predictions,
            "crop_count": crop_count,
            "yield_count": yield_count,
            "disease_count": disease_count,
            "recent_activities": recent_activities,
        }
    )

    # manually clearing cache.
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


def refresh_token_view(request):
    refresh_token = request.COOKIES.get("refresh_token")

    # Refresh Token Missing
    if not refresh_token:
        response = redirect("login")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    try:
        # Decode Refresh Token
        user_id = decode_refresh_token(refresh_token)
        user = User.objects.get(id=user_id)

        # Generate New Tokens
        new_access_token = create_access_token(user.id, user.role)
        # new_refresh_token = create_refresh_token(user.id, user.role)

        response = redirect("dashboard")

        response.set_cookie(key="access_token",value=new_access_token,httponly=True,samesite="Lax")
        # response.set_cookie(key="refresh_token",value=new_refresh_token,httponly=True,samesite="Lax")
        return response

    except User.DoesNotExist:
        response = redirect("login")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    except AuthenticationFailed:
        response = redirect("login")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


def logout_view(request):
    print("BEFORE LOGOUT:", request.COOKIES)
    response = redirect("login")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    logout(request)
    print("AFTER LOGOUT:", request.COOKIES)
    return response








