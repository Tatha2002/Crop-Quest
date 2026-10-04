from rest_framework import serializers
from accounts.models import User
from crop_recomendation.models import CropRecomendation


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "phone", "password", "confirm_password", "role",]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password and Confirm Password do not match.")

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists.")

        if User.objects.filter(phone=data["phone"]).exists():
            raise serializers.ValidationError("Phone number already exists.")

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            email=validated_data["email"],
            phone=validated_data["phone"],
            password=validated_data["password"],
            role=validated_data["role"],
        )

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class CropRecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CropRecomendation

        fields = [
            "nitrogen",
            "phosphorus",
            "potassium",
            "temperature",
            "humidity",
            "ph",
            "rainfall",
        ]


    
