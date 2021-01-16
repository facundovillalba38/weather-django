import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm 

# Create your views here.
def index(request):
     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=90a6dfd1a2b32729ec845c1c0a8e5f3f'
     
     err_msg = ''
     message = ''
     message_class = ''

     if request.method == 'POST':
          form = CityForm(request.POST)


          if form.is_valid(): # Valida que no este cargada la ciudad que se esta ingresando
               new_city = form.cleaned_data['name']
               existing_city = City.objects.filter(name = new_city).count() #0 no existe en la base, por lo que la puede guardar. 1 existe, asi que tira mensaje de error
               if existing_city == 0:
                    r = requests.get(url.format(new_city)).json() # obtiene info de la ciudad a ingresar antes que se guarde, para verificar que sea valida en la API
                    if r['cod'] == 200:
                         form.save() # Guarda en la base de datos si se carga una nueva ciudad
                    else:
                         err_msg = 'That is not a valid city.'
                    
               else:
                    err_msg = 'City already exists in the database.'
          if err_msg:
               message = err_msg
               message_class = 'is-danger'
          else:
               message = 'City added successfully.'
               message_class = 'is-success'

     print(err_msg)

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

     context = {
          'weather_data': weather_data,
          'form' : form,
          'message' : message,
          'message_class':message_class
     }

     return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
     City.objects.get(name=city_name).delete()

     return redirect('home')
