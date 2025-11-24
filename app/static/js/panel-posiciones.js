// panel-posiciones.js
// Renderiza la tabla de posiciones según el torneo y división seleccionados



function renderTablaPosiciones(torneo, division, fecha, bloque) {
  const container = document.getElementById('tabla-posiciones-container');
  container.innerHTML = '<div style="color:#888;">Cargando...</div>';
  const params = new URLSearchParams({ torneo, division });
  if (fecha) params.append('fecha', fecha);
  if (bloque) params.append('bloque', bloque);
  fetch(`/posiciones?${params.toString()}`)
    .then(res => res.json())
    .then(data => {
      if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = '<div style="color:#d32f2f;font-weight:600;">No hay datos para la selección.</div>';
        return;
      }
      let html = `<div class="tabla-posiciones-wrapper">
        <table class="tabla-posiciones-pro" style="width:100%;">
          <thead>
            <tr>
              <th style="width:32px;"></th>
              <th>Pos</th>
              <th>Logo</th>
              <th>Zona</th>
              <th style="min-width:150px;">Equipo</th>
              <th>PJ</th>
              <th>PG</th>
              <th>PE</th>
              <th>PP</th>
              <th>GF</th>
              <th>GC</th>
              <th>Dif</th>
              <th style="min-width:60px;">Bonus</th>
              <th class="puntos-col">Pts</th>
            </tr>
          </thead>
          <tbody>`;
      for (const row of data) {
        html += `<tr>
          <td><span class="lupa"><i class="fas fa-search"></i></span></td>
          <td>${row.pos}</td>
          <td><img src="${row.logo || '/static/assets/img/logo-asociacion.png'}" alt="Logo ${row.equipo}" class="logo-club"></td>
          <td>${row.zona || 'A'}</td>
            <td style="font-weight:600;" title="${row.equipo}">${row.equipo}</td>
          <td>${row.pj}</td>
          <td>${row.pg}</td>
          <td>${row.pe}</td>
          <td>${row.pp}</td>
          <td>${row.gf}</td>
          <td>${row.gc || row.ge || 0}</td>
          <td>${row.dif > 0 ? '+' : ''}${row.dif}</td>
          <td>${row.bonus || 0}</td>
          <td class="puntos-col">${row.pts}</td>
        </tr>`;
      }
      html += '</tbody></table></div>';
      container.innerHTML = html;
    })
    .catch(() => {
      container.innerHTML = '<div style="color:red;">Error al cargar posiciones</div>';
    });
}

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('posiciones-form');
  if (form) {
    const update = function() {
      const torneo = form['torneo'].value;
      const division = form['division'].value;
      const fecha = form['fecha'] ? form['fecha'].value : '';
      const bloque = form['bloque'] ? form['bloque'].value : '';
      renderTablaPosiciones(torneo, division, fecha, bloque);
    };
    // Actualiza la tabla automáticamente al cambiar cualquier filtro
    form['torneo'].addEventListener('change', update);
    form['division'].addEventListener('change', update);
    if (form['fecha']) form['fecha'].addEventListener('change', update);
    if (form['bloque']) form['bloque'].addEventListener('change', update);
    // Render inicial
    update();
  }
});
