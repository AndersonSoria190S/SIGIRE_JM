from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import only_director 
from .models import Nivel, Grado, Gestion, Paralelo
from .forms import NivelForm, GradoForm, ParaleloForm
from django.utils import timezone
from enrollment.models import Inscripcion


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
        'form_paralelo': ParaleloForm(),
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

@login_required
@only_director
def crear_nivel_grado(request): 
    form_nivel = NivelForm()
    form_grado = GradoForm()

    if request.method == 'POST':
        if 'btn_guardar_nivel' in request.POST:
            form_nivel = NivelForm(request.POST)
            if form_nivel.is_valid():
                form_nivel.save()
                messages.success(request, "¡Nivel creado exitosamente!")
                return redirect('crear_nivel_grado')
                
        elif 'btn_guardar_grado' in request.POST:
            form_grado = GradoForm(request.POST)
            if form_grado.is_valid():
                form_grado.save()
                messages.success(request, "¡Grado creado exitosamente!")
                return redirect('estructura_academica')

    context = {
        'form_nivel': form_nivel,
        'form_grado': form_grado,
    }
    return render(request, 'Structure/form_nivel_grade.html', context)

@login_required
@only_director
def editar_nivel(request, pk):
    nivel = get_object_or_404(Nivel, pk=pk)
    if request.method == 'POST':
        form = NivelForm(request.POST, instance=nivel)
        if form.is_valid():
            form.save()
            messages.success(request, f"Nivel '{nivel.nombre}' actualizado.")
            return redirect('estructura_academica')
    else:
        form = NivelForm(instance=nivel)
    context = {
        'form_nivel': form,
        'form_grado': GradoForm(), 
        'editando': True
    }
    return render(request, 'Structure/form_nivel_grade.html', context)

@login_required
@only_director
def eliminar_nivel(request, pk):
    nivel = get_object_or_404(Nivel, pk=pk)
    
    hay_inscritos = Inscripcion.objects.filter(paralelo__grado__nivel=nivel).exists()
    
    if hay_inscritos:
        messages.error(request, f"No se puede eliminar '{nivel.nombre}' porque ya tiene alumnos inscritos en sus grados.")
        return redirect('estructura_academica')
        
    nombre = nivel.nombre
    nivel.delete()
    messages.warning(request, f"Nivel '{nombre}' eliminado correctamente.")
    return redirect('estructura_academica')

@login_required
@only_director
def editar_grado(request, pk):
    grado = get_object_or_404(Grado, pk=pk)
    if request.method == 'POST':
        form = GradoForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()
            messages.success(request, f"Grado '{grado.nombre}' actualizado correctamente.")
            return redirect('estructura_academica')
    else:
        form = GradoForm(instance=grado)
    
    context = {
        'form_grado': form,
        'form_nivel': NivelForm(),
        'editando_grado': True
    }
    return render(request, 'Structure/form_nivel_grade.html', context)

@login_required
@only_director
def eliminar_grado(request, pk):
    grado = get_object_or_404(Grado, pk=pk)
    
    hay_inscritos = Inscripcion.objects.filter(paralelo__grado=grado).exists()
    
    if hay_inscritos:
        messages.error(request, f"El grado '{grado.nombre}' está bloqueado. Tiene alumnos inscritos y no se puede borrar.")
        return redirect('estructura_academica')
        
    nombre = grado.nombre
    grado.delete()
    messages.warning(request, f"Grado '{nombre}' eliminado.")
    return redirect('estructura_academica')

