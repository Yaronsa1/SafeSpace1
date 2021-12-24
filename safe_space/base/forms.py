from django.forms import ModelForm
from base.models import Place

class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        exclude = ['owner']