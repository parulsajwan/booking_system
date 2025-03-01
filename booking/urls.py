from django.urls import include, path

app_name = "booking"

urlpatterns = [
    path("api/", include("booking.api.urls")),
]
