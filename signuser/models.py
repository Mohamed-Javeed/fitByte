from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class User(models.Model):
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     name = models.CharField(max_length=100, null=True)
#     password = models.CharField(max_length=100, null=True)
#     height = models.FloatField(null=True)
#     weight = models.FloatField(null=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
#     age = models.IntegerField(null=True)

#     def __str__(self):
#         return self.name

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username = models.CharField(max_length=100, null=True, unique=True)
    # email = models.EmailField(unique=True, null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    # avatar = models.ImageField(null=True, default='avatar.svg')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    age = models.IntegerField(null=True)
    level = models.IntegerField(null=True, default=1)
    xp = models.IntegerField(null=True, default=10)
    strength = models.IntegerField(null=True, default=1)
    muscle = models.IntegerField(null=True, default=1)
    physique = models.IntegerField(null=True, default=1)
    carbos = models.IntegerField(null=True, default=5)
    protos = models.IntegerField(null=True, default=5)
    fatos = models.IntegerField(null=True, default=5)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    photo_name = models.CharField(max_length=100, null=True)
    food_name = models.CharField(max_length=100, null=True)
    cals = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    fats = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.food_name}, {self.date_created}"
