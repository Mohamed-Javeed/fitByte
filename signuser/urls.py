from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='home'),
    path('login', loginPage, name='login'),
    path('register', registerPage, name='register'),
    path('info', infoPage, name='info'),
    path('nutrininja', nutriNinja, name='nutrininja'),
    path('chat', chat, name='chat'),
    path('profile', profile, name='profile'),
    path('logmeal', logMeal, name='logmeal'),
    path('getreward', getReward, name='getreward'),
    path('buycategory', buyCategory, name='buycategory')
]




