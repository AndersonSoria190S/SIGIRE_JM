document.addEventListener('DOMContentLoaded', function() {

    const capitalizarTexto = function() {
        let valor = this.value;
        valor = valor.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
        
        this.value = valor.split(' ').map(palabra => {
            if (palabra.length > 0) {
                return palabra.charAt(0).toUpperCase() + palabra.slice(1).toLowerCase();
            }
            return palabra;
        }).join(' ');
    };

    const inputsNombre = document.querySelector('input[name="first_name"]');
    const inputsApellido = document.querySelector('input[name="last_name"]');

    if (inputsNombre) inputsNombre.addEventListener('input', capitalizarTexto);
    if (inputsApellido) inputsApellido.addEventListener('input', capitalizarTexto);

    const celularInput = document.querySelector('input[name="celular"]');
    if (celularInput) {
        celularInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 8);
        });
    }

    const ciInput = document.querySelector('input[name="cedula_identidad"]');
    if (ciInput) {
        ciInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
        });
    }

    const complementoInput = document.querySelector('input[name="complemento"]');
    if (complementoInput) {
        complementoInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 2);
        });
    }

    const form = document.getElementById("form-personal");
    const btnSubmit = document.getElementById("btn-submit");

    if (form && btnSubmit) {
        form.addEventListener("submit", function(e) {
  
            e.preventDefault();

            const isEditMode = ciInput && ciInput.disabled;

            const swalTitle = isEditMode ? '¿Guardar cambios?' : '¿Confirmar Registro?';
            const swalText = isEditMode 
                ? 'Se actualizarán los datos de este administrativo en el sistema.' 
                : 'Se creará el usuario y se le enviarán sus credenciales por correo electrónico.';
            const confirmBtnText = isEditMode 
                ? '<i class="fa-solid fa-floppy-disk"></i> Sí, guardar cambios' 
                : '<i class="fa-solid fa-envelope-circle-check"></i> Sí, registrar y enviar';

            Swal.fire({
                title: swalTitle,
                text: swalText,
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3b82f6',
                cancelButtonColor: '#64748b',
                confirmButtonText: confirmBtnText,
                cancelButtonText: 'Cancelar',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
            
                    btnSubmit.innerHTML = isEditMode 
                        ? '<i class="fa-solid fa-circle-notch fa-spin"></i> Guardando cambios...' 
                        : '<i class="fa-solid fa-circle-notch fa-spin"></i> Procesando y enviando correo...';
                    btnSubmit.classList.add("loading");
                    btnSubmit.disabled = true;

                    form.submit();
                }
            });
        });
    }
});