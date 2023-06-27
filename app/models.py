from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.
class Jobs(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    company= models.CharField(max_length=200)
    description= models.TextField(max_length=10000)
    pay= models.CharField(max_length=45)
    requirement= models.TextField(max_length=10000)
    company_logo= models.ImageField(null=True, blank=True, default='sabri-tuzcu-wunVFNvqhfE-unsplash.jpg')
    # email= models.EmailField(max_length=100)
    date_due= models.DateField()
    date_posted= models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title