from django.urls import path

from . import views

urlpatterns = [
    path('upload_donors', views.upload_donors, name='upload_donors'),
    path('upload_donations', views.upload_donations, name='upload_donations'),
]
