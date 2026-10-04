from django import forms
from .models import CropRecomendation


class CropPredictionForm(forms.ModelForm):

    class Meta:
        model = CropRecomendation
        fields = ["nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph", "rainfall"]


    def clean_nitrogen(self):
        nitrogen = self.cleaned_data.get("nitrogen")

        if nitrogen is None:
            raise forms.ValidationError("Nitrogen cannot be empty.")

        if nitrogen < 0 or nitrogen > 140:
            raise forms.ValidationError("Nitrogen must be between 0 and 140.")

        return nitrogen


    def clean_phosphorus(self):
        phosphorus = self.cleaned_data.get("phosphorus")

        if phosphorus is None:
            raise forms.ValidationError("Phosphorus cannot be empty.")

        if phosphorus < 0 or phosphorus > 145:
            raise forms.ValidationError("Phosphorus must be between 0 and 145.")

        return phosphorus


    def clean_potassium(self):
        potassium = self.cleaned_data.get("potassium")

        if potassium is None:
            raise forms.ValidationError("Potassium cannot be empty.")

        if potassium < 0 or potassium > 205:
            raise forms.ValidationError("Potassium must be between 0 and 205.")

        return potassium


    def clean_temperature(self):
        temperature = self.cleaned_data.get('temperature')

        if temperature is None:
            raise forms.ValidationError("Temperature is required.")

        if temperature < -50 or temperature > 60:
            raise forms.ValidationError("Temperature must be between -50°C and 60°C.")

        return temperature


    def clean_humidity(self):
        humidity = self.cleaned_data.get('humidity')

        if humidity is None:
            raise forms.ValidationError("Humidity is required.")

        if humidity < 0 or humidity > 100:
            raise forms.ValidationError("Humidity must be between 0 and 100.")

        return humidity


    def clean_ph(self):
        ph = self.cleaned_data.get("ph")

        if ph is None:
            raise forms.ValidationError("pH cannot be empty.")

        if ph < 0 or ph > 14:
            raise forms.ValidationError("pH must be between 0 and 14.")

        return ph


    def clean_rainfall(self):
        rainfall = self.cleaned_data.get('rainfall')

        if rainfall is None:
            raise forms.ValidationError("Rainfall is required.")

        if rainfall < 0:
            raise forms.ValidationError("Rainfall cannot be negative.")

        return rainfall




