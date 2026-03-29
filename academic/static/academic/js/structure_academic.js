
function abrirModal() {
  document.getElementById('modalParalelo').style.display = 'flex';

  document.getElementById('filtro_nivel').selectedIndex = 0;
  filtrarGrados();
}

function cerrarModal() {
  document.getElementById('modalParalelo').style.display = 'none';
}

window.onclick = function (event) {
  var modal = document.getElementById('modalParalelo');
  if (event.target == modal) {
    cerrarModal();
  }
}

function filtrarGrados() {
  let nivelSelect = document.getElementById('filtro_nivel');
  let gradoSelect = document.getElementById('select_grado');

  let nivelNombre = nivelSelect.options[nivelSelect.selectedIndex].text;

  for (let i = 0; i < gradoSelect.options.length; i++) {
    let option = gradoSelect.options[i];

    if (!option.hasAttribute('data-original-text')) {
      option.setAttribute('data-original-text', option.text);
    }

    let textoOriginal = option.getAttribute('data-original-text');

    if (option.value === '') {
      option.style.display = 'block';
      continue;
    }

    if (nivelNombre === '-- Elige Nivel --') {
      option.style.display = 'none';
    }

    else if (textoOriginal.includes(nivelNombre)) {
      option.style.display = 'block';
      option.text = textoOriginal.split('-')[0].trim();
    } else {
      option.style.display = 'none';
    }
  }

  gradoSelect.value = '';
}

document.addEventListener('DOMContentLoaded', function () {
  filtrarGrados();
});