from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    permission = models.IntegerField(default=0) #0 = visitor ; 1 = business owner ; 2 = Staff#
    haveBusiness = models.BooleanField(default=False) #False have not ; True have#
    avatar = models.ImageField(null=True, default="avatar.svg")
    greenpass = models.ImageField(null=True, default="green_pass.jpg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Restrictions(models.Model):
    name = models.CharField(max_length= 200)
    def __str__(self):
        return self.name

class Place(models.Model):
    owner= models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    placePhoneNumber = models.CharField(max_length=14)
    description = models.TextField(null=True,blank=True)
    email = models.CharField(max_length=14,null=True,blank=True)
    restrictions = models.ManyToManyField(Restrictions, related_name="placeRestrictions",blank=False)
    addedOn = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(null=True, default="noimage.png")

    class Meta:
        ordering = ['-addedOn', '-lastUpdated']
    
    def __str__(self):
        return self.name

   

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    body = models.TextField()
    addedOn = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-addedOn', '-lastUpdated']
        
    def __str__(self):
        return self.body[0:20]

