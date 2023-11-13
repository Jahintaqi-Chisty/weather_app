from django.urls import path,include
from .views import get_coolest_districts_weather,compare_temperatures

urlpatterns = [
        path('compare-temperatures/', compare_temperatures, name='compare_temperatures'),
        path('coolest-districts/', get_coolest_districts_weather, name='coolest_districts'),



]