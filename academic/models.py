from django.db import models

# Clases para el manejo de Nivel, Grado, Gestion y Paralelo

#CLASE NIVEL
class Nivel(models.Model):

    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

#CLASE GRADO
class Grado(models.Model):
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, related_name='grados')
    nombre = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nivel', 'nombre'], 
                name='unique_grado_por_nivel',

                violation_error_message="Ya existe este grado registrado en el nivel seleccionado."
            )
        ]

    def __str__(self):
        return f"{self.nombre} - {self.nivel.nombre}"

#CLASE GESTION
class Gestion(models.Model):

    anio = models.IntegerField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return str(self.año)

#CLASE PARALELO
class Paralelo(models.Model):
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='paralelos')
    letra = models.CharField(max_length=2)
    cupo_max = models.PositiveIntegerField(default=30)

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
