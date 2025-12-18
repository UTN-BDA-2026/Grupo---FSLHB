// admin-panel.js
// Lógica para el panel de administración (usuario admin)

document.addEventListener('DOMContentLoaded', () => {
  const fechaHoy = document.getElementById('fecha-hoy');
  if (fechaHoy) {
    const hoy = new Date();
    const meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
    fechaHoy.textContent = `${hoy.getDate()} de ${meses[hoy.getMonth()]} de ${hoy.getFullYear()}`;
  }

  const panelContent = document.getElementById('panel-content');
  const btnVer = document.getElementById('ver-arbitros');
  const btnAgregar = document.getElementById('agregar-arbitro');
  const btnEditar = document.getElementById('editar-arbitro');
  const btnEliminar = document.getElementById('eliminar-arbitro');
  const btnVerClubes = document.getElementById('ver-clubes');
  const btnAgregarClub = document.getElementById('agregar-club');
  const btnEditarClub = document.getElementById('editar-club');
  const btnEliminarClub = document.getElementById('eliminar-club');
  const btnCargarFixture = document.getElementById('cargar-fixture');
  const btnVerJugadores = document.getElementById('ver-jugadores');
  const btnVerTorneos = document.getElementById('ver-torneos');
  const btnAgregarTorneo = document.getElementById('agregar-torneo');
  const btnEditarTorneo = document.getElementById('editar-torneo');
  const btnEliminarTorneo = document.getElementById('eliminar-torneo');
  const btnGestionarPosiciones = document.getElementById('gestionar-posiciones');

  async function cargarArbitros() {
    if (!panelContent) return;
    panelContent.innerHTML = '<p>Cargando árbitros...</p>';
    try {
      const resp = await fetch('/arbitros/');
      if (!resp.ok) {
        panelContent.innerHTML = `<p>Error al obtener árbitros (código ${resp.status}).</p>`;
        return;
      }
      const lista = await resp.json();
      if (!Array.isArray(lista) || lista.length === 0) {
        panelContent.innerHTML = '<p>No hay árbitros cargados.</p>';
        return;
      }
      const filas = lista.map(a => `
        <tr>
          <td>${a.id}</td>
          <td>${a.apellido}</td>
          <td>${a.nombre}</td>
          <td>${a.dni}</td>
        </tr>
      `).join('');
      panelContent.innerHTML = `
        <h3>Listado de Árbitros</h3>
        <div class="tabla-posiciones-card">
          <table class="tabla-posiciones">
            <thead>
              <tr><th>ID</th><th>Apellido</th><th>Nombre</th><th>DNI</th></tr>
            </thead>
            <tbody>${filas}</tbody>
          </table>
        </div>
      `;
    } catch (err) {
      console.error('Error al cargar árbitros', err);
      panelContent.innerHTML = '<p>Error inesperado al cargar árbitros.</p>';
    }
  }

  if (btnVer) {
    btnVer.addEventListener('click', e => {
      e.preventDefault();
      cargarArbitros();
    });
  }

  async function cargarClubes() {
    if (!panelContent) return;
    panelContent.innerHTML = '<p>Cargando clubes...</p>';
    try {
      const resp = await fetch('/clubs');
      if (!resp.ok) {
        panelContent.innerHTML = `<p>Error al obtener clubes (código ${resp.status}).</p>`;
        return;
      }
      const lista = await resp.json();
      if (!Array.isArray(lista) || lista.length === 0) {
        panelContent.innerHTML = '<p>No hay clubes cargados.</p>';
        return;
      }
      const filas = lista.map(c => `
        <tr>
          <td>${c.id}</td>
          <td>${c.nombre}</td>
          <td>${c.razon_social || ''}</td>
          <td>${c.cancha_local || ''}</td>
        </tr>
      `).join('');
      panelContent.innerHTML = `
        <h3>Listado de Clubes</h3>
        <div class="tabla-posiciones-card">
          <table class="tabla-posiciones">
            <thead>
              <tr><th>ID</th><th>Nombre</th><th>Razón social</th><th>Cancha local</th></tr>
            </thead>
            <tbody>${filas}</tbody>
          </table>
        </div>
      `;
    } catch (err) {
      console.error('Error al cargar clubes', err);
      panelContent.innerHTML = '<p>Error inesperado al cargar clubes.</p>';
    }
  }

  if (btnVerClubes) {
    btnVerClubes.addEventListener('click', e => {
      e.preventDefault();
      cargarClubes();
    });
  }

  async function cargarTorneos() {
    if (!panelContent) return;
    panelContent.innerHTML = '<p>Cargando torneos...</p>';
    try {
      const resp = await fetch('/admin/torneos');
      if (!resp.ok) {
        panelContent.innerHTML = `<p>Error al obtener torneos (código ${resp.status}).</p>`;
        return;
      }
      const lista = await resp.json();
      if (!Array.isArray(lista) || lista.length === 0) {
        panelContent.innerHTML = '<p>No hay torneos cargados.</p>';
        return;
      }
      const filas = lista.map(t => `
        <tr>
          <td>${t.id}</td>
          <td>${t.nombre}</td>
          <td>${t.max_fechas}</td>
        </tr>
      `).join('');
      panelContent.innerHTML = `
        <h3>Listado de Torneos</h3>
        <div class="tabla-posiciones-card">
          <table class="tabla-posiciones">
            <thead>
              <tr><th>ID</th><th>Nombre</th><th>Máx. fechas</th></tr>
            </thead>
            <tbody>${filas}</tbody>
          </table>
        </div>
      `;
    } catch (err) {
      console.error('Error al cargar torneos', err);
      panelContent.innerHTML = '<p>Error inesperado al cargar torneos.</p>';
    }
  }

  if (btnCargarFixture) {
    btnCargarFixture.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Cargar fixture de partidos (CSV)</h3>
        <form id="form-cargar-fixture" class="jugadora-form" style="max-width:700px;" enctype="multipart/form-data">
          <p style="font-size:0.9rem;color:#555;">
            El archivo debe tener las columnas: <code>torneo,categoria,fecha_numero,bloque,fecha_hora,cancha,equipo_local_nombre,equipo_visitante_nombre</code>.
          </p>
          <label>Archivo CSV
            <input type="file" id="archivo-fixture" name="archivo" accept=".csv" required />
          </label>
          <button type="submit">Subir y procesar</button>
        </form>
        <p style="margin-top:1rem;font-size:0.9rem;color:#555;">Solo usuarios administradores pueden ejecutar esta acción.</p>
      `;

      const form = document.getElementById('form-cargar-fixture');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const input = document.getElementById('archivo-fixture');
        if (!input || !input.files || input.files.length === 0) {
          alert('Seleccione un archivo CSV.');
          return;
        }
        const file = input.files[0];
        const formData = new FormData();
        formData.append('archivo', file);
        try {
          const resp = await fetch('/admin/partidos/fixture', {
            method: 'POST',
            body: formData
          });
          const data = await resp.json().catch(() => ({}));
          if (!resp.ok || !data.ok) {
            alert('No se pudo procesar el fixture: ' + (data.error || resp.status));
            return;
          }
          alert('Fixture procesado correctamente. Partidos creados: ' + (data.creados ?? 0));
        } catch (err) {
          console.error('Error al cargar fixture', err);
          alert('Error inesperado al cargar el fixture.');
        }
      });
    });
  }

  // --- Gestión de posiciones / categorías de equipos ---
  const CATEGORIAS_BASE = ['Damas A', 'Damas B', 'Damas C', 'Caballeros', 'Mamis'];

  async function mostrarGestorPosiciones() {
    if (!panelContent) return;
    panelContent.innerHTML = '<p>Cargando torneos...</p>';
    let torneos = [];
    try {
      const resp = await fetch('/admin/torneos');
      if (resp.ok) {
        torneos = await resp.json();
      }
    } catch (e) {
      console.error('Error obteniendo torneos para gestor de posiciones', e);
    }

    const opcionesTorneo = torneos.map(t => `<option value="${t.nombre}">${t.nombre}</option>`).join('');
    const opcionesCategoria = CATEGORIAS_BASE.map(c => `<option value="${c}">${c}</option>`).join('');

    panelContent.innerHTML = `
      <h3>Gestión de categorías de equipos por torneo</h3>
      <form id="gp-form" class="panel-torneo-form" style="max-width:720px;">
        <label>Torneo
          <select name="torneo" id="gp-torneo" required>
            <option value="">Selecciona un torneo</option>
            ${opcionesTorneo}
          </select>
        </label>
        <label>Categoría actual
          <select name="division" id="gp-division" required>
            <option value="">Selecciona una categoría</option>
            ${opcionesCategoria}
          </select>
        </label>
        <button type="submit" class="btn-primario">Ver posiciones</button>
      </form>
      <div id="gp-tabla" style="margin-top:1.5rem;"></div>
    `;

    const form = document.getElementById('gp-form');
    const tablaDiv = document.getElementById('gp-tabla');

    async function cargarTabla() {
      const torneo = form['torneo'].value;
      const division = form['division'].value;
      if (!torneo || !division) {
        tablaDiv.innerHTML = '<p style="color:#888;">Selecciona torneo y categoría.</p>';
        return;
      }
      tablaDiv.innerHTML = '<p style="color:#888;">Cargando posiciones...</p>';
      const params = new URLSearchParams({ torneo, division });
      try {
        const resp = await fetch(`/posiciones?${params.toString()}`);
        const data = await resp.json();
        if (!Array.isArray(data) || data.length === 0) {
          tablaDiv.innerHTML = '<p style="color:#d32f2f;">No hay datos para la selección.</p>';
          return;
        }

        // Construir conjunto de categorías disponibles (base + las que vengan de la API)
        const categoriasSet = new Set(CATEGORIAS_BASE);
        data.forEach(r => { if (r.categoria) categoriasSet.add(r.categoria); });
        const opcionesSelect = Array.from(categoriasSet).map(c => `<option value="${c}">${c}</option>`).join('');

        let html = `
          <div class="tabla-posiciones-wrapper">
            <table class="tabla-posiciones-pro" style="width:100%;">
              <thead>
                <tr>
                  <th>Pos</th>
                  <th>Equipo</th>
                  <th>Categoría actual</th>
                  <th>Nueva categoría</th>
                  <th>Acción</th>
                </tr>
              </thead>
              <tbody>`;
        for (const row of data) {
          const catActual = row.categoria || division;
          html += `
            <tr>
              <td>${row.pos}</td>
              <td>${row.equipo}</td>
              <td>${catActual}</td>
              <td>
                <select class="gp-categoria-select" data-equipo-id="${row.equipo_id}">
                  ${opcionesSelect.replace(`value="${catActual}"`, `value="${catActual}" selected`)}
                </select>
              </td>
              <td>
                <button type="button" class="gp-guardar-categoria" data-equipo-id="${row.equipo_id}">Guardar</button>
              </td>
            </tr>`;
        }
        html += '</tbody></table></div>';
        tablaDiv.innerHTML = html;
      } catch (e) {
        console.error('Error cargando posiciones para gestor', e);
        tablaDiv.innerHTML = '<p style="color:red;">Error al cargar posiciones.</p>';
      }
    }

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      cargarTabla();
    });

    tablaDiv.addEventListener('click', async function(e) {
      const btn = e.target.closest('.gp-guardar-categoria');
      if (!btn) return;
      const equipoId = btn.getAttribute('data-equipo-id');
      const select = tablaDiv.querySelector(`.gp-categoria-select[data-equipo-id="${equipoId}"]`);
      if (!select) return;
      const nuevaCat = select.value;
      if (!nuevaCat) {
        alert('Selecciona una categoría.');
        return;
      }
      if (!confirm('¿Confirmar cambio de categoría para este equipo?')) return;
      try {
        const resp = await fetch(`/admin/equipos/${equipoId}/categoria`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ categoria: nuevaCat })
        });
        const data = await resp.json().catch(() => ({}));
        if (!resp.ok || data.error) {
          alert('No se pudo actualizar la categoría: ' + (data.error || resp.status));
          return;
        }
        alert('Categoría actualizada correctamente.');
        // Recargar tabla para reflejar cambios (el equipo puede desaparecer de la categoría actual)
        cargarTabla();
      } catch (err) {
        console.error('Error actualizando categoría de equipo', err);
        alert('Error inesperado al actualizar la categoría.');
      }
    });
  }

  if (btnGestionarPosiciones) {
    btnGestionarPosiciones.addEventListener('click', e => {
      e.preventDefault();
      mostrarGestorPosiciones();
    });
  }

  async function cargarJugadoresEstadisticas() {
    if (!panelContent) return;
    panelContent.innerHTML = '<p>Cargando estadísticas de jugadores...</p>';
    try {
      const [jugResp, clubResp, resumenResp] = await Promise.all([
        fetch('/jugadoras'),
        fetch('/clubs'),
        fetch('/ranking/resumen')
      ]);

      if (!jugResp.ok || !clubResp.ok || !resumenResp.ok) {
        panelContent.innerHTML = '<p>Error al obtener datos de jugadores o clubes.</p>';
        return;
      }

      const jugadoras = await jugResp.json();
      const clubes = await clubResp.json();
      const resumen = await resumenResp.json();

      const clubMap = {};
      (Array.isArray(clubes) ? clubes : []).forEach(c => {
        clubMap[c.id] = c.nombre;
      });

      const stats = {};
      const mergeLista = (lista, campo) => {
        if (!Array.isArray(lista)) return;
        lista.forEach(item => {
          const key = `${item.club}||${item.jugador}`;
          if (!stats[key]) {
            stats[key] = { goles: 0, amarillas: 0, rojas: 0 };
          }
          stats[key][campo] = item.cantidad || 0;
        });
      };
      mergeLista(resumen.goleadores, 'goles');
      mergeLista(resumen.amarillas, 'amarillas');
      mergeLista(resumen.rojas, 'rojas');

      const filasBase = (Array.isArray(jugadoras) ? jugadoras : []).map(j => {
        const clubNombre = clubMap[j.club_id] || '';
        const jugadorNombre = `${j.nombre} ${j.apellido}`.trim();
        const key = `${clubNombre}||${jugadorNombre}`;
        const s = stats[key] || { goles: 0, amarillas: 0, rojas: 0 };
        return {
          jugadoraId: j.id,
          clubId: j.club_id,
          club: clubNombre,
          jugador: jugadorNombre,
          categoria: j.categoria || '',
          goles: s.goles,
          amarillas: s.amarillas,
          rojas: s.rojas,
        };
      });

      if (filasBase.length === 0) {
        panelContent.innerHTML = '<p>No hay jugadoras cargadas en el sistema.</p>';
        return;
      }

      filasBase.sort((a, b) => {
        if (a.club === b.club) {
          if (a.categoria === b.categoria) {
            return a.jugador.localeCompare(b.jugador);
          }
          return a.categoria.localeCompare(b.categoria);
        }
        return a.club.localeCompare(b.club);
      });

      const clubesUnicos = [];
      const clubSet = new Set();
      filasBase.forEach(f => {
        if (f.club && !clubSet.has(f.clubId)) {
          clubSet.add(f.clubId);
          clubesUnicos.push({ id: f.clubId, nombre: f.club });
        }
      });
      clubesUnicos.sort((a, b) => a.nombre.localeCompare(b.nombre));

      const categoriasUnicas = Array.from(new Set(filasBase.map(f => f.categoria).filter(Boolean))).sort();

      const renderFilas = (filas) => filas.map(r => `
        <tr>
          <td>${r.club}</td>
          <td>${r.jugador}</td>
          <td>${r.categoria || ''}</td>
          <td style="text-align:center;">${r.goles}</td>
          <td style="text-align:center;">${r.amarillas}</td>
          <td style="text-align:center;">${r.rojas}</td>
          <td style="text-align:center;">
            <button type="button" class="btn-editar-tarjetas" data-jugadora-id="${r.jugadoraId}" data-club-id="${r.clubId}" data-jugadora-nombre="${r.jugador}" data-club-nombre="${r.club}">Editar tarjetas</button>
          </td>
        </tr>
      `).join('');

      const opcionesClub = clubesUnicos.map(c => `<option value="${c.id}">${c.nombre}</option>`).join('');
      const opcionesCat = categoriasUnicas.map(c => `<option value="${c}">${c}</option>`).join('');

      panelContent.innerHTML = `
        <h3>Jugadores/as por club con goles y tarjetas</h3>
        <form id="filtro-jugadores" class="jugadora-form" style="max-width:700px;">
          <label>Filtrar por club
            <select id="filtro-club">
              <option value="">Todos los clubes</option>
              ${opcionesClub}
            </select>
          </label>
          <label>Filtrar por categoría
            <select id="filtro-categoria">
              <option value="">Todas las categorías</option>
              ${opcionesCat}
            </select>
          </label>
        </form>
        <div class="tabla-posiciones-card">
          <table class="tabla-posiciones">
            <thead>
              <tr>
                <th>Club</th>
                <th>Jugador/a</th>
                <th>Categoría</th>
                <th>Goles</th>
                <th>Tarjetas amarillas</th>
                <th>Tarjetas rojas</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody id="tbody-jugadores">${renderFilas(filasBase)}</tbody>
          </table>
        </div>
        <div id="detalle-jugadora-tarjetas" style="margin-top:1.5rem;"></div>
        <p style="margin-top:0.8rem;font-size:0.9rem;color:#555;">Datos calculados a partir de las jugadoras cargadas y las incidencias registradas en los partidos.</p>
      `;

      const selectClub = document.getElementById('filtro-club');
      const selectCat = document.getElementById('filtro-categoria');
      const tbody = document.getElementById('tbody-jugadores');

      const detalleDiv = document.getElementById('detalle-jugadora-tarjetas');

      const cargarDetalleTarjetas = async (jugadoraId, clubId, jugadoraNombre, clubNombre) => {
        if (!detalleDiv) return;
        detalleDiv.innerHTML = `<p>Cargando tarjetas de <strong>${jugadoraNombre}</strong> (${clubNombre})...</p>`;
        try {
          const resp = await fetch(`/admin/jugadoras/${jugadoraId}/incidencias`);
          if (!resp.ok) {
            detalleDiv.innerHTML = '<p>No se pudieron cargar las tarjetas de esta jugadora.</p>';
            return;
          }
          const incidencias = await resp.json();
          if (!Array.isArray(incidencias) || incidencias.length === 0) {
            detalleDiv.innerHTML = `<p><strong>${jugadoraNombre}</strong> (${clubNombre}) no tiene tarjetas registradas.</p>`;
          } else {
            const filasInc = incidencias.map(inc => `
              <tr>
                <td>${inc.torneo || ''}</td>
                <td>${inc.categoria || ''}</td>
                <td>${inc.fecha_numero != null ? inc.fecha_numero : ''}</td>
                <td>${(inc.club_local_nombre || '')} vs ${(inc.club_visitante_nombre || '')}</td>
                <td>${inc.color || ''}</td>
                <td>${inc.minuto != null ? inc.minuto : ''}</td>
                <td style="text-align:center;">
                  <button type="button" class="btn-eliminar-tarjeta" data-incidencia-id="${inc.id}">Eliminar</button>
                </td>
              </tr>
            `).join('');

            detalleDiv.innerHTML = `
              <h4>Tarjetas de ${jugadoraNombre} (${clubNombre})</h4>
              <div class="tabla-posiciones-card">
                <table class="tabla-posiciones">
                  <thead>
                    <tr>
                      <th>Torneo</th>
                      <th>Categoría</th>
                      <th>Fecha</th>
                      <th>Partido</th>
                      <th>Color</th>
                      <th>Minuto</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${filasInc}
                  </tbody>
                </table>
              </div>
            `;

            const botonesEliminar = detalleDiv.querySelectorAll('.btn-eliminar-tarjeta');
            botonesEliminar.forEach(btn => {
              btn.addEventListener('click', async () => {
                const incidenciaId = btn.getAttribute('data-incidencia-id');
                if (!incidenciaId) return;
                if (!confirm('¿Seguro que deseas eliminar esta tarjeta?')) return;
                try {
                  const delResp = await fetch(`/admin/incidencias/${incidenciaId}`, { method: 'DELETE' });
                  if (!delResp.ok) {
                    const err = await delResp.json().catch(() => ({}));
                    alert('No se pudo eliminar la tarjeta: ' + (err.error || delResp.status));
                    return;
                  }
                  alert('Tarjeta eliminada correctamente.');
                  // Recargar estadísticas completas para reflejar los cambios
                  cargarJugadoresEstadisticas();
                } catch (err) {
                  console.error('Error al eliminar tarjeta', err);
                  alert('Error inesperado al eliminar tarjeta.');
                }
              });
            });
          }

          // Formulario para agregar nueva tarjeta
          const formHtml = `
            <h4 style="margin-top:1.2rem;">Agregar tarjeta a ${jugadoraNombre}</h4>
            <form id="form-agregar-tarjeta" class="jugadora-form" style="max-width:700px;">
              <label>Partido
                <select id="sel-partido-tarjeta" required>
                  <option value="">Seleccionar partido...</option>
                </select>
              </label>
              <label>Color
                <select id="sel-color-tarjeta" required>
                  <option value="amarilla">Amarilla</option>
                  <option value="roja">Roja</option>
                  <option value="verde">Verde</option>
                </select>
              </label>
              <label>Minuto (opcional)
                <input type="number" id="inp-minuto-tarjeta" min="0" max="200" step="1" />
              </label>
              <button type="submit">Agregar tarjeta</button>
            </form>
          `;

          detalleDiv.insertAdjacentHTML('beforeend', formHtml);

          // Cargar partidos del club para seleccionar
          try {
            const partResp = await fetch(`/partidos?club_id=${encodeURIComponent(String(clubId))}`);
            if (partResp.ok) {
              const partidos = await partResp.json();
              const selPartido = document.getElementById('sel-partido-tarjeta');
              if (selPartido && Array.isArray(partidos)) {
                partidos.forEach(p => {
                  const label = `${p.torneo || ''} - ${p.categoria || ''} - Fecha ${p.fecha_numero != null ? p.fecha_numero : ''} - ${(p.club_local_nombre || '')} vs ${(p.club_visitante_nombre || '')}`;
                  const opt = document.createElement('option');
                  opt.value = p.id;
                  opt.textContent = label;
                  selPartido.appendChild(opt);
                });
              }
            }
          } catch (err) {
            console.error('Error al cargar partidos para tarjetas', err);
          }

          const form = document.getElementById('form-agregar-tarjeta');
          if (form) {
            form.addEventListener('submit', async ev => {
              ev.preventDefault();
              const selPartido = document.getElementById('sel-partido-tarjeta');
              const selColor = document.getElementById('sel-color-tarjeta');
              const inpMinuto = document.getElementById('inp-minuto-tarjeta');
              const partidoId = selPartido ? selPartido.value : '';
              const color = selColor ? selColor.value : '';
              const minutoStr = inpMinuto && inpMinuto.value !== '' ? inpMinuto.value : null;
              if (!partidoId || !color) {
                alert('Debe seleccionar partido y color de tarjeta.');
                return;
              }
              let minuto = null;
              if (minutoStr !== null) {
                const parsed = parseInt(minutoStr, 10);
                if (!Number.isNaN(parsed)) {
                  minuto = parsed;
                }
              }
              try {
                const respCrear = await fetch(`/admin/jugadoras/${jugadoraId}/incidencias`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    partido_id: partidoId,
                    club_id: clubId,
                    color,
                    minuto
                  })
                });
                if (!respCrear.ok) {
                  const err = await respCrear.json().catch(() => ({}));
                  alert('No se pudo registrar la tarjeta: ' + (err.error || respCrear.status));
                  return;
                }
                alert('Tarjeta agregada correctamente.');
                // Recargar estadísticas completas para reflejar los cambios
                cargarJugadoresEstadisticas();
              } catch (err) {
                console.error('Error al agregar tarjeta', err);
                alert('Error inesperado al agregar tarjeta.');
              }
            });
          }
        } catch (err) {
          console.error('Error al cargar detalle de tarjetas', err);
          detalleDiv.innerHTML = '<p>Error inesperado al cargar las tarjetas de esta jugadora.</p>';
        }
      };

      const aplicarFiltros = () => {
        const clubSel = selectClub.value;
        const catSel = selectCat.value;
        const filtradas = filasBase.filter(f => {
          const okClub = !clubSel || String(f.clubId) === clubSel;
          const okCat = !catSel || f.categoria === catSel;
          return okClub && okCat;
        });
        tbody.innerHTML = renderFilas(filtradas);
        const botones = tbody.querySelectorAll('.btn-editar-tarjetas');
        botones.forEach(btn => {
          btn.addEventListener('click', () => {
            const jugadoraId = Number(btn.getAttribute('data-jugadora-id'));
            const clubId = Number(btn.getAttribute('data-club-id'));
            const jugadoraNombre = btn.getAttribute('data-jugadora-nombre') || '';
            const clubNombre = btn.getAttribute('data-club-nombre') || '';
            cargarDetalleTarjetas(jugadoraId, clubId, jugadoraNombre, clubNombre);
          });
        });
      };

      selectClub.addEventListener('change', aplicarFiltros);
      selectCat.addEventListener('change', aplicarFiltros);

      // En el render inicial también enlazar los botones
      const botonesIniciales = tbody.querySelectorAll('.btn-editar-tarjetas');
      botonesIniciales.forEach(btn => {
        btn.addEventListener('click', () => {
          const jugadoraId = Number(btn.getAttribute('data-jugadora-id'));
          const clubId = Number(btn.getAttribute('data-club-id'));
          const jugadoraNombre = btn.getAttribute('data-jugadora-nombre') || '';
          const clubNombre = btn.getAttribute('data-club-nombre') || '';
          cargarDetalleTarjetas(jugadoraId, clubId, jugadoraNombre, clubNombre);
        });
      });
    } catch (err) {
      console.error('Error al cargar estadísticas de jugadores', err);
      panelContent.innerHTML = '<p>Error inesperado al cargar estadísticas de jugadores.</p>';
    }
  }

  if (btnVerJugadores) {
    btnVerJugadores.addEventListener('click', e => {
      e.preventDefault();
      cargarJugadoresEstadisticas();
    });
  }

  // Por ahora mostramos mensajes de placeholder para las otras acciones
  if (btnAgregar) {
    btnAgregar.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Agregar árbitro</h3>
        <form id="form-agregar-arbitro" class="jugadora-form" autocomplete="off">
          <label>Nombre<input type="text" id="arb-nombre" required></label>
          <label>Apellido<input type="text" id="arb-apellido" required></label>
          <label>DNI<input type="text" id="arb-dni" required></label>
          <button type="submit">Guardar</button>
        </form>
        <p style="margin-top:1rem;font-size:0.9rem;color:#555;">Luego de guardar se mostrará el listado actualizado de árbitros.</p>
      `;

      const form = document.getElementById('form-agregar-arbitro');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const nombre = document.getElementById('arb-nombre').value.trim();
        const apellido = document.getElementById('arb-apellido').value.trim();
        const dni = document.getElementById('arb-dni').value.trim();
        if (!nombre || !apellido || !dni) {
          alert('Todos los campos son obligatorios.');
          return;
        }
        try {
          const resp = await fetch('/arbitros/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, apellido, dni })
          });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo crear el árbitro: ' + (err.error || resp.status));
            return;
          }
          alert('Árbitro creado correctamente.');
          cargarArbitros();
        } catch (err) {
          console.error('Error al crear árbitro', err);
          alert('Error inesperado al crear árbitro.');
        }
      });
    });
  }
  if (btnEditar) {
    btnEditar.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Editar datos de árbitro</h3>
        <p style="font-size:0.9rem;color:#555;">Primero consulta "Ver árbitros" para conocer el ID.</p>
        <form id="form-editar-arbitro" class="jugadora-form" autocomplete="off">
          <label>ID Árbitro<input type="number" id="edit-id" min="1" required></label>
          <label>Nuevo nombre (opcional)<input type="text" id="edit-nombre"></label>
          <label>Nuevo apellido (opcional)<input type="text" id="edit-apellido"></label>
          <button type="submit">Guardar cambios</button>
        </form>
      `;

      const form = document.getElementById('form-editar-arbitro');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const id = Number(document.getElementById('edit-id').value);
        const nombre = document.getElementById('edit-nombre').value.trim();
        const apellido = document.getElementById('edit-apellido').value.trim();
        if (!id) {
          alert('Debe indicar un ID de árbitro válido.');
          return;
        }
        if (!nombre && !apellido) {
          alert('Indique al menos un campo a modificar (nombre o apellido).');
          return;
        }
        try {
          const resp = await fetch(`/arbitros/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre || undefined, apellido: apellido || undefined })
          });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo actualizar el árbitro: ' + (err.error || resp.status));
            return;
          }
          alert('Árbitro actualizado correctamente.');
          cargarArbitros();
        } catch (err) {
          console.error('Error al actualizar árbitro', err);
          alert('Error inesperado al actualizar árbitro.');
        }
      });
    });
  }
  if (btnEliminar) {
    btnEliminar.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Eliminar árbitro</h3>
        <p style="font-size:0.9rem;color:#555;">Primero consulta "Ver árbitros" para conocer el ID.</p>
        <form id="form-eliminar-arbitro" class="jugadora-form" autocomplete="off">
          <label>ID Árbitro<input type="number" id="del-id" min="1" required></label>
          <button type="submit" style="background-color:#c62828;">Eliminar</button>
        </form>
      `;

      const form = document.getElementById('form-eliminar-arbitro');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const id = Number(document.getElementById('del-id').value);
        if (!id) {
          alert('Debe indicar un ID de árbitro válido.');
          return;
        }
        if (!confirm('¿Seguro que deseas eliminar este árbitro?')) return;
        try {
          const resp = await fetch(`/arbitros/${id}`, { method: 'DELETE' });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo eliminar el árbitro: ' + (err.error || resp.status));
            return;
          }
          alert('Árbitro eliminado correctamente.');
          cargarArbitros();
        } catch (err) {
          console.error('Error al eliminar árbitro', err);
          alert('Error inesperado al eliminar árbitro.');
        }
      });
    });
  }

  if (btnAgregarClub) {
    btnAgregarClub.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Agregar club</h3>
        <form id="form-agregar-club" class="jugadora-form" autocomplete="off">
          <label>Nombre del club<input type="text" id="club-nombre" required></label>
          <button type="submit">Guardar</button>
        </form>
        <p style="margin-top:1rem;font-size:0.9rem;color:#555;">Luego de guardar se mostrará el listado actualizado de clubes.</p>
      `;

      const form = document.getElementById('form-agregar-club');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const nombre = document.getElementById('club-nombre').value.trim();
        if (!nombre) {
          alert('El nombre del club es obligatorio.');
          return;
        }
        try {
          const resp = await fetch('/clubs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre })
          });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo crear el club: ' + (err.error || resp.status));
            return;
          }
          alert('Club creado correctamente.');
          cargarClubes();
        } catch (err) {
          console.error('Error al crear club', err);
          alert('Error inesperado al crear club.');
        }
      });
    });
  }

  if (btnEditarClub) {
    btnEditarClub.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Editar nombre de club</h3>
        <p style="font-size:0.9rem;color:#555;">Primero consulta "Ver clubes" para conocer el ID.</p>
        <form id="form-editar-club" class="jugadora-form" autocomplete="off">
          <label>ID Club<input type="number" id="edit-club-id" min="1" required></label>
          <label>Nuevo nombre<input type="text" id="edit-club-nombre" required></label>
          <button type="submit">Guardar cambios</button>
        </form>
      `;

      const form = document.getElementById('form-editar-club');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const id = Number(document.getElementById('edit-club-id').value);
        const nombre = document.getElementById('edit-club-nombre').value.trim();
        if (!id) {
          alert('Debe indicar un ID de club válido.');
          return;
        }
        if (!nombre) {
          alert('El nuevo nombre es obligatorio.');
          return;
        }
        try {
          const resp = await fetch(`/clubs/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre })
          });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo actualizar el club: ' + (err.error || resp.status));
            return;
          }
          alert('Club actualizado correctamente.');
          cargarClubes();
        } catch (err) {
          console.error('Error al actualizar club', err);
          alert('Error inesperado al actualizar club.');
        }
      });
    });
  }

  if (btnEliminarClub) {
    btnEliminarClub.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Eliminar club</h3>
        <p style="font-size:0.9rem;color:#555;">Primero consulta "Ver clubes" para conocer el ID.</p>
        <form id="form-eliminar-club" class="jugadora-form" autocomplete="off">
          <label>ID Club<input type="number" id="del-club-id" min="1" required></label>
          <button type="submit" style="background-color:#c62828;">Eliminar</button>
        </form>
      `;

      const form = document.getElementById('form-eliminar-club');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const id = Number(document.getElementById('del-club-id').value);
        if (!id) {
          alert('Debe indicar un ID de club válido.');
          return;
        }
        if (!confirm('¿Seguro que deseas eliminar este club?')) return;
        try {
          const resp = await fetch(`/clubs/${id}`, { method: 'DELETE' });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo eliminar el club: ' + (err.error || resp.status));
            return;
          }
          alert('Club eliminado correctamente.');
          cargarClubes();
        } catch (err) {
          console.error('Error al eliminar club', err);
          alert('Error inesperado al eliminar club.');
        }
      });
    });
  }

  if (btnVerTorneos) {
    btnVerTorneos.addEventListener('click', e => {
      e.preventDefault();
      cargarTorneos();
    });
  }

  if (btnAgregarTorneo) {
    btnAgregarTorneo.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Agregar torneo</h3>
        <form id="form-agregar-torneo" class="jugadora-form" autocomplete="off">
          <label>Nombre del torneo<input type="text" id="torneo-nombre" required></label>
          <label>Cantidad máxima de fechas<input type="number" id="torneo-max-fechas" min="1" required></label>
          <button type="submit">Guardar</button>
        </form>
        <p style="margin-top:1rem;font-size:0.9rem;color:#555;">Luego de guardar se mostrará el listado actualizado de torneos.</p>
      `;

      const form = document.getElementById('form-agregar-torneo');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const nombre = document.getElementById('torneo-nombre').value.trim();
        const maxFechasStr = document.getElementById('torneo-max-fechas').value;
        const maxFechas = Number(maxFechasStr);
        if (!nombre) {
          alert('El nombre del torneo es obligatorio.');
          return;
        }
        if (!maxFechas || maxFechas <= 0) {
          alert('La cantidad máxima de fechas debe ser mayor a cero.');
          return;
        }
        try {
          const resp = await fetch('/admin/torneos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, max_fechas: maxFechas })
          });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo crear el torneo: ' + (err.error || resp.status));
            return;
          }
          alert('Torneo creado correctamente.');
          cargarTorneos();
        } catch (err) {
          console.error('Error al crear torneo', err);
          alert('Error inesperado al crear torneo.');
        }
      });
    });
  }

  if (btnEditarTorneo) {
    btnEditarTorneo.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Editar torneo</h3>
        <p style="font-size:0.9rem;color:#555;">Primero consulta "Ver torneos" para conocer el ID.</p>
        <form id="form-editar-torneo" class="jugadora-form" autocomplete="off">
          <label>ID Torneo<input type="number" id="edit-torneo-id" min="1" required></label>
          <label>Nuevo nombre<input type="text" id="edit-torneo-nombre" required></label>
          <label>Nueva cantidad máxima de fechas<input type="number" id="edit-torneo-max-fechas" min="1" required></label>
          <button type="submit">Guardar cambios</button>
        </form>
      `;

      const form = document.getElementById('form-editar-torneo');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const id = Number(document.getElementById('edit-torneo-id').value);
        const nombre = document.getElementById('edit-torneo-nombre').value.trim();
        const maxFechasStr = document.getElementById('edit-torneo-max-fechas').value;
        const maxFechas = Number(maxFechasStr);
        if (!id) {
          alert('Debe indicar un ID de torneo válido.');
          return;
        }
        if (!nombre) {
          alert('El nuevo nombre es obligatorio.');
          return;
        }
        if (!maxFechas || maxFechas <= 0) {
          alert('La cantidad máxima de fechas debe ser mayor a cero.');
          return;
        }
        try {
          const resp = await fetch(`/admin/torneos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, max_fechas: maxFechas })
          });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo actualizar el torneo: ' + (err.error || resp.status));
            return;
          }
          alert('Torneo actualizado correctamente.');
          cargarTorneos();
        } catch (err) {
          console.error('Error al actualizar torneo', err);
          alert('Error inesperado al actualizar torneo.');
        }
      });
    });
  }

  if (btnEliminarTorneo) {
    btnEliminarTorneo.addEventListener('click', e => {
      e.preventDefault();
      if (!panelContent) return;
      panelContent.innerHTML = `
        <h3>Eliminar torneo</h3>
        <p style="font-size:0.9rem;color:#555;">Primero consulta "Ver torneos" para conocer el ID.</p>
        <form id="form-eliminar-torneo" class="jugadora-form" autocomplete="off">
          <label>ID Torneo<input type="number" id="del-torneo-id" min="1" required></label>
          <button type="submit" style="background-color:#c62828;">Eliminar</button>
        </form>
      `;

      const form = document.getElementById('form-eliminar-torneo');
      form.addEventListener('submit', async ev => {
        ev.preventDefault();
        const id = Number(document.getElementById('del-torneo-id').value);
        if (!id) {
          alert('Debe indicar un ID de torneo válido.');
          return;
        }
        if (!confirm('¿Seguro que deseas eliminar este torneo?')) return;
        try {
          const resp = await fetch(`/admin/torneos/${id}`, { method: 'DELETE' });
          if (!resp.ok) {
            const err = await resp.json().catch(() => ({}));
            alert('No se pudo eliminar el torneo: ' + (err.error || resp.status));
            return;
          }
          alert('Torneo eliminado correctamente.');
          cargarTorneos();
        } catch (err) {
          console.error('Error al eliminar torneo', err);
          alert('Error inesperado al eliminar torneo.');
        }
      });
    });
  }
});
