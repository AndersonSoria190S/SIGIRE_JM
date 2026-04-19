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
    niveles = Nivel.objects.filter(estado=True)
    grados = Grado.objects.filter(estado=True).select_related('nivel')
    paralelos = Paralelo.objects.filter(estado=True).select_related('grado__nivel')

    grados_ocupados = list(Paralelo.objects.filter(estado=True).values_list('grado_id', flat=True).distinct())

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

        'grados_ocupados': grados_ocupados, 
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
    
  
    tipo_registro = request.GET.get('tipo')

    if request.method == 'POST':
       
        if tipo_registro == 'nivel' or 'btn_guardar_nivel' in request.POST:
            form_nivel = NivelForm(request.POST)
            if form_nivel.is_valid():
                form_nivel.save()
                messages.success(request, "¡Nivel creado exitosamente!")
                return redirect('estructura_academica')
            else:
                for error in form_nivel.non_field_errors():
                    messages.error(request, error)

        elif tipo_registro == 'grado' or 'btn_guardar_grado' in request.POST:
            

            nivel_id = request.POST.get('nivel')
            nombre = request.POST.get('nombre')
            
        
            grado_oculto = Grado.objects.filter(nivel_id=nivel_id, nombre=nombre, estado=False).first()
            
            if grado_oculto:
                
                grado_oculto.estado = True
                grado_oculto.save()
                
                
                Paralelo.objects.filter(grado=grado_oculto).update(estado=True)
                
                messages.success(request, f"¡El grado '{nombre}' ha sido restaurado exitosamente!")
                return redirect('estructura_academica')
            
       
            form_grado = GradoForm(request.POST)
            if form_grado.is_valid():
                form_grado.save()
                messages.success(request, "¡Grado creado exitosamente!")
                return redirect('estructura_academica')
            else:
                for error in form_grado.non_field_errors():
                    messages.error(request, error)
                for field, errors in form_grado.errors.items():
                    if field != '__all__': 
                        for error in errors:
                            messages.error(request, f"{error}")

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
    
    if nivel.grados.filter(estado=True).exists():
        messages.error(request, f"No se puede eliminar '{nivel.nombre}' porque tiene grados registrados. Primero debe eliminar los grados asociados.")
        return redirect('estructura_academica')
    
    nivel.estado = False
    nivel.save()
    
    messages.warning(request, f"Nivel '{nivel.nombre}' desactivado correctamente.")
    return redirect('estructura_academica')

@login_required
@only_director
def editar_grado(request, pk):
    grado = get_object_or_404(Grado, pk=pk)
    
    if grado.paralelo_set.filter(estado=True).exists():
        messages.error(request, f"El grado '{grado.nombre}' ya tiene paralelos configurados. No se puede editar para mantener la integridad de los datos.")
        return redirect('estructura_academica')
    
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
    
    if grado.paralelo_set.filter(estado=True).exists():
        messages.error(request, f"No se puede desactivar '{grado.nombre}' porque tiene paralelos activos. Elimine primero sus paralelos.")
        return redirect('estructura_academica')

   
    if Inscripcion.objects.filter(paralelo__grado=grado).exists():
        messages.error(request, f"El grado '{grado.nombre}' tiene historial de alumnos inscritos. No se puede desactivar.")
        return redirect('estructura_academica')

    grado.estado = False
    grado.save()
    
    messages.warning(request, f"Grado '{grado.nombre}' desactivado correctamente.")
    return redirect('estructura_academica')

