
function toggleVista(checkbox) {
    if (checkbox.checked) {
        window.location.href = "?inactivos=true";
    } else {
        window.location.href = window.location.pathname;
    }
}

document.addEventListener('DOMContentLoaded', function() {

    console.log("Módulo de personal cargado...");
});