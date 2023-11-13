from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .district import DISTRICT

def fetch_data(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_average_temperature(data):
    hourly = data.get('hourly', {})
    temperature_2m_values = hourly.get('temperature_2m', {})
    if temperature_2m_values:
        temperatures_2pm = temperature_2m_values[14:165:24]
        return sum(temperatures_2pm) / len(temperatures_2pm)
    return None

def get_weather_data(latitude, longitude,district_name ,cache_key=None):
    if cache_key:
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m"
    }

    try:
        response_data = fetch_data(url, params)
        result = {
            'district': district_name,
            'latitude': latitude,
            'longitude': longitude,
            'average_temperature_2pm': get_average_temperature(response_data)
        }
        if cache_key:
            cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
        return result
    except requests.RequestException as e:
        print(f"Error fetching data for {latitude}, {longitude}: {e}")
        return None

@api_view(['GET'])
def get_coolest_districts_weather(request):
    with ThreadPoolExecutor() as executor:
        district_weather_list = list(executor.map(get_weather_data, [float(d['lat']) for d in DISTRICT['districts']],
                                                 [float(d['long']) for d in DISTRICT['districts']],[d['name'] for d in DISTRICT['districts']]))

    district_weather_list = [weather for weather in district_weather_list if weather is not None]

    coolest_districts = sorted(district_weather_list, key=lambda x: x['average_temperature_2pm'])[:10]

    response_data = {"coolest_districts": coolest_districts}
    return Response(response_data)






# @require_GET
# def get_coolest_districts_weather(request):
#
#     districts_data = DISTRICT.get('districts', [])
#
#     # Prepare a list to store the average temperatures for each district
#     district_temperatures = []
#
#     for district in districts_data:
#         latitude = float(district['lat'])
#         longitude = float(district['long'])
#
#         url = f"https://api.open-meteo.com/v1/forecast"
#         params = {
#             "latitude": latitude,
#             "longitude": longitude,
#             "hourly": "temperature_2m"
#         }
#         response = requests.get(url, params=params)
#         a = 1
#
#         # if a==1:
#         print(f"====>{response.status_code}\n")
#         if response.status_code==200:
#             data = response.json()
#
#             # # Process hourly data
#             hourly = data.get('hourly', {})
#             temperature_2m_values = hourly.get('temperature_2m', {})
#
#             if temperature_2m_values:
#                 # Calculate the average temperature for the next 7 days
#                 temperatures_2pm = hourly['temperature_2m'][14:165:24]  # Extracting temperatures at 2:00 PM for the next 7 days
#                 average_temperature_2pm = sum(temperatures_2pm) / len(temperatures_2pm)
#
#                 # Append district information and average temperature to the list
#                 district_temperatures.append({
#                     'district': district['name'],
#                     'latitude': latitude,
#                     'longitude': longitude,
#                     'average_temperature_2pm': average_temperature_2pm
#                 })
#
#     # Sort the list based on average temperature and get the coolest 10 districts
#     coolest_districts = sorted(district_temperatures, key=lambda x: x['average_temperature_2pm'])[:10]
#
#     response_data = {"coolest_districts": coolest_districts}
#
#     return JsonResponse(response_data)

