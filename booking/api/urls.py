from django.urls import include, path


urlpatterns = [
    path("v1/", include("booking.api.v1.urls")),
]