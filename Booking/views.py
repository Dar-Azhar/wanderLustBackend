from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializer import BookingSerializer
from .serializer import  ContactSerializer
from .serializer import RegistrationSerializer
from . serializer import BlogsSerializer
from django.http.response import JsonResponse,Http404
from .models import Booking
from .models import Contact
from .models import User,Blogs
from django.forms.models import model_to_dict
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt



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
    
class BlogsView(APIView):
    def post(self, request):
        data = request.data
        serializer = BlogsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your Blog has been created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Failed to create blog, kindly try again.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, blogId=None):
        if blogId is not None:
            # Fetch a single blog by id
            try:
                single_blog = Blogs.objects.get(blogId=blogId)
                serializer = BlogsSerializer(single_blog)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Blogs.DoesNotExist:
                return Response({"error": "Blog not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Fetch all blogs
            all_blogs = Blogs.objects.all()
            serializer = BlogsSerializer(all_blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    # def post(self, request):
    #     data = request.data
    #     serializer = BlogsSerializer(data=data)
        
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse("Your Blog has been created successfully", status=status.HTTP_201_CREATED, safe=False)
    #     return JsonResponse(" failed to create blog, kindly try again." , safe=False)
    # def get(self, request):
    #     allBlogs = Blogs.object.all()
    #     serializer = BlogsSerializer(allBlogs, many=True)
    #     return JsonResponse(serializer.data, safe=False)
    # def get(self, request):
    #     id = request.data.params
    #     SingleBlog = Blogs.get(id)
    #     serializer = BlogsSerializer(SingleBlog)
    #     return JsonResponse(serializer.data, safe=False)
        
            

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
        authentication_classes = (TokenAuthentication,)
        email = request.data.get('email').strip()  
        password = request.data.get('password').strip()
        
        user = authenticate(username=email, password=password) 
        
        if user:
           login(request, user)
           token, created = Token.objects.get_or_create(user=user)
           user_data = {
              "token": token.key,
              "message": "Login successful!",
              "user":{
                  "UserId" : user.id,
                  "name" : user.username,
                  "email" : user.email
              }
              
          }
           return Response(user_data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        token = request.auth
        if token:
            token.delete()
        logout(request)
        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)

  
            

