from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Requisito, EntregaDocumento

@login_required
def registrar_inscripcion_view(request):
    context = {
        'gestion_actual': '2026',
        'estudiante': {
            'nombres': 'Ronaldo Antonio',
            'apellido_paterno': 'Mamani',
            'apellido_materno': 'Cruz',
            'cedula_identidad': '27382332 PT'
        }
    }
    return render(request, 'Inscriptions/form_enrollment.html', context)

@login_required
def list_inscripciones(request):
    return render(request, 'Inscriptions/list_of_subscribers.html')

@require_POST
def crear_requisito(request):
    nombre = request.POST.get('nombre_documento')
    
    if nombre:
        Requisito.objects.create(nombre_documento=nombre)
        messages.success(request, f"Requisito '{nombre}' registrado correctamente.")
    else:
        messages.error(request, "El nombre del documento no puede estar vacío.")
        
    return redirect('estructura_academica')

def eliminar_requisito(request, pk):
    requisito = get_object_or_404(Requisito, pk=pk)
    nombre = requisito.nombre_documento
    
    existe_en_entregas = EntregaDocumento.objects.filter(requisito=requisito).exists()
    
    if existe_en_entregas:
        requisito.estado = False
        requisito.save()
        messages.warning(request, f"El requisito '{nombre}' se ha desactivado (no se eliminó físicamente por integridad de datos).")
    else:
        requisito.delete()
        messages.success(request, f"Requisito '{nombre}' eliminado físicamente con éxito.")
        
    return redirect('estructura_academica')

def editar_requisito(request, pk):
    requisito = get_object_or_404(Requisito, pk=pk)
    if request.method == "POST":
        nuevo_nombre = request.POST.get('nombre_documento')
        if nuevo_nombre:
            requisito.nombre_documento = nuevo_nombre
            requisito.save()
            messages.success(request, "Requisito actualizado correctamente.")
        return redirect('estructura_academica')
    
    return render(request, 'Inscriptions/edit_requirement.html', {'requisito': requisito})