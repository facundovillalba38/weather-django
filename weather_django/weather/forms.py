from django.forms import ModelForm, TextInput
from .models import City


# Se utiliza el template del modelo creado, no es necesario crear uno personalizado
class CityForm(ModelForm):
     class Meta:
          model = City
          fields = ['name']
          widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder':'City Name'})} # Le da estilo al form