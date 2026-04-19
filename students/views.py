from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tutor, Estudiante, Parentesco
from .forms import TutorForm,EstudianteForm
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q


@login_required
def registrar_tutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)

        if form.is_valid():
            
            tutor = form.save() 
            messages.success(request, "Tutor registrado correctamente.")
            
            base_url = reverse('list_tutores')
            return redirect(f"{base_url}?nuevo_tutor_id={tutor.pk}")
            
        else:
            messages.error(request, "Error en el formulario. Verifique los datos.")

    else:
        form = TutorForm()
    
    return render(request, 'Tutor/form_tutor.html', {'form': form})

@login_required
def list_tutores(request):
    query = request.GET.get('search', '')
    
    tutores = Tutor.objects.filter(estado=True).order_by('apellidos')
    
    if query:
        tutores = tutores.filter(
            Q(nombres__icontains=query) | 
            Q(apellidos__icontains=query) | 
            Q(cedula_identidad__icontains=query) |
            Q(ocupacion__icontains=query)
        ).distinct()
        
    return render(request, 'Tutor/list_tutores.html', {
        'tutores': tutores,
        'search_query': query
    })


@login_required
def editar_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)

    ci_parts = tutor.cedula_identidad.split('-')
    initial_data = {
        'ci_nro': ci_parts[0],
        'ci_comp': ci_parts[1] if len(ci_parts) == 3 else '',
        'ci_exp': ci_parts[-1],
    }

    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor, initial=initial_data)
        
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, f"Datos de {tutor.nombres} {tutor.apellidos} actualizados correctamente.")
            else:
                messages.info(request, "No se detectaron modificaciones en el formulario.")
                
            return redirect('list_tutores')
            
        else:
        
            print("Errores del formulario:", form.errors)
            messages.error(request, "Error de validación. Revisa los datos ingresados.")
            
    else:
        form = TutorForm(instance=tutor, initial=initial_data)

    return render(request, 'Tutor/form_tutor.html', {
        'form': form,
        'edit_mode': True,
        'tutor': tutor
    })


@login_required
def eliminar_tutor(request, pk):
    tutor = get_object_or_404(Tutor, pk=pk)
    
 
    if tutor.tiene_estudiantes:
        messages.error(request, f"El tutor {tutor.nombres} {tutor.apellidos} no se puede eliminar porque tiene estudiantes asociados.")
        return redirect('list_tutores')
 
    tutor.estado = False
    tutor.fecha_baja = timezone.now() 
    tutor.save()
    
    messages.warning(request, f"El tutor {tutor.nombres} fue enviado a la papelera. Se eliminará definitivamente en 30 días.")
    return redirect('list_tutores')

# @login_required
# def crear_estudiante(request):
#     tutor_id = request.GET.get('tutor_id')
#     tutor_obj = None
#     mostrar_pregunta = False

#     if tutor_id:
#         try:
#             tutor_obj = Tutor.objects.get(pk=tutor_id)
#         except Tutor.DoesNotExist:
#             tutor_obj = None
#     else:
#         mostrar_pregunta = True

#     context = {
#         'tutor_seleccionado': tutor_obj,
#         'mostrar_pregunta': mostrar_pregunta,
#     }
#     return render(request, 'Student/form_student.html', context)

@login_required
def list_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'Student/list_estudiantes.html', {'estudiantes': estudiantes})

#REGISTRAR ESTUDIANTE 

@login_required
def crear_estudiante(request):
    # Intentamos obtener el tutor_id del GET (cuando carga la página) 
    # o del POST (cuando se envía el formulario)
    tutor_id = request.GET.get('tutor_id') or request.POST.get('tutor_id')
    tutor_guardar = None
    mostrar_pregunta = False

    if tutor_id:
        try:
            tutor_guardar = Tutor.objects.get(pk=tutor_id)
        except Tutor.DoesNotExist:
            tutor_guardar = None
    else:
        mostrar_pregunta = True

    if request.method == "POST":
        form = EstudianteForm(request.POST)

        if not tutor_guardar:
            messages.error(request, "Error de seguridad: Se requiere un tutor para registrar al estudiante.")
            return redirect("list_tutores")

        if form.is_valid():
    
            nuevo_estudiante = form.save()
            
            tipo_relacion = request.POST.get('relacion', 'Apoderado')

            Parentesco.objects.create(
                estudiante=nuevo_estudiante,
                tutor=tutor_guardar,
                relacion=tipo_relacion
            )

            messages.success(request, "Estudiante y Tutor vinculados y registrados correctamente.")   
            return redirect("list_estudiantes")
        else:
            messages.error(request, "Error en el formulario. Verifique los datos.") 
    else:
        form = EstudianteForm()

    context = {
        'form': form,  
        'tutor_seleccionado': tutor_guardar,
        'mostrar_pregunta': mostrar_pregunta,
    }

    return render(request, 'Student/form_student.html', context)