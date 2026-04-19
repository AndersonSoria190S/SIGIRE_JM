from django.utils import timezone
from datetime import timedelta
from students.models import Tutor 

def vaciar_papelera_tutores():
  
    hace_30_dias = timezone.now() - timedelta(days=30)
    

    tutores_vencidos = Tutor.objects.filter(
        estado=False,
        fecha_baja__isnull=False,
        fecha_baja__lt=hace_30_dias
    )
    
    eliminados = 0
    for tutor in tutores_vencidos:
        if not tutor.tiene_estudiantes:
            tutor.delete()
            eliminados += 1
            
    print(f"Limpieza completada: {eliminados} tutores eliminados permanentemente de la BD.")