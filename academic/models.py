from django.db import models
from django.core.exceptions import ValidationError

# Clases para el manejo de Nivel, Grado, Gestion y Paralelo

#CLASE NIVEL
class Nivel(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

#CLASE GRADO
class Grado(models.Model):
    # Definimos los nombres permitidos
    NOMBRES_GRADOS = [
        ('Primero', 'Primero'),
        ('Segundo', 'Segundo'),
        ('Tercero', 'Tercero'),
        ('Cuarto', 'Cuarto'),
        ('Quinto', 'Quinto'),
        ('Sexto', 'Sexto'),
    ]

    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name='grados')
    nombre = models.CharField(max_length=50, choices=NOMBRES_GRADOS) # Cambiado a choices
    estado = models.BooleanField(default=True)
    
    @property
    def tiene_paralelos_activos(self):
        return self.paralelo_set.filter(estado=True).exists()

    def clean(self):
        if self.nivel_id and self.nombre: 
            if not self.pk:
               
                if Grado.objects.filter(nivel=self.nivel, estado=True).count() >= 6:
                    raise ValidationError(f"El nivel '{self.nivel.nombre}' ya completó los 6 grados activos permitidos.")
            
           
            if not self.pk and Grado.objects.filter(nivel=self.nivel, nombre=self.nombre, estado=True).exists():
                 raise ValidationError(f"El grado '{self.nombre}' ya existe y está activo en este nivel.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

#CLASE GESTION
class Gestion(models.Model):

    anio = models.IntegerField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return str(self.anio)

#CLASE PARALELO
class Paralelo(models.Model):
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='paralelos')
    letra = models.CharField(max_length=2)
    cupo_max = models.PositiveIntegerField(default=30)
    estado = models.BooleanField(default=True)
    
    @property
    def tiene_inscritos(self):
    
        return self.inscripcion_set.exists()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['grado', 'letra'], 
                name='unique_paralelo_por_grado',
                violation_error_message="Este paralelo ya existe para el grado seleccionado."
            )
        ]
        ordering = ['grado', 'letra']

    def __str__(self):
        return f"{self.grado.nombre} ({self.grado.nivel.nombre}) - Paralelo {self.letra}"
