from django.contrib import admin
from django.urls import path, include
from crop_recomendation import views

from django.conf.urls.static import static
from Crop_Recomendation_System import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("crop/", include("crop_recomendation.urls")),
    path("yield/", include("yield_prediction.urls")),
    path("disease/", include("disease_prediction.urls")),
    path('accounts/', include('accounts.urls')),
    path("api/", include("api.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)