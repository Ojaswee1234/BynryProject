from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('submit_request/', views.submit_request, name='submit_request'),
    path('request_status/', views.request_status, name='request_status'),
    # Other URL patterns for your app
]


