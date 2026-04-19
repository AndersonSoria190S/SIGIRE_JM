document.addEventListener("DOMContentLoaded", function() {

    // 1. SELECTORES PRINCIPALES
    // Buscamos el formulario específicamente dentro de la card de estudiante para evitar confusiones
    const studentForm = document.querySelector('.student-form-card form');
    const btnSave = document.querySelector('.btn-save-student');

    // 2. LÓGICA DE EDICIÓN (BLOQUEO DE BOTÓN)
    // Usamos la variable 'esEdicion' que inyectamos desde el HTML
    if (typeof configEstudiante !== 'undefined' && configEstudiante.esEdicion && btnSave) {
        
        // Estado inicial: Desactivado
        btnSave.disabled = true;
        btnSave.style.opacity = '0.5';
        btnSave.style.cursor = 'not-allowed';

        const habilitarBoton = () => {
            btnSave.disabled = false;
            btnSave.style.opacity = '1';
            btnSave.style.cursor = 'pointer';
            btnSave.style.transform = 'scale(1)'; 
        };

        // Escuchamos CUALQUIER cambio en el formulario
        // 'input' detecta cada letra escrita, 'change' detecta cambios en selects/fechas
        studentForm.addEventListener('input', habilitarBoton);
        studentForm.addEventListener('change', habilitarBoton);
    }

    // 3. SANITIZACIÓN (Nombres y Apellidos)
    function formatTitleCase(str) {
        return str.toLowerCase().replace(/(?:^|\s)\w/g, match => match.toUpperCase());
    }

    const textInputs = studentForm.querySelectorAll('input[name="nombres"], input[name="apellido_paterno"], input[name="apellido_materno"]');
    textInputs.forEach(input => {
        input.addEventListener('input', function() {
            let cursorPosition = this.selectionStart;
            let valorLimpio = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
            this.value = formatTitleCase(valorLimpio);
            this.setSelectionRange(cursorPosition, cursorPosition);
        });
    });

    // 4. CALENDARIO (Flatpickr)
    if (typeof flatpickr !== 'undefined') {
        flatpickr("input[name='fecha_nacimiento']", {
            locale: "es", 
            dateFormat: "Y-m-d", 
            maxDate: "today",
            disableMobile: true,
            // Al cambiar la fecha, también despertamos el botón de guardar
            onChange: function() {
                if (btnSave && configEstudiante.esEdicion) {
                    btnSave.disabled = false;
                    btnSave.style.opacity = '1';
                }
            }
        });
    }

    // 5. LÓGICA DE TUTOR (Solo si NO es edición)
    if (typeof configEstudiante !== 'undefined' && configEstudiante.mostrarPregunta && !configEstudiante.esEdicion) {
        Swal.fire({
            title: '¿Ya registró al tutor?',
            text: "Para registrar un estudiante, primero debe existir un tutor en el sistema.",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#c62828',
            confirmButtonText: 'Sí, ya está registrado',
            cancelButtonText: 'No, registrar ahora',
            allowOutsideClick: false
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = configEstudiante.urlListaTutores;
            } else {
                window.location.href = configEstudiante.urlRegistrarTutor;
            }
        });
    }
});