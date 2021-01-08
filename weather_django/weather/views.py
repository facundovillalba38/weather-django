import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm 

# Create your views here.
def index(request):
     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=90a6dfd1a2b32729ec845c1c0a8e5f3f'
     
     if request.method == 'POST':
          form = CityForm(request.POST)
          form.save() # Guarda en la base de datos si se carga una nueva ciudad

     form = CityForm()

     cities = City.objects.all()

     weather_data = []

     for city in cities:
          r = requests.get(url.format(city))
          data = r.json()

          #print(data)

          city_weather = {
               'city' : city.name,
               'temperature' : data['main']['temp'],
               'description' : data['weather'][0]['description'],
               'icon' : data['weather'][0]['icon'],
          }

          print(city_weather)
          weather_data.append(city_weather)

     context = {'weather_data': weather_data, 'form' : form}

     return render(request, 'weather/weather.html', context)
