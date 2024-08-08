from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializer import BookingSerializer
from .serializer import  ContactSerializer
from .serializer import RegistrationSerializer
from django.http.response import JsonResponse,Http404
from .models import Booking
from .models import Contact
from .models import User
from django.forms.models import model_to_dict
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


def home_view(request):
    return HttpResponse("Hello, World!")

class ContactView(APIView):
      def post(self, request):
        data = request.data
        seriallizer =  ContactSerializer(data=data)
        
        if seriallizer.is_valid():
            seriallizer.save()
            return JsonResponse("message has been recieved successfully" ,safe=False)
        return JsonResponse(" message not recieved, kindly try again." , safe=False)
      def get(self, request):
        AllContacts = Contact.objects.all()  # Get all bookings
        serializer = ContactSerializer(AllContacts, many=True)  # Serialize the queryset
        return JsonResponse(serializer.data, safe=False)
        
class BookingView(APIView):

    def post(self, request):
        data = request.data
        seriallizer = BookingSerializer(data=data)

        if seriallizer.is_valid():
            seriallizer.save()
            return JsonResponse("booking has been done successfully" ,safe=False)
        return JsonResponse("booking failed, kindly try again." , safe=False)
    def get(self, request):
        bookings = Booking.objects.all()  # Get all bookings
        serializer = BookingSerializer(bookings, many=True)  # Serialize the queryset
        return JsonResponse(serializer.data, safe=False)
            
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
    
    
class RegisterView(APIView):
    def post(self, request):
        if request.method == 'POST' :
            serializer = RegistrationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "User registered successfully"}, status=status.HTTP_201_CREATED, safe=False)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST,safe=False)
        return JsonResponse({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def get(self, request):
        users = User.objects.all()
        serializer = RegistrationSerializer(users, many=True)
        return Response(serializer.data)

        
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email').strip()  # Change from username to email
        password = request.data.get('password').strip()
        
        user = authenticate(username=email, password=password)  # This should work with email

        if user:
            return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

  
            

