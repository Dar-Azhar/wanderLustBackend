from django.db import models
import uuid
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser

class Booking(models.Model):
    
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)  
    phone = models.CharField(max_length=12,validators=[MinLengthValidator(limit_value=10)]) 
    date = models.DateField()
    num_adults = models.PositiveIntegerField()  
    num_children = models.PositiveIntegerField()
    state = models.CharField(max_length=50)  

    def __str__(self):
        return self.full_name  
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name 


class Blogs(models.Model):
    blogId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.TextField()
    title = models.TextField()
    bannerImage = models.ImageField(upload_to='blog_images/')
    content = models.TextField()
    
    def __str__(self):
        return f"{self.title} ({self.blogId})"


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    REQUIRED_FIELDS = [ 'username' ]
    
    USERNAME_FIELD ="email"
    def __str__(self):
        return self.email
    
