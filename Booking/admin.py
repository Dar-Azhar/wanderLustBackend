from django.contrib import admin
from .models import Booking
# Register your models here.
model_list = [Booking]
admin.site.register(Booking)