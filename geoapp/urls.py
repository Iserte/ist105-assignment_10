from django.urls import path
from .views import continent_form_view, search_results_view, history_view

urlpatterns = [
    path("", continent_form_view, name="continent_form"),
    path("results/<str:continent>/<int:count>/", search_results_view, name="search_results"),
    path("history/", history_view, name="history"),
]