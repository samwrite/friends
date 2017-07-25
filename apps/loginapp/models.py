from __future__ import unicode_literals

from django.db import models
import re, bcrypt
from django.contrib import messages
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
class UserManager(models.Manager):
    def register(self,postData):
        result = {'status':True, 'error':[]}
        if not postData['first_name'] or postData['first_name'] < 2:
            result['status'] = False
            result['error'].append('First name must be longer than 1 letter')
        if not postData['last_name'] or postData['last_name'] < 2:
            result['status'] = False
            result['error'].append('Last name must be longer than 1 letter')
        if not postData['email'] or not EMAIL_REGEX.match(postData['email']):
            result['status'] = False
            result['error'].append('Must be a valid email')
        if not postData['password'] or postData['password'] < 8:
            result['status'] = False
            result['error'].append('Password must be longer than 8 characters')
        if not postData['confpassword'] or postData['confpassword'] != postData['password']:
            result['status'] = False
            result['error'].append('Passwords must match')
        if result['status'] == True:
            if User.objects.filter(email = postData['email']):
                result['status'] = False
                result['error'].append('User already exist')
            else:
                password = postData['password'].encode('utf-8')
                hashedpw = bcrypt.hashpw(password,bcrypt.gensalt(12))
                User.objects.create(
                    first_name = postData['first_name'],
                    last_name = postData['last_name'],
                    email = postData['email'],
                    password = hashedpw,
                )
        return result
    def login(self,postData, sessionData):
        user = User.objects.filter(email = postData['email'])
        if len(user) > 0:
            hashed = User.objects.get(email = postData['email']).password.encode('utf-8')
            password = postData['password'].encode('utf-8')
            if bcrypt.hashpw(password,hashed) == hashed:
                sessionData['id'] = User.objects.get(email = postData['email']).id
                return True
            else:
                return False

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    friends = models.ManyToManyField('self', related_name='friendof')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()