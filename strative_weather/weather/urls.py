from django.urls import path,include
from .views import get_coolest_districts_weather

urlpatterns = [
        path('coolest-districts/', get_coolest_districts_weather, name='coolest_districts'),



]