@login_required
@only_director
def crear_paralelo(request):
    if request.method == 'POST':
        form = ParaleloForm(request.POST)
        if form.is_valid():
            paralelo = form.save(commit=False)
            grado_actual = paralelo.grado
            
            orden_grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto']
            
            if grado_actual.nombre in orden_grados:
                indice_actual = orden_grados.index(grado_actual.nombre)
                
                if indice_actual > 0:
                    nombre_grado_anterior = orden_grados[indice_actual - 1]
                    grado_anterior = Grado.objects.filter(nivel=grado_actual.nivel, nombre=nombre_grado_anterior).first()
                    
                    if not grado_anterior or not Paralelo.objects.filter(grado=grado_anterior).exists():
                        messages.error(
                            request, 
                            f"Jerarquía estricta: Debes tener al menos un paralelo en '{nombre_grado_anterior}' de {grado_actual.nivel.nombre} antes de abrir '{grado_actual.nombre}'."
                        )
                        return redirect('estructura_academica')
                
                elif indice_actual == 0 and grado_actual.nivel.nombre == 'Secundaria':
                    grado_sexto_primaria = Grado.objects.filter(nivel__nombre='Primaria', nombre='Sexto').first()
                    
                    if not grado_sexto_primaria or not Paralelo.objects.filter(grado=grado_sexto_primaria).exists():
                        messages.error(
                            request, 
                            "Jerarquía de Niveles: No puedes abrir 'Primero de Secundaria' sin tener la jerarquía completa hasta 'Sexto de Primaria'."
                        )
                        return redirect('estructura_academica')

            ultimo = Paralelo.objects.filter(grado=paralelo.grado).order_by('letra').last()
            
            if ultimo:
                siguiente_letra = chr(ord(ultimo.letra) + 1)
                if siguiente_letra > 'Z':
                    messages.error(request, f"¡Límite máximo de paralelos alcanzado para {grado_actual.nombre}!")
                    return redirect('estructura_academica')
                paralelo.letra = siguiente_letra
            else:
                paralelo.letra = 'A'

            paralelo.cupo_max = 30 
            paralelo.save()
            
            messages.success(request, f"Paralelo '{paralelo.letra}' generado automáticamente para {grado_actual.nombre} de {grado_actual.nivel.nombre}.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error: {error}")
            
    return redirect('estructura_academica')

@login_required
@only_director
def eliminar_paralelo(request, pk):
    paralelo = get_object_or_404(Paralelo, pk=pk)
    grado_actual = paralelo.grado

    if Inscripcion.objects.filter(paralelo=paralelo).exists():
        messages.error(request, f"No puedes eliminar el paralelo '{paralelo.letra}' de {grado_actual.nombre} porque ya tiene alumnos inscritos.")
        return redirect('estructura_academica')

 
    ultimo_paralelo = Paralelo.objects.filter(grado=grado_actual).order_by('letra').last()
    if paralelo.letra != ultimo_paralelo.letra:
        messages.error(request, f"Secuencia: Para eliminar la letra '{paralelo.letra}', primero debes eliminar el paralelo '{ultimo_paralelo.letra}'.")
        return redirect('estructura_academica')

    cantidad_paralelos = Paralelo.objects.filter(grado=grado_actual).count()
    if cantidad_paralelos == 1:
        orden_grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto']
        
        if grado_actual.nombre in orden_grados:
            indice_actual = orden_grados.index(grado_actual.nombre)
            
            if indice_actual < len(orden_grados) - 1:
                grado_siguiente_nombre = orden_grados[indice_actual + 1]
                grado_siguiente = Grado.objects.filter(nivel=grado_actual.nivel, nombre=grado_siguiente_nombre).first()
                
                if grado_siguiente and Paralelo.objects.filter(grado=grado_siguiente).exists():
                    messages.error(
                        request, 
                        f"Jerarquía: No puedes dejar '{grado_actual.nombre}' vacío porque '{grado_siguiente_nombre}' ya tiene paralelos activos."
                    )
                    return redirect('estructura_academica')
            
            elif indice_actual == 5 and grado_actual.nivel.nombre == 'Primaria':
                primero_secundaria = Grado.objects.filter(nivel__nombre='Secundaria', nombre='Primero').first()
                if primero_secundaria and Paralelo.objects.filter(grado=primero_secundaria).exists():
                    messages.error(
                        request, 
                        "Jerarquía de Niveles: No puedes vaciar 'Sexto de Primaria' porque 'Primero de Secundaria' ya tiene paralelos activos."
                    )
                    return redirect('estructura_academica')

    nombre_completo = f"{grado_actual.nombre} '{paralelo.letra}' ({grado_actual.nivel.nombre})"
    paralelo.delete()
    
    messages.warning(request, f"Paralelo {nombre_completo} eliminado correctamente.")
    return redirect('estructura_academica')