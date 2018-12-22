from django.urls import path

from . import views
from metrics.views import MetricsView

urlpatterns = [
    path('', MetricsView.as_view()),
]
