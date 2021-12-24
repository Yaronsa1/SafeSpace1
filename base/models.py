from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


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

