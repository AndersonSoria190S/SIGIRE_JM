from django import forms
from .models import Tutor, Estudiante

OPCIONES_EXPEDIDO = [
    ('LP', 'La Paz'), ('OR', 'Oruro'), ('PT', 'Potosí'),
    ('CB', 'Cochabamba'), ('SC', 'Santa Cruz'), ('BN', 'Beni'),
    ('PA', 'Pando'), ('TJ', 'Tarija'), ('CH', 'Chuquisaca')
]

class TutorForm(forms.ModelForm):
    ci_nro = forms.CharField(max_length=10, label="Número de CI")
    ci_comp = forms.CharField(max_length=2, required=False, label="Complemento")
    
    ci_exp = forms.ChoiceField(choices=OPCIONES_EXPEDIDO, label="Expedido")

    class Meta:
        model = Tutor
        fields = ['nombres', 'apellidos', 'ocupacion', 'celular'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            if 'ci_nro' in self.fields: self.fields['ci_nro'].disabled = True
            if 'ci_comp' in self.fields: self.fields['ci_comp'].disabled = True
            if 'ci_exp' in self.fields: self.fields['ci_exp'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        

        if self.instance and self.instance.pk:
            return cleaned_data
            
        ci_nro = cleaned_data.get('ci_nro')
        ci_comp = cleaned_data.get('ci_comp')
        ci_exp = cleaned_data.get('ci_exp')
        
        if ci_nro and ci_exp:
            cedula = f"{ci_nro}-{ci_comp}-{ci_exp}" if ci_comp else f"{ci_nro}-{ci_exp}"
            
            from .models import Tutor
            if Tutor.objects.filter(cedula_identidad=cedula).exists():
                raise forms.ValidationError("Este CI ya está registrado en el sistema.")
            
            cleaned_data['cedula_identidad'] = cedula
            
        return cleaned_data

    def save(self, commit=True):
        tutor = super().save(commit=False)
        
        if not (self.instance and self.instance.pk):
            tutor.cedula_identidad = self.cleaned_data.get('cedula_identidad')

        if commit:
            tutor.save()

        return tutor

    
class EstudianteForm(forms.ModelForm):
    ci_nro = forms.CharField(max_length=10, label="Número de CI")
    ci_comp = forms.CharField(max_length=2, required=False, label="Complemento")
    ci_exp = forms.ChoiceField(choices=OPCIONES_EXPEDIDO, label="Expedido")
    
    zona = forms.CharField(max_length=100)
    avenida = forms.CharField(max_length=100)
    num_puerta = forms.CharField(max_length=10)  
    
    class Meta:
          model = Estudiante
          fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'genero', 'correo_electronico', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.es_edicion = False
        
        if self.instance and self.instance.pk:
            self.es_edicion = True
            if 'ci_nro' in self.fields: self.fields['ci_nro'].disabled = True
            if 'ci_comp' in self.fields: self.fields['ci_comp'].disabled = True
            if 'ci_exp' in self.fields: self.fields['ci_exp'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        
    
        if not self.es_edicion:
            ci_nro = cleaned_data.get('ci_nro')
            ci_comp = cleaned_data.get('ci_comp')
            ci_exp = cleaned_data.get('ci_exp')
            
            if ci_nro and ci_exp:
                
                cedula = f"{ci_nro}-{ci_comp}-{ci_exp}" if ci_comp else f"{ci_nro}-{ci_exp}"
                
                if Estudiante.objects.filter(cedula_identidad=cedula).exists():
                    raise forms.ValidationError("El CI de este estudiante ya está registrado.")
                
                cleaned_data['cedula_identidad'] = cedula
                
        return cleaned_data

    def save(self, commit=True):
        estudiante = super().save(commit=False)

        if not self.es_edicion:
            estudiante.cedula_identidad = self.cleaned_data.get('cedula_identidad')
            
        zona = self.cleaned_data.get("zona", "")
        avenida = self.cleaned_data.get("avenida", "")
        numero_puerta = self.cleaned_data.get("num_puerta", "")

        estudiante.direccion = f"{zona}, {avenida}, N° {numero_puerta}"

        if commit:
            estudiante.save()

        return estudiante
    
class EditarEstudianteForm(forms.ModelForm):
    zona = forms.CharField(max_length=100)
    avenida = forms.CharField(max_length=100)
    num_puerta = forms.CharField(max_length=10, required=False) 

    class Meta:
        model = Estudiante
        
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 
            'fecha_nacimiento', 'genero', 'correo_electronico'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }