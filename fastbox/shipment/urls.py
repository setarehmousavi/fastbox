from django.urls import path
from shipment import views

app_name = "shipment"

urlpatterns = [
    path("track/search/", views.track_search, name="track_search"),
    path("track/result/<uuid:tracking_code>/", views.track_result, name="track_result"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.parcel_create, name="parcel_create"),
]
