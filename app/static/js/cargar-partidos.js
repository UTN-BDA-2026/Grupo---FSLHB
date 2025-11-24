// Admin: Cargar y listar Partidos
(function(){
  const torneoSel = document.getElementById('torneo');
  const categoriaSel = document.getElementById('categoria');
  const fechaNum = document.getElementById('fecha_numero');
  const bloque = document.getElementById('bloque');
  const fechaHora = document.getElementById('fecha_hora');
  const cancha = document.getElementById('cancha');
  const eqLocal = document.getElementById('equipo_local');
  const eqVisit = document.getElementById('equipo_visitante');
  const btnCrear = document.getElementById('btn-crear');
  const msg = document.getElementById('msg');
  const tablaBody = document.querySelector('#tabla-partidos tbody');
  const filtroTorneo = document.getElementById('filtro_torneo');
  const filtroCategoria = document.getElementById('filtro_categoria');
  const btnRefrescar = document.getElementById('btn-refrescar');

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

  function setCategorias(sel, torneo) {
    sel.innerHTML = '<option value="">Seleccione Categoría</option>';
    const arr = categoriasPorTorneo[torneo] || [];
    arr.forEach(c => { const o = document.createElement('option'); o.value=c.value; o.textContent=c.text; sel.appendChild(o); });
  }

  torneoSel.addEventListener('change', () => setCategorias(categoriaSel, torneoSel.value));
  filtroTorneo.addEventListener('change', () => setCategorias(filtroCategoria, filtroTorneo.value));

  async function cargarEquipos() {
    // Carga todos los equipos y luego filtramos por categoría si se desea
    try {
  const res = await fetch('/equipos');
      if (!res.ok) throw new Error('No se pudieron obtener equipos');
      const equipos = await res.json();
      function poblar(select, categoria) {
        select.innerHTML = '<option value="">Seleccione Equipo</option>';
        equipos
          .filter(e => !categoria || (e.categoria && e.categoria.toLowerCase().replace(/\s+/g,'_') === categoria))
          .forEach(e => { const o=document.createElement('option'); o.value=e.id; o.textContent=`${e.nombre} (${e.categoria||'-'})`; select.appendChild(o); });
      }
      const cat = categoriaSel.value;
      poblar(eqLocal, cat);
      poblar(eqVisit, cat);
    } catch (e) {
      msg.textContent = e.message;
    }
  }

  categoriaSel.addEventListener('change', cargarEquipos);

  function validar() {
    msg.style.color = 'red';
    if (!torneoSel.value) return 'Seleccione torneo';
    if (!categoriaSel.value) return 'Seleccione categoría';
    if (!eqLocal.value) return 'Seleccione equipo local';
    if (!eqVisit.value) return 'Seleccione equipo visitante';
    if (eqLocal.value === eqVisit.value) return 'El local y visitante no pueden ser el mismo equipo';
    return '';
  }

  btnCrear.addEventListener('click', async () => {
    msg.textContent = '';
    const err = validar();
    if (err) { msg.textContent = err; return; }
    const payload = {
      torneo: torneoSel.value,
      categoria: categoriaSel.value,
      fecha_numero: fechaNum.value ? parseInt(fechaNum.value) : null,
      bloque: bloque.value || null,
      fecha_hora: fechaHora.value || null,
      cancha: cancha.value || null,
      equipo_local_id: parseInt(eqLocal.value),
      equipo_visitante_id: parseInt(eqVisit.value)
    };
    try {
  const res = await fetch('/partidos', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      const j = await res.json().catch(()=>({}));
      if (!res.ok) throw new Error(j.error || 'No se pudo crear el partido');
      msg.style.color = 'green';
      msg.textContent = `Partido creado (ID ${j.id}).`;
      await listar();
    } catch (e) {
      msg.style.color = 'red';
      msg.textContent = e.message;
    }
  });

  function fmtFechaHora(iso) {
    if (!iso) return ['',''];
    const d = new Date(iso);
    const dd = String(d.getDate()).padStart(2,'0');
    const mm = String(d.getMonth()+1).padStart(2,'0');
    const yyyy = d.getFullYear();
    const hh = String(d.getHours()).padStart(2,'0');
    const mi = String(d.getMinutes()).padStart(2,'0');
    return [`${dd}/${mm}/${yyyy}`, `${hh}:${mi}`];
  }

  async function listar() {
    try {
      const params = new URLSearchParams();
      if (filtroTorneo.value) params.append('torneo', filtroTorneo.value);
      if (filtroCategoria.value) params.append('categoria', filtroCategoria.value);
  const res = await fetch(`/partidos?${params.toString()}`);
      if (!res.ok) throw new Error('No se pudieron listar partidos');
      const arr = await res.json();
      tablaBody.innerHTML = '';
      arr.forEach(p => {
        const tr = document.createElement('tr');
        const [f, h] = fmtFechaHora(p.fecha_hora);
        const encuentro = `#${p.id} - ${p.categoria || ''}`;
        tr.innerHTML = `
          <td>${p.id}</td>
          <td>${p.torneo || ''}</td>
          <td>${p.categoria || ''}</td>
          <td>${f}</td>
          <td>${h}</td>
          <td>${encuentro}</td>
          <td>${p.cancha || ''}</td>
        `;
        tablaBody.appendChild(tr);
      });
    } catch (e) {
      msg.textContent = e.message;
    }
  }

  // Inicial
  setCategorias(categoriaSel, torneoSel.value);
  setCategorias(filtroCategoria, filtroTorneo.value);
  cargarEquipos();
  listar();
})();