from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import BookingSerializer
from django.http.response import JsonResponse,Http404
from .models import Booking
from rest_framework.response import Response

# Create your views here.

from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Hello, World!")

class BookingView(APIView):

    def post(self, request):
        data = request.data
        seriallizer = BookingSerializer(data=data)

        if seriallizer.is_valid():
            seriallizer.save()
            return JsonResponse("booking has been done successfully" ,safe=False)
        return JsonResponse("booking failed, kindly try again." , safe=False)

    def get_booking(self,pk):
        try:
            booking = Booking.objects.get(id = pk)
            return booking
        except Booking.DoesNotExist():
            return "Booking does not exist"
        
    def search_booking(self, full_name, phone):
        try:
            booking = Booking.objects.get(full_name=full_name, phone=phone)
            return booking
        except Booking.DoesNotExist:
            return "Booking not found"
   
    def get(self, request, pk=None, full_name=None, phone=None):
        serializer = None
        
        
        if pk:
            data = self.get_booking(pk)
            serializer = BookingSerializer(data)
        

        elif full_name and phone:
                # Search for booking by name and phone
                data = self.search_booking(full_name, phone)
                if data:
                    serializer = BookingSerializer(data)
                else:
                    return JsonResponse("Booking not found", status=404)
        else:
                # If full_name and phone are not provided, return all bookings
                data = Booking.objects.all()
                serializer = BookingSerializer(data, many=True)

        return Response(serializer.data)
        
    def put(self, request, pk=None):
        booking_to_update = Booking.objects.get(id=pk)
        serializer =  BookingSerializer(instance=booking_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("booking updated sucessfully", safe=False)
        return JsonResponse("Failed to update your booking, please try again!", safe=False)

    def delete(self, request, pk=None):
        booking_to_delete = Booking.objects.get(id=pk)
        booking_to_delete.delete()
        return JsonResponse("booking deleted sucessfully", safe=False) 