@login_required
@only_director
def crear_paralelo(request):
    if request.method == 'POST':
        form = ParaleloForm(request.POST)
        if form.is_valid():
            paralelo_temp = form.save(commit=False)
            grado_actual = paralelo_temp.grado
            
            orden_grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto']
            
            # --- 1. VERIFICACIÓN DE JERARQUÍA (Revisando solo activos) ---
            if grado_actual.nombre in orden_grados:
                indice_actual = orden_grados.index(grado_actual.nombre)
                
                if indice_actual > 0:
                    nombre_grado_anterior = orden_grados[indice_actual - 1]
                    grado_anterior = Grado.objects.filter(nivel=grado_actual.nivel, nombre=nombre_grado_anterior, estado=True).first()
                    
                    # Verificamos que el grado anterior exista y tenga paralelos ACTIVOS
                    if not grado_anterior or not Paralelo.objects.filter(grado=grado_anterior, estado=True).exists():
                        messages.error(
                            request, 
                            f"Jerarquía estricta: Debes tener al menos un paralelo activo en '{nombre_grado_anterior}' de {grado_actual.nivel.nombre} antes de abrir '{grado_actual.nombre}'."
                        )
                        return redirect('estructura_academica')
                
                elif indice_actual == 0 and grado_actual.nivel.nombre == 'Secundaria':
                    grado_sexto_primaria = Grado.objects.filter(nivel__nombre='Primaria', nombre='Sexto', estado=True).first()
                    
                    if not grado_sexto_primaria or not Paralelo.objects.filter(grado=grado_sexto_primaria, estado=True).exists():
                        messages.error(
                            request, 
                            "Jerarquía de Niveles: No puedes abrir 'Primero de Secundaria' sin tener paralelos activos hasta 'Sexto de Primaria'."
                        )
                        return redirect('estructura_academica')

            # --- 2. LÓGICA DE REACTIVACIÓN O CREACIÓN ---
            
            # A) ¿Hay algún paralelo oculto que podamos reactivar? (Buscamos el primero en orden alfabético)
            paralelo_oculto = Paralelo.objects.filter(grado=grado_actual, estado=False).order_by('letra').first()
            
            if paralelo_oculto:
                paralelo_oculto.estado = True
                paralelo_oculto.cupo_max = 30 # Reseteamos los cupos
                paralelo_oculto.save()
                messages.success(request, f"Paralelo '{paralelo_oculto.letra}' restaurado automáticamente para {grado_actual.nombre} ({grado_actual.nivel.nombre}).")
                return redirect('estructura_academica')

            # B) Si no hay ocultos, creamos uno completamente nuevo.
            # Buscamos la última letra históricamente registrada (sin importar el estado)
            ultimo_historico = Paralelo.objects.filter(grado=grado_actual).order_by('letra').last()
            
            if ultimo_historico:
                siguiente_letra = chr(ord(ultimo_historico.letra) + 1)
                if siguiente_letra > 'Z':
                    messages.error(request, f"¡Límite máximo de paralelos alcanzado para {grado_actual.nombre}!")
                    return redirect('estructura_academica')
                paralelo_temp.letra = siguiente_letra
            else:
                paralelo_temp.letra = 'A'

            paralelo_temp.cupo_max = 30 
            paralelo_temp.estado = True
            paralelo_temp.save()
            
            messages.success(request, f"Paralelo '{paralelo_temp.letra}' generado automáticamente para {grado_actual.nombre} ({grado_actual.nivel.nombre}).")
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
        messages.error(request, f"No puedes desactivar el paralelo '{paralelo.letra}' de {grado_actual.nombre} porque ya tiene alumnos inscritos.")
        return redirect('estructura_academica')

    ultimo_paralelo_activo = Paralelo.objects.filter(grado=grado_actual, estado=True).order_by('letra').last()
    
    if paralelo.letra != ultimo_paralelo_activo.letra:
        messages.error(request, f"Secuencia estricta: Para desactivar la letra '{paralelo.letra}', primero debes desactivar el paralelo '{ultimo_paralelo_activo.letra}'.")
        return redirect('estructura_academica')


    cantidad_paralelos_activos = Paralelo.objects.filter(grado=grado_actual, estado=True).count()
    if cantidad_paralelos_activos == 1:
        orden_grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto']
        
        if grado_actual.nombre in orden_grados:
            indice_actual = orden_grados.index(grado_actual.nombre)
            
            if indice_actual < len(orden_grados) - 1:
                grado_siguiente_nombre = orden_grados[indice_actual + 1]
                grado_siguiente = Grado.objects.filter(nivel=grado_actual.nivel, nombre=grado_siguiente_nombre, estado=True).first()
                
              
                if grado_siguiente and Paralelo.objects.filter(grado=grado_siguiente, estado=True).exists():
                    messages.error(
                        request, 
                        f"Jerarquía: No puedes vaciar '{grado_actual.nombre}' porque '{grado_siguiente_nombre}' ya tiene paralelos activos dependientes."
                    )
                    return redirect('estructura_academica')
            
            elif indice_actual == 5 and grado_actual.nivel.nombre == 'Primaria':
                primero_secundaria = Grado.objects.filter(nivel__nombre='Secundaria', nombre='Primero', estado=True).first()
                if primero_secundaria and Paralelo.objects.filter(grado=primero_secundaria, estado=True).exists():
                    messages.error(
                        request, 
                        "Jerarquía de Niveles: No puedes vaciar 'Sexto de Primaria' porque 'Primero de Secundaria' ya tiene paralelos activos."
                    )
                    return redirect('estructura_academica')


    nombre_completo = f"{grado_actual.nombre} '{paralelo.letra}' ({grado_actual.nivel.nombre})"
    paralelo.estado = False
    paralelo.save()
    
    messages.warning(request, f"Paralelo {nombre_completo} desactivado correctamente.")
    return redirect('estructura_academica')