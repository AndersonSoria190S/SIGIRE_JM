document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Estética de inputs
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(el => el.classList.add('form-control-academic'));

    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const btnSubmit = form.querySelector('button[type="submit"]');
        if (!btnSubmit) return;

        // --- LÓGICA DE BOTÓN INTELIGENTE (Desactivado si no hay cambios) ---
        const getSnapshot = () => {
            const data = new FormData(form);
            const obj = {};
            for (let [key, value] of data.entries()) {
                if (key !== 'csrfmiddlewaretoken') {
                    obj[key] = value.toString().trim();
                }
            }
            return obj;
        };

        const snapshot = getSnapshot();

        const verificarCambios = () => {
            const currentValues = getSnapshot();
            let huboCambios = false;

            for (const key in snapshot) {
                if (snapshot[key] !== currentValues[key]) {
                    huboCambios = true;
                    break;
                }
            }
            
            if (btnSubmit.classList.contains('btn-edit')) {
                btnSubmit.disabled = !huboCambios;
                btnSubmit.style.opacity = huboCambios ? "1" : "0.6";
            }
        };

        form.addEventListener('input', verificarCambios);
        form.addEventListener('change', verificarCambios);
        verificarCambios(); 

        // --- LÓGICA DE ENVÍO (Interceptamos solo para confirmar) ---
        form.addEventListener('submit', function(e) {
            // Nota: Si el código llega hasta aquí, significa que el navegador 
            // YA validó que no haya campos vacíos (gracias a quitar novalidate).
            
            e.preventDefault(); 
            const isEdit = btnSubmit.classList.contains('btn-edit');
            
            Swal.fire({
                title: isEdit ? '¿Guardar cambios?' : '¿Confirmar registro?',
                text: isEdit ? 'Se actualizará la información en la base de datos.' : 'Se creará este nuevo elemento.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3b82f6',
                cancelButtonColor: '#64748b',
                confirmButtonText: 'Sí, continuar',
                cancelButtonText: 'Cancelar',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {
                    btnSubmit.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Procesando...';
                    btnSubmit.disabled = true;
                    form.submit();
                }
            });
        });
    });
});