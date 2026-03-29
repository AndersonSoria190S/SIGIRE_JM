import string
from django import forms
from django.utils import timezone
from .models import Gestion, Nivel, Grado, Paralelo


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
    
class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = ['nombre']

class GradoForm(forms.ModelForm):
    
    OPCIONES_GRADOS = [
        ('Primero', 'Primero'),
        ('Segundo', 'Segundo'),
        ('Tercero', 'Tercero'),
        ('Cuarto', 'Cuarto'),
        ('Quinto', 'Quinto'),
        ('Sexto', 'Sexto'),
    ]
    
    nombre = forms.ChoiceField(
        choices=OPCIONES_GRADOS, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Grado
        fields = ['nivel', 'nombre']
        
        
class ParaleloForm(forms.ModelForm):
    nivel = forms.ModelChoiceField(
        queryset=Nivel.objects.all(),
        required=True, 
        empty_label="-- Elige Nivel --",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'filtro_nivel', 'onchange': 'filtrarGrados()'})
    )

    class Meta:
        model = Paralelo
        fields = ['grado'] 
        widgets = {
            'grado': forms.Select(attrs={'class': 'form-control', 'id': 'select_grado'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grado'].empty_label = "-- Elige Grado --"

        self.fields['grado'].choices = [('', '-- Elige Grado --')] + [
            (g.id, f"{g.nombre} - {g.nivel.nombre}") for g in Grado.objects.select_related('nivel').all()
        ]