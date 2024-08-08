from django.contrib import admin
from django.urls import path
from .views import BookingView
from .views import ContactView
from .views import home_view
from .views import RegisterView
from .views import LoginView


urlpatterns = [
    path('', home_view, name='home'),
    path('all/', BookingView.as_view()),
    path('booking/', BookingView.as_view()),
    path('booking/<int:pk>/', BookingView.as_view()),
    path('booking/<str:full_name>/<int:phone>/', BookingView.as_view()),
    path('contact/', ContactView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

]