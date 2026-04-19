document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formTutor');
    if (!form) return;

    const isEditMode = form.getAttribute('data-edit-mode') === 'true';

    if (isEditMode) {
        const btnGuardar = document.getElementById('btnGuardar');
        const inputs = form.querySelectorAll('input:not([readonly]), select:not([disabled])');
        const estadoOriginal = {};

        inputs.forEach(input => {
            estadoOriginal[input.name] = input.value;
        });

        function desactivarBoton() {
            btnGuardar.disabled = true;
            btnGuardar.classList.add('btn-disabled');
            btnGuardar.innerHTML = '<i class="fa-solid fa-lock"></i> Sin cambios detectados';
        }

        function activarBoton() {
            btnGuardar.disabled = false;
            btnGuardar.classList.remove('btn-disabled');
            btnGuardar.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Guardar Cambios';
        }

        desactivarBoton();

        form.addEventListener('input', function() {
            let formCambio = false;
            inputs.forEach(input => {
                if (input.value !== estadoOriginal[input.name]) {
                    formCambio = true;
                }
            });

            if (formCambio) {
                activarBoton();
            } else {
                desactivarBoton();
            }
        });
    }

    function formatTitleCase(str) {
        return str.toLowerCase().replace(/(?:^|\s)\w/g, function(match) {
            return match.toUpperCase();
        });
    }

 
    const textFields = ['nombres', 'apellidos', 'ocupacion'];
    textFields.forEach(fieldName => {
        const input = form.querySelector(`input[name="${fieldName}"]`);
        if (input) {
            input.addEventListener('input', function() {
               
                let valorLimpio = this.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
               
                this.value = formatTitleCase(valorLimpio);
            });
        }
    });


    const inputCiNro = form.querySelector('input[name="ci_nro"]');
    if (inputCiNro) {
        inputCiNro.addEventListener('input', function() {
          
            this.value = this.value.replace(/[^0-9]/g, '').substring(0, 10);
        });

        inputCiNro.addEventListener('blur', function() {
            if (this.value.length > 0 && this.value.length < 8) {
                this.setCustomValidity('El CI debe tener al menos 8 números.');
                this.reportValidity(); 
            } else {
                this.setCustomValidity('');
            }
        });
    }

    const inputCiComp = form.querySelector('input[name="ci_comp"]');
    if (inputCiComp) {
        inputCiComp.addEventListener('input', function() {
            let val = this.value.toUpperCase(); 
            
            if (val.length === 1) {
               
                val = val.replace(/[^A-Z]/g, '');
            } else if (val.length >= 2) {
                
                let primera = val.charAt(0).replace(/[^A-Z]/g, '');
                let segunda = val.charAt(1).replace(/[^0-9]/g, '');
                val = primera + segunda;
            }
            this.value = val;
        });
    }

    const inputCelular = form.querySelector('input[name="celular"]');
    if (inputCelular) {
        inputCelular.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '').substring(0, 8);
        });

        inputCelular.addEventListener('blur', function() {
            const val = this.value;
            if (val.length > 0) {
                if (val.length !== 8 || !(val.startsWith('6') || val.startsWith('7'))) {
                    this.setCustomValidity('Debe ser un celular boliviano válido (8 dígitos, empezando con 6 o 7).');
                    this.reportValidity();
                } else {
                    this.setCustomValidity('');
                }
            }
        });
    }
});