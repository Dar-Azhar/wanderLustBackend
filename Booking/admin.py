from django.contrib import admin
from .models import Booking,Contact
# Register your models here.
model_list = [Booking, Contact]
admin.site.register(Booking)
admin.site.register(Contact)