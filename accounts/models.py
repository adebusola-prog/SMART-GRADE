from base import constants
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.urls import reverse
from PIL import Image

from base.managers import MyUserManager, ActiveUserManager
from base.models import DeletableBaseModel
from phonenumber_field.modelfields import PhoneNumberField
    

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username"""
    FEMALE = constants.FEMALE
    MALE = constants.MALE

    GENDER_CHOICES =(
        ('F', FEMALE),
        ('M', MALE),
    )

    email = models.EmailField(max_length=255, unique=True, verbose_name="email address")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    is_verified = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='accounts/media', blank=True, null=True, default='static/images/pi.png')
    phone_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    
    REQUIRED_FIELDS= []
    USERNAME_FIELD = "email"
    
    objects = MyUserManager()
    active_objects = ActiveUserManager()

    def __str__(self):
        return self.email 
    
    @property
    def picture_url(self):
        try:
            url = self.picture.url
        except:
            url =''
        return url
    
    @property
    def is_admin(self):
         return self.is_staff


class Student(DeletableBaseModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, null=True, 
        related_name='student'
    )
    is_current = models.BooleanField(default=True)
    
    def get_full_name(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    def __str__(self):
        return f'{self.get_full_name()}'

class Teacher(DeletableBaseModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, null=True, 
        related_name="teacher"
    )
    students = models.ManyToManyField(
        Student,
        related_name="teachers",
        blank=True
    )
    
    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return f'{self.get_full_name()} ({self.user.email})'