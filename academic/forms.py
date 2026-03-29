from django import forms
from django.utils import timezone
from .models import Gestion

class GestionForm(forms.ModelForm):
    class Meta:
        model = Gestion
        fields = ['anio'] 
        labels = {
            'año': 'Año Escolar (Ej. 2026)',
        }
        widgets = {
            'año': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Ej. 2026'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        año_actual = timezone.now().year
        self.fields['año'].widget.attrs['min'] = año_actual

    def clean_anio(self):
        año_ingresado = self.cleaned_data.get('anio')
        año_actual = timezone.now().year 
        
        if año_ingresado < año_actual:
            raise forms.ValidationError(f"No puedes registrar un año pasado. El año mínimo es {año_actual}.")
        
        if Gestion.objects.filter(año=año_ingresado).exists():
            raise forms.ValidationError(f"¡Atención! La gestión {año_ingresado} ya está registrada.")
            
        return año_ingresado