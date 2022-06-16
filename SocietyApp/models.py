from pyexpat import model
from tkinter import CASCADE
from django.db import models
import datetime

class UserType(models.Model):
    Type = models.CharField(max_length=15)

    class Meta:
        db_table = 'UserType'

    
# Master record
class Master(models.Model):
    Email=models.EmailField(unique=True)
    Password=models.CharField(max_length=12)
    UserType = models.ForeignKey(UserType, on_delete=models.CASCADE)
    IsActive=models.BooleanField(default=False)
    DateCreated=models.DateTimeField(auto_now=True)
    LastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='master'

gender_choices=(
    ('M','Male'),
    ('F','Female'),
)


class Profile(models.Model):
    Master=models.ForeignKey(Master,on_delete=models.CASCADE)
    ProfileImage = models.FileField(upload_to="profile/", default="default.png")
    FullName=models.CharField(max_length=30,default='')
    Email=models.EmailField(unique=True)
    Gender=models.CharField(max_length=6, choices=gender_choices)
    Mobile=models.CharField(max_length=10,default='')
    
    Address=models.TextField(max_length=100,default='')


    class Meta:
        db_table='profile'



class User(models.Model):
    Master=models.ForeignKey(Master,on_delete=models.CASCADE)
    UID = models.CharField(max_length=20)
    Firstname=models.CharField(max_length=30,default='')
    Lastname=models.CharField(max_length=30,default='')
    Address=models.TextField(max_length=100,default='')
    Gender=models.CharField(max_length=6, choices=gender_choices)
    City=models.CharField(max_length=30,default='')
    Country=models.CharField(max_length=30,default='')
    Mobile=models.CharField(max_length=10,default='')
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now=True)


    class Meta:
        db_table='user'



class Complain(models.Model):
    User= models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    Complain=models.TextField(max_length=100,default='')
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'complain'

class Society_rules(models.Model):
    Master= models.ForeignKey(Master, on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    Society_rules=models.TextField(max_length=100,default='')
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'society_rules'

class Transaction(models.Model):
    made_by = models.ForeignKey(Profile, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

class Event(models.Model):
    User= models.ForeignKey(User, on_delete=models.CASCADE)
    Eventname = models.CharField(max_length=50)
    EventImage = models.FileField(upload_to="change_event/", default="default.jpg")
    Eventdescription=models.TextField(max_length=100,default='')
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'event'