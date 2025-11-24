// JS dedicado para filtros de Control de Partidos

document.addEventListener('DOMContentLoaded', function() {
    const torneoSelect = document.getElementById('torneo-control-select');
    const categoriaSelect = document.getElementById('categoria-control-select');
    const fechaSelect = document.getElementById('fecha-control-select');
    const encuentroSelect = document.getElementById('encuentro-control-select');
    const detalleSection = document.getElementById('control-partido-detalle');
    const resumenDiv = document.getElementById('control-partido-resumen');
    const cuerpoTecnicoContainer = document.getElementById('control-partido-cuerpo-tecnico');
    const golesDiv = document.getElementById('control-partido-goles');
    // Cargar logos de clubes
    let clubesLogos = {};
    let clubesNombres = [];
    fetch('/static/data/clubes.json').then(r => r.json()).then(data => {
        data.forEach(c => {
            clubesLogos[c.nombre] = c.logo;
            clubesNombres.push(c.nombre);
        });
    });
    const tarjetasDiv = document.getElementById('control-partido-tarjetas');
    const msgDiv = document.getElementById('control-partido-msg');
    const incidenciasDiv = document.getElementById('control-partido-incidencias');

    const categoriasPorTorneo = {
        'Clausura Damas (2025)': [
            { value: 'Damas A', text: 'Damas A' },
            { value: 'Damas B', text: 'Damas B' },
            { value: 'Damas C', text: 'Damas C' }
        ],
        'Clausura Caballeros (2025)': [
            { value: 'Caballeros', text: 'Caballeros' }
        ],
        'Clausura Mamis (2025)': [
            { value: 'Mamis', text: 'Mamis' }
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

    function limpiarFechasYEncuentros() {
        fechaSelect.innerHTML = '<option value="">Seleccione Fecha</option>';
        encuentroSelect.innerHTML = '<option value="">Seleccione Encuentro</option>';
        detalleSection.style.display = 'none';
        resumenDiv.innerHTML = '';
        if (cuerpoTecnicoContainer) cuerpoTecnicoContainer.innerHTML = '';
    }

    torneoSelect.addEventListener('change', function() {
        actualizarCategorias();
        limpiarFechasYEncuentros();
    });

    categoriaSelect.addEventListener('change', async function() {
        limpiarFechasYEncuentros();
        // Cargar fechas disponibles para ese torneo/categoría que tengan partidos jugados
        const torneoQuery = (torneoSelect.value || '').replace(/\s*\(\d{4}\)\s*$/, '').trim();
        const categoriaQuery = (categoriaSelect.value || '').trim();
        if (!torneoQuery || !categoriaQuery) return;
        try {
            msgDiv.textContent = '';
            // Operador (sin club) NO debe filtrar por club
            const nombreClub = localStorage.getItem('nombreClub');
            const isOperador = (localStorage.getItem('isOperador') || '').toString() === 'true';
            const rawClubId = localStorage.getItem('club_id');
            const clubId = (nombreClub && !isOperador && rawClubId) ? rawClubId : null;
            const base = `/partidos?torneo=${encodeURIComponent(torneoQuery)}&categoria=${encodeURIComponent(categoriaQuery)}${clubId?`&club_id=${encodeURIComponent(clubId)}`:''}`;
            // primero intentamos solo jugados
            let res = await fetch(`${base}&estado=jugado`);
            let partidos = res.ok ? await res.json() : [];
            if (!Array.isArray(partidos) || partidos.length === 0) {
                // fallback: cualquier estado
                res = await fetch(base);
                partidos = res.ok ? await res.json() : [];
                if (partidos.length === 0) {
                    msgDiv.textContent = 'No hay partidos cargados para este torneo y categoría.';
                    return;
                }
                msgDiv.textContent = 'Aún no hay partidos cerrados. Se muestran todas las fechas disponibles.';
            }
            const fechas = [...new Set(partidos.map(p => p.fecha_numero).filter(f => f != null))].sort((a,b)=>a-b);
            if (fechas.length === 0) {
                // si no hay fecha_numero, permitir saltar directo a encuentros sin filtrar por fecha
                await cargarEncuentros(torneoQuery, categoriaQuery, null, partidos);
                return;
            }
            // Agregar opción 'Todas'
            const optTodas = document.createElement('option');
            optTodas.value = 'todas';
            optTodas.textContent = 'Todas';
            fechaSelect.appendChild(optTodas);
            fechas.forEach(f => {
                const opt = document.createElement('option');
                opt.value = String(f);
                opt.textContent = `Fecha ${f}`;
                fechaSelect.appendChild(opt);
            });
            // Por defecto, con 'Todas' seleccionada, mostrar todos los encuentros jugados
            await cargarEncuentros(torneoQuery, categoriaQuery, null, partidos);
        } catch(_){}
    });

    async function cargarEncuentros(torneoQuery, categoriaQuery, fecha, partidosPrefetch) {
        encuentroSelect.innerHTML = '<option value="">Seleccione Encuentro</option>';
        detalleSection.style.display = 'none';
        resumenDiv.innerHTML = '';
        try {
            let partidos = partidosPrefetch;
            if (!partidos) {
                const nombreClub = localStorage.getItem('nombreClub');
                const isOperador = (localStorage.getItem('isOperador') || '').toString() === 'true';
                const rawClubId = localStorage.getItem('club_id');
                const clubId = (nombreClub && !isOperador && rawClubId) ? rawClubId : null;
                let url = `/partidos?torneo=${encodeURIComponent(torneoQuery)}&categoria=${encodeURIComponent(categoriaQuery)}${clubId?`&club_id=${encodeURIComponent(clubId)}`:''}`;
                if (fecha != null) url += `&fecha_numero=${fecha}`;
                // Preferir jugados; si no hay, caer a todos
                let res = await fetch(url + `&estado=jugado`);
                partidos = res.ok ? await res.json() : [];
                if (!Array.isArray(partidos) || partidos.length === 0) {
                    res = await fetch(url);
                    partidos = res.ok ? await res.json() : [];
                }
            }
            partidos.forEach(p => {
                const opt = document.createElement('option');
                const local = p.equipo_local_nombre || p.club_local_nombre || 'Local';
                const visit = p.equipo_visitante_nombre || p.club_visitante_nombre || 'Visitante';
                const label = `${local} vs ${visit}`;
                opt.value = p.id;
                opt.textContent = label;
                opt.title = label;
                encuentroSelect.appendChild(opt);
            });
        } catch(_){}
    }

    fechaSelect.addEventListener('change', async function() {
        const torneoQuery = (torneoSelect.value || '').replace(/\s*\(\d{4}\)\s*$/, '').trim();
        const categoriaQuery = (categoriaSelect.value || '').trim();
        const fecha = (fechaSelect.value && fechaSelect.value !== 'todas') ? parseInt(fechaSelect.value, 10) : null;
        if (!torneoQuery || !categoriaQuery) return;
        await cargarEncuentros(torneoQuery, categoriaQuery, fecha, null);
    });

    encuentroSelect.addEventListener('change', async function() {
        detalleSection.style.display = 'none';
        resumenDiv.innerHTML = '';
    golesDiv.innerHTML = '';
    tarjetasDiv.innerHTML = '';
    incidenciasDiv.innerHTML = '';
    const partidoId = encuentroSelect.value;
        if (!partidoId) return;
        try {
            // 1. Datos del partido
            const res = await fetch(`/partidos/${encodeURIComponent(partidoId)}`);
            if (!res.ok) return;
            const p = await res.json();

            // 1b. Cuerpo técnico (DT/PF) para ambos clubes
            let cuerpoTecnicoPorClub = {};
            // También tendremos disponibles por club para fallback (si no hay seleccionados)
            const ctDisponiblesPorClub = {};
            try {
                const resCT = await fetch(`/partidos/${encodeURIComponent(partidoId)}/cuerpo-tecnico`);
                if (resCT.ok) {
                    const dataCT = await resCT.json();
                    // dataCT.seleccionados: [{club_id, rol, cuerpo_tecnico_id}]
                    // Agrupar por club y rol
                    cuerpoTecnicoPorClub = {};
                    for (const ct of (dataCT.seleccionados || [])) {
                        if (!cuerpoTecnicoPorClub[ct.club_id]) cuerpoTecnicoPorClub[ct.club_id] = {};
                        cuerpoTecnicoPorClub[ct.club_id][ct.rol] = ct.cuerpo_tecnico_id;
                    }
                }
            } catch (e) { cuerpoTecnicoPorClub = {}; }
            const local = p.equipo_local_nombre || p.club_local_nombre || 'Local';
            const visit = p.equipo_visitante_nombre || p.club_visitante_nombre || 'Visitante';
            const fecha = p.fecha_numero ? `Fecha ${p.fecha_numero}` : (p.fecha_hora ? new Date(p.fecha_hora).toLocaleString() : '');
            const cancha = p.cancha || '';
            const estado = p.estado || '';
            // 2. Incidencias (goles y tarjetas)
            const resInc = await fetch(`/partidos/${encodeURIComponent(partidoId)}/incidencias`);
            const incidencias = resInc.ok ? await resInc.json() : [];
            // Agrupar por club
            const clubs = {};
            [p.club_local_id, p.club_visitante_id].forEach(cid => {
                clubs[cid] = { goles: 0, amarillas: 0, rojas: 0, verdes: 0 };
            });
            incidencias.forEach(inc => {
                if (!clubs[inc.club_id]) return;
                if (inc.tipo === 'gol') clubs[inc.club_id].goles++;
                if (inc.tipo === 'tarjeta') {
                    if (inc.color === 'amarilla') clubs[inc.club_id].amarillas++;
                    if (inc.color === 'roja') clubs[inc.club_id].rojas++;
                    if (inc.color === 'verde') clubs[inc.club_id].verdes++;
                }
            });
            // 3. Calcular resultado si no está en el modelo
            let resultado;
            if (p.goles_local != null && p.goles_visitante != null) {
                resultado = `${p.goles_local} - ${p.goles_visitante}`;
            } else {
                resultado = `${clubs[p.club_local_id].goles} - ${clubs[p.club_visitante_id].goles}`;
            }
            // Logos
            function normalizar(s) {
                return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9 ]/gi, '').trim();
            }
            function logoHtml(nombreEquipo, nombreClub) {
                // 1. Coincidencia exacta club
                let src = clubesLogos[nombreClub];
                // 2. Coincidencia exacta equipo
                if (!src && clubesLogos[nombreEquipo]) src = clubesLogos[nombreEquipo];
                // 3. Coincidencia parcial club
                if (!src) {
                    const normClub = normalizar(nombreClub);
                    for (const n of clubesNombres) {
                        if (normalizar(n).includes(normClub) || normClub.includes(normalizar(n))) {
                            src = clubesLogos[n];
                            break;
                        }
                    }
                }
                // 4. Coincidencia parcial equipo
                if (!src) {
                    const normEquipo = normalizar(nombreEquipo);
                    for (const n of clubesNombres) {
                        if (normalizar(n).includes(normEquipo) || normEquipo.includes(normalizar(n))) {
                            src = clubesLogos[n];
                            break;
                        }
                    }
                }
                // 5. Fallback genérico
                if (!src) src = 'assets/img/logo-asociacion.png';
                return `<img src="/static/${src}" alt="${nombreEquipo}" style="height:64px;max-width:120px;margin-bottom:0.5rem;">`;
            }
            // 4. Render resumen
            const cacheBust = Date.now();
            const linkPlanilla = (estado && estado.toLowerCase() === 'jugado')
                ? `<div style="margin-top:10px;"><a class="panel-btn" href="/partidos/${encodeURIComponent(partidoId)}/planilla.pdf?t=${cacheBust}" target="_blank" rel="noopener">Descargar planilla PDF</a></div>`
                : '';
            resumenDiv.innerHTML = `
                <div><b>${fecha}</b> | ${cancha}</div>
                <div style="font-size:1.2rem; margin:0.25rem 0;"><b>${local}</b> vs <b>${visit}</b></div>
                <div><b>Estado:</b> ${estado} | <b>Resultado:</b> ${resultado}</div>
                ${linkPlanilla}
            `;
            // 5. Mostrar goles por equipo
            golesDiv.innerHTML = `
                <div style="text-align:center;">
                    ${logoHtml(local, p.club_local_nombre)}
                    <div style="font-size:2.5rem;font-weight:bold;color:#1976d2;">${clubs[p.club_local_id].goles}</div>
                    <div style="margin-top:0.5rem;">Goles: ${local}</div>
                </div>
                <div style="text-align:center;">
                    ${logoHtml(visit, p.club_visitante_nombre)}
                    <div style="font-size:2.5rem;font-weight:bold;color:#1976d2;">${clubs[p.club_visitante_id].goles}</div>
                    <div style="margin-top:0.5rem;">Goles: ${visit}</div>
                </div>
            `;
            // 6. Mostrar tarjetas por equipo
            function circle(color, count) {
                return `<span style="display:inline-block;width:38px;height:38px;border-radius:50%;background:${color};color:#fff;font-weight:bold;font-size:1.2rem;line-height:38px;text-align:center;margin:0 6px;">${count}</span>`;
            }
            tarjetasDiv.innerHTML = `
                <div style="text-align:center;">
                    ${circle('#e53935', clubs[p.club_local_id].rojas)}
                    ${circle('#fbc02d', clubs[p.club_local_id].amarillas)}
                    ${circle('#43a047', clubs[p.club_local_id].verdes)}
                    <div style="margin-top:0.5rem;">Tarjetas: ${local}</div>
                </div>
                <div style="text-align:center;">
                    ${circle('#e53935', clubs[p.club_visitante_id].rojas)}
                    ${circle('#fbc02d', clubs[p.club_visitante_id].amarillas)}
                    ${circle('#43a047', clubs[p.club_visitante_id].verdes)}
                    <div style="margin-top:0.5rem;">Tarjetas: ${visit}</div>
                </div>
            `;
            // 7. Mostrar jugadoras e incidencias por equipo
            function tarjetaIcon(color) {
                const map = { 'roja': '#e53935', 'amarilla': '#fbc02d', 'verde': '#43a047' };
                return `<span style="display:inline-block;width:22px;height:22px;border-radius:50%;background:${map[color]||'#888'};color:#fff;font-size:1rem;line-height:22px;text-align:center;margin-right:4px;vertical-align:middle;">${color[0].toUpperCase()}</span>`;
            }
            function tipoIcon(tipo) {
                if (tipo === 'gol') return '<span style="color:#1976d2;font-weight:bold;margin-right:4px;">⚽</span>';
                if (tipo === 'tarjeta') return '';
                return '';
            }
            function incLabel(inc) {
                if (inc.tipo === 'gol') return `${tipoIcon('gol')}Gol`;
                if (inc.tipo === 'tarjeta') return `${tarjetaIcon(inc.color)}Tarjeta ${inc.color}`;
                return inc.tipo || '';
            }

            async function fetchJugadoras(equipoId, clubId, categoria) {
                try {
                    if (equipoId) {
                        const r = await fetch(`/jugadoras?equipo_id=${encodeURIComponent(equipoId)}`);
                        if (r.ok) return await r.json();
                    }
                    // Fallback por club
                    const r2 = await fetch(`/jugadoras?club_id=${encodeURIComponent(clubId)}`);
                    let arr = r2.ok ? await r2.json() : [];
                    if (categoria) {
                        const catNorm = String(categoria || '').toLowerCase();
                        arr = arr.filter(j => String(j.categoria || '').toLowerCase() === catNorm);
                    }
                    return arr;
                } catch { return []; }
            }

            function renderJugadorasTabla(jugadoras, clubId, clubLabel) {
                // Mapear incidencias por jugadora para este club
                const incsClub = incidencias.filter(i => i.club_id === clubId);
                const mapByPlayer = new Map();
                for (const inc of incsClub) {
                    if (!mapByPlayer.has(inc.jugadora_id)) mapByPlayer.set(inc.jugadora_id, []);
                    mapByPlayer.get(inc.jugadora_id).push(inc);
                }
                // Ordenar jugadoras por apellido, nombre
                jugadoras = (jugadoras || []).slice().sort((a,b)=>{
                    const an = `${a.apellido||''} ${a.nombre||''}`.toLowerCase();
                    const bn = `${b.apellido||''} ${b.nombre||''}`.toLowerCase();
                    return an.localeCompare(bn);
                });
                // Estilos llamativos para la tabla
                const tableStyle = `
                    width:100%;
                    max-width:720px;
                    border-collapse:separate;
                    border-spacing:0;
                    background:#fff;
                    border-radius:14px;
                    box-shadow:0 2px 12px #0001;
                    margin-top:1.2rem;
                    overflow:hidden;
                    table-layout:fixed;
                `;
                const thStyle = `
                    padding:10px 16px;
                    background:#1976d2;
                    color:#fff;
                    font-weight:700;
                    text-align:center;
                    position:sticky;
                    top:0;
                    z-index:2;
                    border-bottom:2px solid #1565c0;
                    letter-spacing:0.5px;
                    word-break:break-word;white-space:normal;overflow-wrap:anywhere;
                `;
                const tdStyle = `padding:9px 14px;font-size:1.05rem;transition:background 0.2s;word-break:break-word;white-space:normal;overflow-wrap:anywhere;text-align:center;`;
                let html = `<div class=\"tabla-equipo\" style=\"text-align:center;\"><div style=\"font-weight:bold;font-size:1.18rem;margin-bottom:0.7rem;letter-spacing:0.5px;\">${clubLabel}</div>`;
                // Placeholder for cuerpo técnico info (to be rendered outside this function)
                html += `<div style=\"width:100%;max-width:720px;margin:0 auto;overflow:hidden;\"><table style=\"${tableStyle}\">`;
                html += `<thead><tr>
                        <th style="${thStyle}">Jugador</th>
                        <th style="${thStyle}">DNI</th>
                        <th style="${thStyle}">Incidencia</th>
                        <th style="${thStyle}">Minuto</th>
                    </tr></thead><tbody>`;
                let row = 0;
                for (const j of jugadoras) {
                    const incs = mapByPlayer.get(j.id) || [];
                    if (incs.length === 0) {
                        html += `<tr style="background:${row%2===0?'#f5f8ff':'#fff'};transition:background 0.2s;">`+
                            `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;">${j.nombre} ${j.apellido}</td>`+
                            `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;">${j.dni || ''}</td>`+
                            `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;"></td>`+
                            `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;"></td>`+
                        `</tr>`;
                        row++;
                    } else {
                        for (const inc of incs) {
                            html += `<tr style="background:${row%2===0?'#f5f8ff':'#fff'};transition:background 0.2s;">`+
                                `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;">${j.nombre} ${j.apellido}</td>`+
                                `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;">${j.dni || ''}</td>`+
                                `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;">${incLabel(inc)}</td>`+
                                `<td style="${tdStyle}border-bottom:1px solid #e3e8f0;">${inc.minuto != null ? inc.minuto : ''}</td>`+
                            `</tr>`;
                            row++;
                        }
                    }
                }
                html += '</tbody></table></div></div>';
                return html;
            }

            // Renderizar tablas usando SOLO la precarga (alineaciones) del partido
            let jugLocal = [], jugVisit = [];
            try {
                const rAli = await fetch(`/partidos/${encodeURIComponent(partidoId)}/alineaciones`);
                if (rAli.ok) {
                    const ali = await rAli.json();
                    // Estructura: { club_local: {id, nombre, jugadoras: [...]}, club_visitante: {...} }
                    if (ali && ali.club_local && Array.isArray(ali.club_local.jugadoras)) jugLocal = ali.club_local.jugadoras;
                    if (ali && ali.club_visitante && Array.isArray(ali.club_visitante.jugadoras)) jugVisit = ali.club_visitante.jugadoras;
                }
            } catch {}
            incidenciasDiv.innerHTML =
                renderJugadorasTabla(jugLocal, p.club_local_id, local) +
                renderJugadorasTabla(jugVisit, p.club_visitante_id, visit);

            // Prepare to render cuerpo técnico info after the resumenDiv
            // We'll render this after the resumenDiv, before the golesDiv
            let cuerpoTecnicoHtml = '';
            async function fetchCTInfo(ctId) {
                if (!ctId) return null;
                try {
                    const r = await fetch(`/cuerpo-tecnico/${ctId}`);
                    if (r.ok) return await r.json();
                } catch {}
                return null;
            }
            // For both clubs, fetch DT and PF info if available
            const clubIds = [p.club_local_id, p.club_visitante_id];
            // Mostrar el nombre del equipo (si existe); fallback al nombre del club
            const clubLabels = [local || p.club_local_nombre, visit || p.club_visitante_nombre];
            cuerpoTecnicoHtml += '<div style="display:flex;justify-content:center;gap:3rem;margin:1.2rem 0 0.5rem 0;flex-wrap:wrap;">';
            for (let i = 0; i < clubIds.length; i++) {
                const cid = clubIds[i];
                const label = clubLabels[i];
                cuerpoTecnicoHtml += `<div style="min-width:220px;text-align:left;background:#f5f8ff;padding:0.7rem 1.2rem;border-radius:10px;box-shadow:0 1px 6px #0001;">`;
                cuerpoTecnicoHtml += `<div style="font-weight:bold;font-size:1.08rem;margin-bottom:0.3rem;">${label}</div>`;
                cuerpoTecnicoHtml += '<ul style="list-style:none;padding:0;margin:0;">';
                for (const rol of ['director_tecnico', 'preparador_fisico']) {
                    const pretty = rol === 'director_tecnico' ? 'Director Técnico' : 'Preparador Físico';
                    const ctId = (cuerpoTecnicoPorClub[cid]||{})[rol];
                    cuerpoTecnicoHtml += `<li style="margin-bottom:0.2rem;">`;
                    // Siempre renderizamos el mismo span con id para poder actualizarlo luego
                    const initial = ctId ? 'Cargando...' : 'No asignado';
                    const color = ctId ? '#111' : '#888';
                    cuerpoTecnicoHtml += `<span style="font-weight:600;">${pretty}:</span> <span id="ct-nombre-${cid}-${rol}" style="color:${color};">${initial}</span>`;
                    cuerpoTecnicoHtml += `</li>`;
                }
                cuerpoTecnicoHtml += '</ul></div>';
            }
            cuerpoTecnicoHtml += '</div>';
            // Render into dedicated container to avoid duplicados entre cambios
            if (cuerpoTecnicoContainer) {
                cuerpoTecnicoContainer.innerHTML = cuerpoTecnicoHtml;
            } else {
                // Fallback: si no existe el contenedor, insertar tras el resumen
                resumenDiv.insertAdjacentHTML('afterend', cuerpoTecnicoHtml);
            }
            // Now fetch and fill names for each DT/PF
            for (let i = 0; i < clubIds.length; i++) {
                const cid = clubIds[i];
                for (const rol of ['director_tecnico', 'preparador_fisico']) {
                    const ctId = (cuerpoTecnicoPorClub[cid]||{})[rol];
                    if (ctId) {
                        fetch(`/cuerpo-tecnico/${ctId}`).then(r=>r.ok?r.json():null).then(data=>{
                            if (data && data.nombre && data.apellido) {
                                const el = document.getElementById(`ct-nombre-${cid}-${rol}`);
                                if (el) el.textContent = `${data.nombre} ${data.apellido}`;
                            }
                        });
                    } else {
                        // Fallback: si no hay seleccionado para este partido, y hay exactamente uno disponible para ese rol en el club, mostrarlo como referencia del club
                        // Evita mostrar algo incorrecto cuando hay múltiples candidatos
                        if (!ctDisponiblesPorClub[cid]) {
                            try {
                                const r = await fetch(`/partidos/${encodeURIComponent(partidoId)}/cuerpo-tecnico?club_id=${encodeURIComponent(cid)}`);
                                if (r.ok) {
                                    const j = await r.json();
                                    ctDisponiblesPorClub[cid] = Array.isArray(j.disponibles) ? j.disponibles : [];
                                }
                            } catch { ctDisponiblesPorClub[cid] = []; }
                        }
                        const lista = ctDisponiblesPorClub[cid] || [];
                        const norm = (s) => String(s||'').toLowerCase();
                        const candidatos = lista.filter(x => {
                            const r = norm(x.rol);
                            return rol === 'director_tecnico' ? /(^|\W)(dt|director\s*tecnic)/.test(r) : /(^|\W)(pf|preparador\s*fisic)/.test(r);
                        });
                        if (candidatos.length === 1) {
                            const el = document.getElementById(`ct-nombre-${cid}-${rol}`);
                            if (el) el.textContent = `${candidatos[0].nombre || ''} ${candidatos[0].apellido || ''} (del club)`;
                        }
                    }
                }
            }
            detalleSection.style.display = 'block';
        } catch(_){}
    });

    // Inicial
    actualizarCategorias();
});
