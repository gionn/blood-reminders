from django.urls import path

from . import views
from charts.views import ChartsView

urlpatterns = [
    path('', ChartsView.as_view()),
]
