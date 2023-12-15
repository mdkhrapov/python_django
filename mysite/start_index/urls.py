from django.urls import path
from .views import StartIndex

app_name = "start_index"

urlpatterns = [
    path("", StartIndex.as_view(), name="start_index"),
]