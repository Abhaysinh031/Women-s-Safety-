from django.shortcuts import render, HttpResponse



# Create your views here.

from django.shortcuts import render, HttpResponse
import requests
import json


# def home(request):

#    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

#    if x_forwarded_for:

#        ip = x_forwarded_for.split(',')[0]

#    else:

#        ip = request.META.get('REMOTE_ADDR')



#    return HttpResponse("Welcome! You are visiting from: {}".format(ip))

# API key
import requests
from django.http import HttpResponse

api_key = "91333dc4d69c4962b10cc2232d1a0d2d"
api_url = "https://ipgeolocation.abstractapi.com/v1/?api_key=91333dc4d69c4962b10cc2232d1a0d2d"

def get_ip_geolocation_data(ip_address):
    params = {
        "api_key": api_key,
        "ip_address": ip_address
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return None

# def home(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')

#     geolocation_data = get_ip_geolocation_data(ip)

#     if geolocation_data:
#         country = geolocation_data.get('country', 'Unknown')
#         region = geolocation_data.get('region', 'Unknown')
#         response_message = f"Welcome! Your IP address is: {ip} and you are visiting from {region} in {country}"
#     else:
#         response_message = f"Welcome! Your IP address is: {ip} but geolocation data is not available."

#     return HttpResponse(response_message)
# from django.shortcuts import render, HttpResponse

def home(request):

   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

   if x_forwarded_for:

       ip = x_forwarded_for.split(',')[0]

   else:

       ip = request.META.get('REMOTE_ADDR')



   geolocation_data= get_ip_geolocation_data(ip)

#    geolocation_data = json.loads(geolocation_json)

   country = geolocation_data['country']

   region = geolocation_data['region']



   return HttpResponse("Welcome! Your IP address is: {} and you are visiting from {} in {}".format(ip, country, region))

