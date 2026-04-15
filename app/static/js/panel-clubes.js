// Mostrar identidad en el panel y comportarse distinto si es operador (sin club)

document.addEventListener('DOMContentLoaded', function() {
    const clubNombre = localStorage.getItem('nombreClub');
    const clubId = localStorage.getItem('club_id');
    const usuario = localStorage.getItem('usuario');
    const isOperador = localStorage.getItem('isOperador') === 'true' || !clubId;

    // Mostrar nombre del club u 'Mesa de Control' en la barra
    const clubNav = document.getElementById('nombre-club-nav');
    if (clubNav) {
    clubNav.textContent = (clubNombre && clubNombre.trim() !== '') ? clubNombre : 'Mesa de Control';
    }

    // Nunca redirigir por falta de club: los operadores pueden ingresar
    if (!usuario) {
        // Si no hay sesión, ir al login
        window.location.href = '/login';
        return;
    }

    // Ocultar menú "Parámetros del Club" si es operador
    const paramLink = document.getElementById('param-club-link');
    const paramContainer = paramLink ? paramLink.closest('.panel-nav-dropdown-container') : null;
    if (isOperador && paramContainer) {
        paramContainer.style.display = 'none';
    }

    // Carga de datos específica del club solo si hay clubId
    if (clubId) {
        fetch(`/jugadoras?club_id=${encodeURIComponent(clubId)}`)
            .then(res => res.json())
            .then(jugadoras => {
                console.log('Jugadoras del club:', jugadoras);
            });
    }

    // --- Tablas secundarias: goleadores y tarjetas ---
    // Selects inferiores (sección Posiciones)
    const posTorneoSel = document.getElementById('pos-torneo-select');
    const posDivisionSel = document.getElementById('pos-division-select');
    // Selects superiores (encabezado de la página)
    const topTorneoSel = document.getElementById('torneo-select');
    const topDivisionSel = document.getElementById('division-select');
    const topFechaSel = document.getElementById('fecha-select');

    const tbGoleadores = document.querySelector('#tabla-goleadores tbody');
    const tbAmarillas = document.querySelector('#tabla-tarjetas-amarillas tbody');
    const tbRojas = document.querySelector('#tabla-tarjetas-rojas tbody');
    const btnXLSX = document.getElementById('descargar-goleadores-excel');
    const btnTarjetasXLSX = document.getElementById('descargar-tarjetas-excel');

    function renderRows(tbody, rows, cols) {
        if (!tbody) return;
        if (!Array.isArray(rows) || rows.length === 0) {
            tbody.innerHTML = `<tr><td colspan="${cols}" style="text-align:center;color:#888;">Sin datos</td></tr>`;
            return;
        }
        tbody.innerHTML = rows.map(r => {
            // r tiene {club, jugador, cantidad}
            const club = r.club || '';
            const jugador = r.jugador || '';
            const cant = r.cantidad != null ? r.cantidad : (r.goles || r.tarjetas || 0);
            return `<tr><td>${club}</td><td title="${jugador}">${jugador}</td><td style=\"text-align:center;font-weight:700;\">${cant}</td></tr>`;
        }).join('');
    }

    function getFiltros() {
        // Priorizar selects superiores; si no existen, usar los de posiciones
        const torneo = (topTorneoSel && topTorneoSel.value) || (posTorneoSel && posTorneoSel.value) || '';
        const categoria = (topDivisionSel && topDivisionSel.value) || (posDivisionSel && posDivisionSel.value) || '';
        const fecha = (topFechaSel && topFechaSel.value) || '';
        return { torneo, categoria, fecha };
    }

    async function cargarTablasSecundarias() {
        if (!tbGoleadores || !tbAmarillas || !tbRojas) return;
    const { torneo, categoria, fecha } = getFiltros();
    // Log de depuración opcional
    console.debug('Cargando tablas secundarias con:', { torneo, categoria, fecha });
        const params = new URLSearchParams();
        if (torneo) params.append('torneo', torneo);
        if (categoria) params.append('categoria', categoria);
        if (fecha) params.append('fecha', fecha);

        tbGoleadores.innerHTML = '<tr><td colspan="3" style="text-align:center;color:#888;">Cargando...</td></tr>';
        tbAmarillas.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;">Cargando...</td></tr>';
        tbRojas.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;">Cargando...</td></tr>';

        try {
            const res = await fetch(`/ranking/resumen?${params.toString()}`);
            const data = await res.json();
            // data: { goleadores: [{club,jugador,cantidad}], amarillas: [...], rojas: [...] }
            renderRows(tbGoleadores, data.goleadores, 3);
            // Para amarillas y rojas, hay una primera columna vacía en el thead para rank/icono; la mantenemos con una celda vacía
            if (Array.isArray(data.amarillas) && data.amarillas.length) {
                tbAmarillas.innerHTML = data.amarillas.map((r, idx) => `
                    <tr><td style="text-align:center;color:#777;">${idx + 1}</td><td>${r.club || ''}</td><td title="${r.jugador || ''}">${r.jugador || ''}</td><td style="text-align:center;font-weight:700;">${r.cantidad || 0}</td></tr>
                `).join('');
            } else {
                tbAmarillas.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;">Sin datos</td></tr>';
            }
            if (Array.isArray(data.rojas) && data.rojas.length) {
                tbRojas.innerHTML = data.rojas.map((r, idx) => `
                    <tr><td style="text-align:center;color:#777;">${idx + 1}</td><td>${r.club || ''}</td><td title="${r.jugador || ''}">${r.jugador || ''}</td><td style="text-align:center;font-weight:700;">${r.cantidad || 0}</td></tr>
                `).join('');
            } else {
                tbRojas.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;">Sin datos</td></tr>';
            }
        } catch (e) {
            tbGoleadores.innerHTML = '<tr><td colspan="3" style="text-align:center;color:red;">Error al cargar</td></tr>';
            tbAmarillas.innerHTML = '<tr><td colspan="4" style="text-align:center;color:red;">Error al cargar</td></tr>';
            tbRojas.innerHTML = '<tr><td colspan="4" style="text-align:center;color:red;">Error al cargar</td></tr>';
        }

        if (btnXLSX) {
            const xParams = new URLSearchParams();
            if (torneo) xParams.append('torneo', torneo);
            if (categoria) xParams.append('categoria', categoria);
            if (fecha) xParams.append('fecha', fecha);
            btnXLSX.href = `/ranking/goleadores/excel?${xParams.toString()}`;
        }
        if (btnTarjetasXLSX) {
            const tParams = new URLSearchParams();
            if (torneo) tParams.append('torneo', torneo);
            if (categoria) tParams.append('categoria', categoria);
            if (fecha) tParams.append('fecha', fecha);
            btnTarjetasXLSX.href = `/ranking/tarjetas/excel?${tParams.toString()}`;
        }
    }

    // Disparar actualización cuando cambian torneo/categoría o fecha
    if (posTorneoSel) posTorneoSel.addEventListener('change', cargarTablasSecundarias);
    if (posDivisionSel) posDivisionSel.addEventListener('change', cargarTablasSecundarias);
    if (topFechaSel) topFechaSel.addEventListener('change', cargarTablasSecundarias);
    if (topTorneoSel) topTorneoSel.addEventListener('change', cargarTablasSecundarias);
    if (topDivisionSel) topDivisionSel.addEventListener('change', cargarTablasSecundarias);

    // Carga inicial
    cargarTablasSecundarias();
});
