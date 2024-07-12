from django.contrib import admin
from django.urls import path
from .views import BookingView
from .views import home_view


urlpatterns = [
    path('', home_view, name='home'),
    path('booking/', BookingView.as_view()),
    path('booking/<int:pk>/', BookingView.as_view()),
    path('booking/<str:full_name>/<int:phone>/', BookingView.as_view()),


]