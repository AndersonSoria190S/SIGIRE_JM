from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import only_director 
from .models import Nivel, Grado, Gestion, Paralelo
from .forms import GestionForm
from django.utils import timezone

@login_required
@only_director
def estructura_academica(request):
    gestiones = Gestion.objects.all().order_by('-anio')
    niveles = Nivel.objects.all()
    grados = Grado.objects.all().select_related('nivel')
    paralelos = Paralelo.objects.all().select_related('grado__nivel')

    anio_actual = timezone.now().year

    mostrar_btn_gestion = True
    siguiente_anio = anio_actual

    if gestiones.exists():
        ultima_gestion = gestiones.first()
        siguiente_anio = ultima_gestion.anio + 1
        
        if ultima_gestion.anio >= anio_actual:
            mostrar_btn_gestion = False

    context = {
        'gestiones': gestiones,
        'niveles': niveles,
        'grados': grados,
        'paralelos': paralelos,
        'anio_actual': anio_actual,
        'mostrar_btn_gestion': mostrar_btn_gestion,
        'siguiente_anio': siguiente_anio,
    }
    
    return render(request, 'Structure/structure_academic.html', context)

@login_required
@only_director
def toggle_gestion(request, pk):
  
    gestion = get_object_or_404(Gestion, pk=pk)
    año_actual = timezone.now().year
    
    if not gestion.estado and gestion.año < año_actual:
        messages.error(request, f"¡Acción denegada! No puedes reabrir la Gestión {gestion.año} porque ya concluyó.")
        return redirect('estructura_academica')

    if not gestion.estado:
        Gestion.objects.update(estado=False)
        gestion.estado = True
        messages.success(request, f"¡La Gestión {gestion.año} ahora es la gestión activa!")
    else:
        gestion.estado = False
        messages.warning(request, f"Se ha cerrado la Gestión {gestion.año}.")
        
    gestion.save()
    return redirect('estructura_academica')

@login_required
@only_director
def crear_gestion(request):
    gestiones = Gestion.objects.all().order_by('-anio')
    año_actual = timezone.now().year

    nuevo_año = gestiones.first().anio + 1 if gestiones.exists() else año_actual

    Gestion.objects.all().update(estado=False)

    Gestion.objects.create(anio=nuevo_año, estado=True)

    messages.success(request, f"¡La Gestión {nuevo_año} ha sido creada y activada automáticamente!")
    return redirect('estructura_academica')