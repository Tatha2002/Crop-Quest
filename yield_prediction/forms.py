from django import forms
from .models import YieldPrediction


class YieldPredictionForm(forms.ModelForm):

    class Meta:
        model = YieldPrediction
        fields = ["crop_type", "soil_type", "temperature", "humidity", "rainfall", "season"]

    def clean_crop_type(self):
        crop: str = self.cleaned_data['crop_type']

        if not crop.strip():
            raise forms.ValidationError("Crop type is required.")

        return crop

    def clean_soil_type(self):
        soil = self.cleaned_data['soil_type']

        if not soil.strip():
            raise forms.ValidationError("Soil type is required.")

        return soil

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

    def clean_rainfall(self):
        rainfall = self.cleaned_data.get('rainfall')

        if rainfall is None:
            raise forms.ValidationError("Rainfall is required.")

        if rainfall < 0:
            raise forms.ValidationError("Rainfall cannot be negative.")

        return rainfall

    def clean_season(self):
        season = self.cleaned_data['season']

        if not season.strip():
            raise forms.ValidationError("Season is required.")

        return season