document.addEventListener('DOMContentLoaded', function () {

    const selectNivel = document.querySelector('select[name="nivel"]');
    const selectGrado = document.querySelector('select[name="grado"]');

    if (selectNivel && selectGrado && typeof gradosPorNivel !== 'undefined') {
        const defaultOption = '<option value="">---------</option>';
        
        if (!selectNivel.value) {
            selectGrado.innerHTML = defaultOption;
            selectGrado.disabled = true;
        }

    
        selectNivel.addEventListener('change', function() {
            const nivelId = this.value;
            selectGrado.innerHTML = defaultOption; 

            if (nivelId && gradosPorNivel[nivelId]) {
                
                gradosPorNivel[nivelId].forEach(grado => {
                    const option = document.createElement('option');
                    option.value = grado.id;
                    option.textContent = grado.nombre;
                    selectGrado.appendChild(option);
                });
                
                selectGrado.disabled = false;
            } else {
                
                selectGrado.disabled = true;
            }
        });
    }

    document.body.addEventListener('click', function (event) {
        const btnEliminar = event.target.closest('.alerta-eliminar');

        if (btnEliminar) {
            event.preventDefault();
            const url = btnEliminar.getAttribute('href');
            const nombre = btnEliminar.getAttribute('data-nombre') || "este elemento";
            const extra = btnEliminar.getAttribute('data-extra') || "";

            confirmarAccion(url, nombre, extra);
        }
    });
});


function confirmarAccion(url, nombre, extra) {
    if (typeof Swal === 'undefined') {
        if (confirm(`¿Está seguro de eliminar ${nombre}?`)) window.location.href = url;
        return;
    }

    Swal.fire({
        title: '¿Estás seguro?',
        text: extra || `Estás a punto de eliminar ${nombre}. Esta acción no se puede deshacer.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#64748b',
        confirmButtonText: '<i class="fa-solid fa-trash-can"></i> Sí, eliminar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true,
        focusCancel: true
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    });
}

function abrirSelectorCreacion(urlBase) {
    Swal.fire({
        title: '¿Qué desea crear?',
        text: 'Seleccione el tipo de registro académico',
        icon: 'question',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: '<i class="fa-solid fa-layer-group"></i> Crear Nivel',
        confirmButtonColor: '#0ea5e9',
        denyButtonText: '<i class="fa-solid fa-graduation-cap"></i> Crear Grado',
        denyButtonColor: '#f59e0b',
        cancelButtonText: 'Cancelar',
        cancelButtonColor: '#64748b',
        reverseButtons: false 
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = urlBase + "?tipo=nivel";
        } else if (result.isDenied) {
            window.location.href = urlBase + "?tipo=grado";
        }
    });
}

function abrirModal() {
    const modal = document.getElementById('modalParalelo');
    if (modal) {
       
        const selectNivel = modal.querySelector('select[name="nivel"]');
        const selectGrado = modal.querySelector('select[name="grado"]');
        
        if (selectNivel) selectNivel.value = "";
        if (selectGrado) {
            selectGrado.innerHTML = '<option value="">---------</option>';
            selectGrado.disabled = true;
        }

        
        modal.style.display = 'flex';
        setTimeout(() => modal.classList.add('active'), 10);
    }
}

function cerrarModal() {
    const modal = document.getElementById('modalParalelo');
    if (modal) {
       
        modal.classList.remove('active');
        
        setTimeout(() => modal.style.display = 'none', 300);
    }
}


window.addEventListener('click', (e) => {
    const modal = document.getElementById('modalParalelo');
    
    if (e.target === modal) cerrarModal();
    
});

let urlCrearRequisitoOriginal = '';
let nombreOriginalRequisito = ''; 

document.addEventListener('DOMContentLoaded', function () {
    const formRequisito = document.getElementById('formRequisito');
    const inputNombreReq = document.getElementById('inputNombreReq');
    const btnUpdateReq = document.getElementById('btnUpdateReq');

    if (formRequisito) {
        urlCrearRequisitoOriginal = formRequisito.action;
    }

    if (inputNombreReq && btnUpdateReq) {
        inputNombreReq.addEventListener('input', function() {
            if (btnUpdateReq.style.display !== 'none') {
                const valorActual = inputNombreReq.value.trim();
                if (valorActual === '' || valorActual === nombreOriginalRequisito) {
                    btnUpdateReq.disabled = true;
                } else {
                    btnUpdateReq.disabled = false;
                }
            }
        });
    }
});

function cargarEdicion(id, nombre) {
    const form = document.getElementById('formRequisito');
    const input = document.getElementById('inputNombreReq');
    const btnAdd = document.getElementById('btnAddReq');
    const btnUpdate = document.getElementById('btnUpdateReq');
    const btnCancel = document.getElementById('btnCancelReq');

    nombreOriginalRequisito = nombre.trim();

    input.value = nombreOriginalRequisito;
    input.focus();

    form.action = `/requisitos/editar/${id}/`;

    btnAdd.style.display = 'none';
    btnAdd.disabled = true;

    btnUpdate.style.display = 'flex';
    btnCancel.style.display = 'flex';

    btnUpdate.disabled = true; 
}

function cancelarEdicion() {
    const form = document.getElementById('formRequisito');
    const input = document.getElementById('inputNombreReq');
    const btnAdd = document.getElementById('btnAddReq');
    const btnUpdate = document.getElementById('btnUpdateReq');
    const btnCancel = document.getElementById('btnCancelReq');

    input.value = '';
    nombreOriginalRequisito = '';
    form.action = urlCrearRequisitoOriginal;

    btnAdd.style.display = 'flex';
    btnAdd.disabled = false;

    btnUpdate.style.display = 'none';
    btnCancel.style.display = 'none';
}