from django.urls import path
from .views import ChronologyDetailView, chronology_line, event_detail, homepage

urlpatterns = [
    path("", homepage, name="homepage"),
    path("<str:slug>/", ChronologyDetailView.as_view(), name="chronology_detail"),
    path("chronology/<str:slug>/", chronology_line, name="chronology_line"),
    path("events/<str:slug>", event_detail, name="event_detail"),
]   