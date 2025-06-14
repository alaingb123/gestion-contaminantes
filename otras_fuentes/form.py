from django import forms
from Contaminantes.models import Liquidos

class LiquidosForm(forms.ModelForm):
    class Meta:
        model = Liquidos
        fields = '__all__'  # O especifica los campos que deseas incluir