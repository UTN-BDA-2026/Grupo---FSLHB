// tabla-posiciones-home.js
// Carga y muestra la tabla de posiciones en la página principal con filtro por categoría

document.addEventListener('DOMContentLoaded', function () {
  const section = document.getElementById('tabla-posiciones-section');
  const tbody = document.getElementById('tabla-posiciones');
  if (!section || !tbody) return;

  // Centrar el card y limitar ancho de la tabla
  const card = section.querySelector('.tabla-posiciones-card');
  if (card) {
    card.style.display = 'flex';
    card.style.justifyContent = 'center';
    card.style.padding = '1rem';
  }
  const table = section.querySelector('table');
  if (table) {
    table.style.minWidth = '360px';
    table.style.maxWidth = '720px';
    table.style.width = '100%';
    // Centrar cabeceras
    const ths = table.querySelectorAll('th');
    ths.forEach(th => th.style.textAlign = 'center');
  }

  // Selector de categoría bajo el título
  const selector = document.createElement('select');
  selector.id = 'categoria-posiciones-selector';
  selector.style.display = 'block';
  selector.style.margin = '0.5rem 0 1rem 0';
  selector.innerHTML = '<option value="">Todas las categorías</option>' +
    ['Damas A', 'Damas B', 'Damas C', 'Caballeros', 'Mamis']
      .map(cat => `<option value="${cat}">${cat}</option>`)
      .join('');
  const heading = section.querySelector('h2');
  if (heading) heading.insertAdjacentElement('afterend', selector);

  function renderTabla(division) {
    // Si no hay división elegida, limpiamos y mostramos un placeholder
    if (!division) {
      tbody.innerHTML = '';
      const tr = document.createElement('tr');
      const td = document.createElement('td');
      td.colSpan = 2;
      td.style.color = '#888';
      td.style.textAlign = 'center';
      td.textContent = 'Selecciona una categoría para ver posiciones';
      tr.appendChild(td);
      tbody.appendChild(tr);
      return;
    }

    tbody.innerHTML = `<tr><td colspan="2" style="color:#888;text-align:center;">Cargando...</td></tr>`;
    const params = new URLSearchParams({ division });
    fetch(`/posiciones?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        if (!Array.isArray(data) || data.length === 0) {
          tbody.innerHTML = `<tr><td colspan="2" style="color:#d32f2f;text-align:center;">No hay datos para la selección.</td></tr>`;
          return;
        }
        // Renderizar solo Equipo y Puntos
        tbody.innerHTML = data.map(r =>
          `<tr><td style="text-align:center;font-weight:600;">${r.equipo}</td><td style="text-align:center;font-weight:700;">${r.pts}</td></tr>`
        ).join('');
      })
      .catch(() => {
        tbody.innerHTML = `<tr><td colspan="2" style="color:red;text-align:center;">Error al cargar posiciones</td></tr>`;
      });
  }

  selector.addEventListener('change', () => renderTabla(selector.value));

  // Estado inicial
  renderTabla('');
});
