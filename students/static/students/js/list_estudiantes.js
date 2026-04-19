document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const generoFilter = document.getElementById('generoFilter');
    const toggleInactivos = document.getElementById('toggleInactivos');
    const hiddenInactivos = document.getElementById('hiddenInactivos');

    let typingTimer;

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                searchForm.submit();
            }, 500);
        });

        const val = searchInput.value;
        searchInput.value = '';
        searchInput.value = val;
        searchInput.focus();
    }

    if (generoFilter) {
        generoFilter.addEventListener('change', () => {
            searchForm.submit();
        });
    }

    if (toggleInactivos) {
        toggleInactivos.addEventListener('change', function() {
            hiddenInactivos.value = this.checked ? 'on' : '';
            searchForm.submit();
        });
    }

    const deactivateBtns = document.querySelectorAll('.sweet-deactivate');
    deactivateBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            const nombre = this.getAttribute('data-nombre');

            Swal.fire({
                title: '¿Desactivar estudiante?',
                text: `${nombre} pasará a la lista de inactivos y no podrá ser inscrito en la gestión actual.`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#f59e0b', 
                cancelButtonColor: '#64748b',
                confirmButtonText: 'Sí, desactivar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) window.location.href = url;
            });
        });
    });

    const deleteDbBtns = document.querySelectorAll('.sweet-delete-db');
    deleteDbBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            const nombre = this.getAttribute('data-nombre');
            const inscrito = this.getAttribute('data-inscrito') === 'true';
            const tieneHermanos = this.getAttribute('data-hermanos') === 'true';

            if (inscrito) {
                Swal.fire({
                    icon: 'error',
                    title: 'Acción Denegada',
                    text: `El estudiante ${nombre} tiene registros académicos (Inscripciones). Por seguridad, no puede ser eliminado de la base de datos.`,
                    confirmButtonColor: '#1e293b'
                });
                return;
            }
            if (tieneHermanos) {
                Swal.fire({
                    icon: 'error',
                    title: 'Acción Restringida',
                    text: `No se puede eliminar a ${nombre} porque su tutor tiene otros estudiantes a cargo (Hermanos). Desactívelo en su lugar.`,
                    confirmButtonColor: '#1e293b'
                });
                return;
            }

            Swal.fire({
                title: '¿Borrar definitivamente?',
                html: `Está a punto de eliminar a <strong>${nombre}</strong>.<br><br><span style="color:#c62828;"><strong>¡Atención!</strong> Como es el único estudiante de su tutor, <strong>el tutor también será eliminado</strong> permanentemente del sistema.</span>`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#c62828',
                cancelButtonColor: '#64748b',
                confirmButtonText: '<i class="fa-solid fa-trash-can"></i> Sí, eliminar ambos',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) window.location.href = url;
            });
        });
    });
});