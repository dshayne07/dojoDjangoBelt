from __future__ import unicode_literals
import bcrypt
import datetime
from django.db import models

class UserManager(models.Manager):
    def register(self, postData):
        response = {
            'errors':[],
            'success':'',
            'uid':None,
        }
        if len(postData['name']) < 2:
            response['errors'].append("Name is too short!")
        if len(postData['username']) < 2:
            response['errors'].append("Username is too short!")
        else:
            usernames = User.objects.filter(username=postData['username'].lower())
            if len(usernames) > 0:
                response["errors"].append("Username already exists")
        if len(postData['password']) <8:
            response['errors'].append("Password must be 8 characters long!")
        elif postData['password'] != postData['confirm_password']:
            response['errors'].append("Passwords don't match!")
        if len(response['errors']) == 0:
            response['success'] = "Thanks for registering!"
            user = User.objects.create(
                name=postData['name'],
                username=postData['username'],
                password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            response['uid'] = user.id
        return response
    def login(self, postData):
        response = {
            'errors':[],
            'success':'',
            'uid':None,
            'name':None
        }
        if len(postData['username']) < 2:
            response['errors'].append("Username is too short!")
        else:
            usernames = User.objects.filter(username=postData['username'])
            if len(usernames) == 0:
                response["errors"].append("Invalid username/password!")
        if len(postData['password']) <8:
            response['errors'].append("Password must be 8 characters long!")
        if len(response['errors']) == 0:
            if bcrypt.checkpw(postData['password'].encode(), usernames[0].password.encode()):
                response['uid'] = usernames[0].id
                response['name'] = usernames[0].name
                response['success'] = "Logged in!"
            else:
                response["errors"].append("Invalid username/password!")
        
        return response

class TravelManager(models.Manager):
    def add_trip(self, postData, uid):
        response = {
            'errors':[],
            'success':'',
        }
        if len(postData['destination']) < 2:
            response["errors"].append("Destination is too short!")
        if len(postData['description']) < 2:
            response["errors"].append("Description is too short!")
        if len(postData['start_date']) < 1:
            response["errors"].append("Please enter a start date!")
        if len(postData['end_date']) < 1:
            response["errors"].append("Please enter a end date!")
        elif postData['start_date'] > postData['end_date']:
            response["errors"].append("Your start date is after your end date!")
        elif postData['start_date'] < str(datetime.datetime.now()):
            response["errors"].append("Your start date is in the past!")
        if len(response['errors']) == 0:
            response['success'] = "Trip Added!"
            your_plan = Travel.objects.create(
                destination=postData['destination'],
                start_date=postData['start_date'],
                end_date=postData['end_date'],
                plan=postData['description'],
                created_by=User.objects.get(id=uid))
        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="trips")
    users = models.ManyToManyField(User, related_name="plans")
    objects = TravelManager()