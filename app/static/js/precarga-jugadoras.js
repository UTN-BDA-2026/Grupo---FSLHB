// JS para mostrar jugadoras filtradas en precarga de equipos

document.addEventListener('DOMContentLoaded', function() {
    // Filtrar categorías según torneo seleccionado
    const torneoSelect = document.getElementById('torneo-select');
    const categoriaSelect = document.getElementById('categoria-select');
    const categoriasPorTorneo = {
        'Clausura Damas (2025)': [
            { value: 'damas_a', text: 'Damas A' },
            { value: 'damas_b', text: 'Damas B' },
            { value: 'damas_c', text: 'Damas C' }
        ],
        'Clausura Caballeros (2025)': [
            { value: 'caballeros', text: 'Caballeros' }
        ],
        'Clausura Mamis (2025)': [
            { value: 'mamis', text: 'Mamis' }
        ]
    };

    function actualizarCategorias() {
        const torneo = torneoSelect.value;
        categoriaSelect.innerHTML = '<option value="">Seleccione Categoría</option>';
        if (categoriasPorTorneo[torneo]) {
            categoriasPorTorneo[torneo].forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat.value;
                opt.textContent = cat.text;
                categoriaSelect.appendChild(opt);
            });
        }
    }
    const form = document.getElementById('precarga-form');
    const jugadorasSection = document.getElementById('jugadoras-section');
    const tablaJugadoras = document.getElementById('tabla-jugadoras').querySelector('tbody');
    const msg = document.getElementById('jugaderas-msg') || document.getElementById('jugadoras-msg');
    const clubId = localStorage.getItem('club_id');
    const isOperador = localStorage.getItem('isOperador') === 'true' || !clubId;
    const fechaSelect = document.getElementById('fecha-select');
    const partidoSelect = document.getElementById('partido-select');
    const btnConfirmar = document.getElementById('btn-confirmar-precarga');
    const contadorDiv = document.getElementById('jugadoras-contador');
    const contadorSpan = contadorDiv ? contadorDiv.querySelector('span') : null;
    const partidoInfo = document.getElementById('partido-info');
    const clubPrecargaSel = document.getElementById('club-precarga-select');
    const clubPrecargaWrap = document.getElementById('club-precarga-wrapper');
    let clubTargetId = null; // club destino de la precarga (operador) o clubId (club)

    // --- Custom dropdown sobre el select nativo para forzar apertura hacia abajo ---
    const ddWrapper = document.createElement('div');
    ddWrapper.className = 'custom-dd';
    const ddBtn = document.createElement('button');
    ddBtn.type = 'button';
    ddBtn.className = 'custom-dd-btn';
    ddBtn.textContent = 'Seleccione Partido';
    const ddMenu = document.createElement('div');
    ddMenu.className = 'custom-dd-menu';
    ddWrapper.appendChild(ddBtn);
    ddWrapper.appendChild(ddMenu);
    // Inserta justo después del select
    partidoSelect.parentNode.insertBefore(ddWrapper, partidoSelect.nextSibling);
    // Oculta el select nativo (lo usamos como fuente de verdad y para eventos)
    partidoSelect.style.display = 'none';

    function cerrarMenu() { ddWrapper.classList.remove('open'); }
    ddBtn.addEventListener('click', () => {
        ddWrapper.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
        if (!ddWrapper.contains(e.target)) cerrarMenu();
    });

    function renderDropdownFromSelect() {
        // Botón label
        const selOpt = partidoSelect.options[partidoSelect.selectedIndex];
        ddBtn.textContent = selOpt && selOpt.value ? (selOpt.title || selOpt.textContent) : 'Seleccione Partido';
        // Contenido
        ddMenu.innerHTML = '';
        Array.from(partidoSelect.options).forEach(opt => {
            const item = document.createElement('div');
            item.className = 'custom-dd-item';
            item.textContent = opt.title || opt.textContent;
            item.dataset.value = opt.value;
            item.addEventListener('click', () => {
                partidoSelect.value = opt.value;
                partidoSelect.dispatchEvent(new Event('change'));
                cerrarMenu();
                renderDropdownFromSelect();
            });
            ddMenu.appendChild(item);
        });
    }

    // Límite de jugadoras seleccionables
    const LIMITE_JUGADORAS = 20;
    const MINIMO_JUGADORAS = 7;

    // Utilidad para normalizar categoria
    const norm = (s) => (s || '').toString().toLowerCase().replace(/\s+/g, '_').trim();

    // Obtener fechas disponibles según torneo/categoría (y estado no jugado)
    async function cargarFechas() {
        const torneo = torneoSelect.value;
        const categoria = categoriaSelect.value;
        if (!torneo || !categoria) { fechaSelect.innerHTML = '<option value="">Todas</option>'; return; }
        try {
            const torneoQuery = (torneo || '').replace(/\s*\(\d{4}\)\s*$/, '').trim();
            const categoriaQuery = (categoria || '').replace(/_/g, ' ').trim();
            const params = new URLSearchParams({ torneo: torneoQuery, categoria: categoriaQuery, estado_not: 'jugado' });
            if (!isOperador && clubId) params.append('club_id', clubId);
            const url = `/partidos?${params.toString()}`;
            const res = await fetch(url);
            if (!res.ok) throw new Error();
            const partidos = await res.json();
            const fechas = Array.from(new Set((partidos || []).map(p => p.fecha_numero).filter(v => v != null))).sort((a,b)=>a-b);
            fechaSelect.innerHTML = '<option value="">Todas</option>' + fechas.map(f=>`<option value="${f}">${f}</option>`).join('');
        } catch (_) {
            fechaSelect.innerHTML = '<option value="">Todas</option>';
        }
    }

    // Cargar partidos segun torneo/categoria/fecha; si es club, filtra por club
    async function cargarPartidos() {
        const torneo = torneoSelect.value;
        const categoria = categoriaSelect.value;
        partidoSelect.innerHTML = '<option value="">Seleccione Partido</option>';
        if (!torneo || !categoria) return;
        try {
            // Normalizar valores para que coincidan con los almacenados en DB
            // - El torneo en DB es "Clausura Damas" (sin "(2025)")
            // - La categoría en DB es "Damas A" (con espacios, no con guiones bajos)
            const torneoQuery = (torneo || '').replace(/\s*\(\d{4}\)\s*$/, '').trim();
            const categoriaQuery = (categoria || '').replace(/_/g, ' ').trim();

            const params = new URLSearchParams({ torneo: torneoQuery, categoria: categoriaQuery, estado_not: 'jugado' });
            if (!isOperador && clubId) params.append('club_id', clubId);
            const fechaVal = (fechaSelect && fechaSelect.value) ? parseInt(fechaSelect.value) : null;
            if (fechaVal) params.append('fecha_numero', String(fechaVal));
            const url = `/partidos?${params.toString()}`;
            const res = await fetch(url);
            if (!res.ok) throw new Error('No se pudieron obtener los partidos');
            const partidos = await res.json();
            if (Array.isArray(partidos) && partidos.length) {
                partidos.forEach(p => {
                    const opt = document.createElement('option');
                    // Solo mostrar el encuentro (local vs visitante)
                    const local = p.equipo_local_nombre || p.club_local_nombre || 'Local';
                    const visitante = p.equipo_visitante_nombre || p.club_visitante_nombre || 'Visitante';
                    opt.value = p.id;
                    const label = `${local} vs ${visitante}`;
                    opt.textContent = label;
                    opt.title = label; // tooltip con texto completo
                    partidoSelect.appendChild(opt);
                });
                renderDropdownFromSelect();
            } else {
                // Mantener placeholder y opcionalmente informar en consola
                console.debug('Sin partidos para filtros', { torneoQuery, categoriaQuery, clubId });
                renderDropdownFromSelect();
            }
        } catch (e) {
            // mensaje no bloqueante
        }
    }

    function resetUI() {
        jugadorasSection.style.display = 'none';
        tablaJugadoras.innerHTML = '';
        btnConfirmar.style.display = 'none';
        if (msg) msg.textContent = '';
    }

    torneoSelect.addEventListener('change', () => { actualizarCategorias(); cargarFechas(); cargarPartidos(); resetUI(); });
    categoriaSelect.addEventListener('change', () => { cargarFechas(); cargarPartidos(); resetUI(); });
    if (fechaSelect) fechaSelect.addEventListener('change', () => { cargarPartidos(); resetUI(); });
    partidoSelect.addEventListener('change', async () => {
        resetUI();
        const sel = partidoSelect.options[partidoSelect.selectedIndex];
        if (sel && sel.value) {
            partidoInfo.style.display = 'block';
            partidoInfo.textContent = sel.title || sel.textContent;
            // Si es operador, cargar opciones de club destino (local/visitante)
            if (isOperador && clubPrecargaWrap && clubPrecargaSel) {
                clubPrecargaSel.innerHTML = '';
                try {
                    const res = await fetch(`/partidos/${encodeURIComponent(sel.value)}`);
                    const p = await res.json();
                    const opts = [];
                    if (p && p.club_local_id) {
                        opts.push({ id: p.club_local_id, nombre: p.equipo_local_nombre || p.club_local_nombre || 'Local' });
                    }
                    if (p && p.club_visitante_id) {
                        opts.push({ id: p.club_visitante_id, nombre: p.equipo_visitante_nombre || p.club_visitante_nombre || 'Visitante' });
                    }
                    clubPrecargaSel.appendChild(new Option('Seleccione club', ''));
                    opts.forEach(o => clubPrecargaSel.appendChild(new Option(o.nombre, o.id)));
                    clubPrecargaWrap.style.display = 'block';
                    clubTargetId = null;
                } catch (_) {
                    clubPrecargaWrap.style.display = 'none';
                }
            } else {
                // Usuario de club: el destino es su propio club
                clubTargetId = clubId ? parseInt(clubId) : null;
                if (clubPrecargaWrap) clubPrecargaWrap.style.display = 'none';
            }
        } else if (partidoInfo) {
            partidoInfo.style.display = 'none';
            partidoInfo.textContent = '';
            if (clubPrecargaWrap) clubPrecargaWrap.style.display = 'none';
            clubTargetId = null;
        }
    });

    // Cambio de club destino para operadores
    if (clubPrecargaSel) {
        clubPrecargaSel.addEventListener('change', () => {
            clubTargetId = clubPrecargaSel.value ? parseInt(clubPrecargaSel.value) : null;
            resetUI();
        });
    }

    // Mostrar/ocultar boton confirmar
    function actualizarBotonConfirmar() {
        const seleccionadas = tablaJugadoras.querySelectorAll('.seleccionar-jugadora:checked');
        const cant = seleccionadas.length;
        if (contadorDiv && contadorSpan) {
            if (cant >= MINIMO_JUGADORAS && cant <= LIMITE_JUGADORAS) {
                contadorDiv.style.display = 'flex';
                contadorSpan.textContent = cant;
            } else {
                contadorDiv.style.display = 'none';
            }
        }
        if (cant >= MINIMO_JUGADORAS) {
            btnConfirmar.style.display = 'inline-block';
        } else {
            btnConfirmar.style.display = 'none';
        }
    }

    // Cargar precarga existente y tildar checks
    async function aplicarPrecargaExistente(partidoId) {
        const target = isOperador ? clubTargetId : (clubId ? parseInt(clubId) : null);
        if (!partidoId || !target) return;
        try {
            const res = await fetch(`/partidos/${partidoId}/precarga?club_id=${encodeURIComponent(target)}`);
            if (!res.ok) return;
            const lista = await res.json(); // [{jugadora_id}]
            const ids = new Set(lista.map(x => String(x.jugadora_id)));
            tablaJugadoras.querySelectorAll('.seleccionar-jugadora').forEach(cb => {
                const jid = cb.getAttribute('data-id');
                if (!cb.disabled) cb.checked = ids.has(String(jid));
            });
            actualizarBotonConfirmar();
        } catch (_) { /* noop */ }
    }

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        msg.textContent = '';
        jugadorasSection.style.display = 'block';
        tablaJugadoras.innerHTML = '';

        // Obtener valores seleccionados
        const categoria = categoriaSelect.value;
        const partidoId = partidoSelect.value;
        if (!partidoId) {
            msg.textContent = 'Selecciona un partido';
            msg.style.color = 'red';
            return;
        }
        // Si es operador, debe elegir club destino
        const targetClub = isOperador ? clubTargetId : (clubId ? parseInt(clubId) : null);
        if (isOperador && !targetClub) {
            msg.textContent = 'Selecciona el club a precargar';
            msg.style.color = 'red';
            return;
        }
        // Puedes agregar más filtros si lo deseas (rama, bloque, etc)
        try {
            let url = `/jugadoras?club_id=${encodeURIComponent(targetClub)}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error('Error al obtener jugadoras');
            let jugadoras = await response.json();
            // Filtrar por categoría si corresponde
            if (categoria) {
                jugadoras = jugadoras.filter(j => {
                    if (!j.categoria) return false;
                    // Normalizar ambos valores para comparar
                    return norm(j.categoria) === norm(categoria);
                });
            }
            // Obtener lista de suspendidos para este partido/club
            let suspendidosSet = new Set();
            let suspendidosMotivo = {};
            try {
                const rs = await fetch(`/partidos/${encodeURIComponent(partidoId)}/suspensiones?club_id=${encodeURIComponent(targetClub)}`);
                if (rs.ok) {
                    const arr = await rs.json();
                    (arr || []).forEach(it => { suspendidosSet.add(String(it.jugadora_id)); suspendidosMotivo[String(it.jugadora_id)] = it.motivo; });
                }
            } catch(_){}
            if (jugadoras.length === 0) {
                tablaJugadoras.innerHTML = '<tr><td colspan="6" style="color:red;">No hay jugadoras para esta categoría</td></tr>';
                return;
            }
            jugadoras.forEach(jugadora => {
                const fila = document.createElement('tr');
                const sid = String(jugadora.id);
                const estaSuspendida = suspendidosSet.has(sid);
                fila.innerHTML = `
                    <td>${jugadora.dni || ''}</td>
                    <td>${jugadora.apellido || ''}</td>
                    <td>${jugadora.nombre || ''}</td>
                    <td>${jugadora.categoria || ''}</td>
                `;
                const tdSeleccionar = document.createElement('td');
                tdSeleccionar.style.textAlign = 'center';
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'seleccionar-jugadora';
                checkbox.setAttribute('data-id', jugadora.id);
                if (estaSuspendida) {
                    checkbox.disabled = true;
                    // Fondo un poco más intenso para resaltar suspensión
                    fila.style.background = '#ffcdd2'; // antes: #ffebee
                    fila.style.color = '#b71c1c';
                    const motivo = suspendidosMotivo[sid] || 'suspensión';
                    fila.title = motivo === 'roja' ? 'Suspendido por tarjeta roja (1 partido)'
                              : (motivo === '3_amarillas' ? 'Suspendido por 3 amarillas (1 partido)'
                              : (motivo === '5_verdes' ? 'Suspendido por 5 verdes (1 partido)' : 'Suspendido'));
                }
                tdSeleccionar.appendChild(checkbox);
                fila.appendChild(tdSeleccionar);
                tablaJugadoras.appendChild(fila);
            });

            // Lógica para limitar la selección a 20 jugadoras
            tablaJugadoras.addEventListener('change', function(e) {
                if (e.target.classList.contains('seleccionar-jugadora')) {
                    const seleccionadas = tablaJugadoras.querySelectorAll('.seleccionar-jugadora:checked');
                    if (seleccionadas.length > LIMITE_JUGADORAS) {
                        e.target.checked = false;
                        msg.textContent = `Solo puedes seleccionar hasta ${LIMITE_JUGADORAS} jugadoras.`;
                        msg.style.color = 'red';
                    } else {
                        msg.textContent = '';
                    }
                    actualizarBotonConfirmar();
                }
            });

            // Intentar aplicar precarga existente
            await aplicarPrecargaExistente(partidoId);
            actualizarBotonConfirmar();
        } catch (e) {
            tablaJugadoras.innerHTML = '<tr><td colspan="6" style="color:red;">No se pudieron cargar las jugadoras</td></tr>';
        }
    });

    // Guardar precarga
    btnConfirmar.addEventListener('click', async function() {
        const partidoId = partidoSelect.value;
        const targetClub = isOperador ? clubTargetId : (clubId ? parseInt(clubId) : null);
        if (!targetClub) {
            msg.textContent = 'Selecciona el club a precargar';
            msg.style.color = 'red';
            return;
        }
        const seleccionadas = Array.from(tablaJugadoras.querySelectorAll('.seleccionar-jugadora:checked')).map(cb => parseInt(cb.getAttribute('data-id')));
        if (seleccionadas.length < MINIMO_JUGADORAS) {
            msg.textContent = `Debes seleccionar al menos ${MINIMO_JUGADORAS} jugadoras para la precarga.`;
            msg.style.color = 'red';
            return;
        }
        if (seleccionadas.length > LIMITE_JUGADORAS) {
            msg.textContent = `Solo puedes seleccionar hasta ${LIMITE_JUGADORAS} jugadoras.`;
            msg.style.color = 'red';
            return;
        }
        try {
            const res = await fetch(`/partidos/${encodeURIComponent(partidoId)}/precarga`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ club_id: targetClub, jugadora_ids: seleccionadas })
            });
            if (!res.ok) {
                const j = await res.json().catch(() => ({}));
                throw new Error(j.error || 'Error al guardar la precarga');
            }
            msg.textContent = 'Precarga guardada correctamente.';
            msg.style.color = 'green';
        } catch (err) {
            msg.textContent = err.message || 'No se pudo guardar la precarga';
            msg.style.color = 'red';
        }
    });

    // Inicial
    actualizarCategorias();
    cargarFechas();
    cargarPartidos();
    });
