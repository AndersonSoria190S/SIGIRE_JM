function toggleSubMenu(event, submenuId) {
    event.preventDefault(); 
    
    const submenu = document.getElementById(submenuId);
    const icon = event.currentTarget.querySelector('.chevron-icon');
    
    if (submenu) {
        submenu.classList.toggle('open');
    }
    
    if (icon) {
        icon.classList.toggle('rotate');
    }
}

document.addEventListener('DOMContentLoaded', function () {
  
  document.body.addEventListener('click', function (event) {
    
    let botonEliminar = event.target.closest('.alerta-eliminar');

    if (botonEliminar) {
      event.preventDefault(); 

      let urlEliminar = botonEliminar.getAttribute('href');
      let nombreItem = botonEliminar.getAttribute('data-nombre') || "este registro";
      let textoExtra = botonEliminar.getAttribute('data-extra') || "";

      Swal.fire({
        title: '¿Estás seguro?',
        text: textoExtra ? textoExtra : `Estás a punto de eliminar ${nombreItem}. Esta acción no se puede deshacer.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#64748b',
        confirmButtonText: '<i class="fa-solid fa-check"></i> Sí, proceder',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.href = urlEliminar;
        }
      });
    }
  });

});