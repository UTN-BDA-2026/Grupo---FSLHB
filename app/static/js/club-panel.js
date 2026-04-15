// club-panel.js
// Lógica JS para el panel de clubes

// Mostrar la fecha actual en la barra superior
const fechaHoy = document.getElementById('fecha-hoy');
if (fechaHoy) {
    const hoy = new Date();
    const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
    fechaHoy.textContent = `${hoy.getDate()} de ${meses[hoy.getMonth()]} de ${hoy.getFullYear()}`;
}

// Simulación de navegación interna
const panelContent = document.getElementById('panel-content');

document.getElementById('cargar-jugadoras').onclick = function(e) {
    e.preventDefault();
    renderFormularioJugadora();
};

document.getElementById('cargar-resultados').onclick = function(e) {
    e.preventDefault();
    renderFormularioResultado();
};

document.getElementById('ver-listado').onclick = function(e) {
    e.preventDefault();
    panelContent.innerHTML = '<h3>Listado de Jugadoras</h3><p>Listado de jugadoras del club (a implementar)...</p>';
};

document.getElementById('historial-partidos').onclick = function(e) {
    e.preventDefault();
    panelContent.innerHTML = '<h3>Historial de Partidos</h3><p>Listado de partidos jugados por el club (a implementar)...</p>';
};

document.getElementById('descargar-planilla').onclick = function(e) {
    e.preventDefault();
    panelContent.innerHTML = '<h3>Descargar Planilla</h3><p>Descarga de planillas en PDF/Excel (a implementar)...</p>';
};

document.getElementById('notificaciones').onclick = function(e) {
    e.preventDefault();
    panelContent.innerHTML = '<h3>Notificaciones</h3><p>Avisos y mensajes de la asociación (a implementar)...</p>';
};

document.getElementById('perfil-club').onclick = function(e) {
    e.preventDefault();
    panelContent.innerHTML = '<h3>Perfil del Club</h3><p>Datos del club, logo y contacto (a implementar)...</p>';
};

document.getElementById('soporte').onclick = function(e) {
    e.preventDefault();
    panelContent.innerHTML = '<h3>Soporte</h3><p>Ayuda y contacto con la asociación (a implementar)...</p>';
};

document.getElementById('logout').onclick = function(e) {
    e.preventDefault();
    window.location.href = 'login.html';
};

document.getElementById('tribunal-penas').onclick = function(e) {
    e.preventDefault();
    renderTribunalPenas();
};

let sanciones = JSON.parse(localStorage.getItem('sanciones') || '[]');

function renderTribunalPenas() {
    panelContent.innerHTML = `
        <h3>Tribunal de Penas</h3>
        <div class="jugadoras-lista" id="penas-lista"></div>
        <p style="font-size:0.97rem;color:#666;margin-top:1.2rem;">Las sanciones se generan automáticamente a partir de los reportes de partidos.</p>
    `;
    renderListaSanciones();
}

// Esta función puede ser llamada desde la lógica de resultados para agregar una sanción
window.agregarSancionAutomatica = function({nombre, dni, division, partidos, motivo}) {
    sanciones.push({ nombre, dni, division, partidos, motivo });
    localStorage.setItem('sanciones', JSON.stringify(sanciones));
};

function renderListaSanciones() {
    const cont = document.getElementById('penas-lista');
    if (!cont) return;
    if (sanciones.length === 0) {
        cont.innerHTML = '<p>No hay sanciones activas.</p>';
        return;
    }
    cont.innerHTML = sanciones.map((s) => `
        <div class="jugadora-card">
            <div class="info">
                <strong>${s.nombre}</strong><br>
                DNI: ${s.dni}<br>
                División: ${s.division}<br>
                Partidos de sanción: <b>${s.partidos}</b><br>
                Motivo: ${s.motivo}
            </div>
        </div>
    `).join('');
}

// --- Lógica para Cargar Jugadoras ---
let jugadoras = JSON.parse(localStorage.getItem('jugadoras') || '[]');

function renderFormularioJugadora() {
    panelContent.innerHTML = `
        <h3>Cargar Jugadora</h3>
        <form id="jugadora-form" class="jugadora-form" autocomplete="off">
            <label>Nombre y Apellido<input type="text" id="nombre" required></label>
            <label>DNI<input type="number" id="dni" required></label>
            <label>Fecha de Nacimiento<input type="date" id="nacimiento" required></label>
            <label>División
                <select id="division" required>
                    <option value="">Seleccionar</option>
                    <option value="Primera">Primera</option>
                    <option value="Intermedia">Intermedia</option>
                    <option value="Juveniles">Juveniles</option>
                </select>
            </label>
            <label>Foto<input type="file" id="foto" accept="image/*"></label>
            <button type="submit">Agregar Jugadora</button>
        </form>
        <div class="jugadoras-lista" id="jugadoras-lista"></div>
    `;
    document.getElementById('jugadora-form').onsubmit = agregarJugadora;
    renderListaJugadoras();
}

function agregarJugadora(e) {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value.trim();
    const dni = document.getElementById('dni').value.trim();
    const nacimiento = document.getElementById('nacimiento').value;
    const division = document.getElementById('division').value;
    const fotoInput = document.getElementById('foto');
    if (jugadoras.some(j => j.dni === dni)) {
        alert('Ya existe una jugadora con ese DNI.');
        return;
    }
    let fotoUrl = '';
    if (fotoInput.files && fotoInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(ev) {
            fotoUrl = ev.target.result;
            guardarJugadora({ nombre, dni, nacimiento, division, foto: fotoUrl });
        };
        reader.readAsDataURL(fotoInput.files[0]);
    } else {
        guardarJugadora({ nombre, dni, nacimiento, division, foto: '' });
    }
}

function guardarJugadora(jugadora) {
    jugadoras.push(jugadora);
    localStorage.setItem('jugadoras', JSON.stringify(jugadoras));
    renderFormularioJugadora();
}

function renderListaJugadoras() {
    const cont = document.getElementById('jugadoras-lista');
    if (!cont) return;
    if (jugadoras.length === 0) {
        cont.innerHTML = '<p>No hay jugadoras cargadas.</p>';
        return;
    }
    cont.innerHTML = jugadoras.map((j, idx) => `
        <div class="jugadora-card">
            <img src="${j.foto || '../assets/img/default-avatar.png'}" alt="Foto" onerror="this.src='../assets/img/default-avatar.png'">
            <div class="info">
                <strong>${j.nombre}</strong><br>
                DNI: ${j.dni}<br>
                Nac: ${j.nacimiento}<br>
                División: ${j.division}
            </div>
            <button onclick="window.eliminarJugadora(${idx})">Eliminar</button>
        </div>
    `).join('');
    // Exponer función para eliminar
    window.eliminarJugadora = function(idx) {
        if (confirm('¿Eliminar jugadora?')) {
            jugadoras.splice(idx, 1);
            localStorage.setItem('jugadoras', JSON.stringify(jugadoras));
            renderFormularioJugadora();
        }
    };
}

// --- Lógica para Cargar Resultados ---
function renderFormularioResultado() {
    panelContent.innerHTML = `
        <h3>Cargar Resultado</h3>
        <form id="resultado-form" class="jugadora-form">
            <label>Fecha<input type="date" id="fecha-partido" required></label>
            <label>Club Local<input type="text" id="local" required></label>
            <label>Club Visitante<input type="text" id="visitante" required></label>
            <label>Goles Local<input type="number" id="goles-local" min="0" required></label>
            <label>Goles Visitante<input type="number" id="goles-visitante" min="0" required></label>
            <label>Tarjetas<input type="text" id="tarjetas" placeholder="Ej: 2 amarillas, 1 roja"></label>
            <label>Lesiones<input type="text" id="lesiones" placeholder="Opcional"></label>
            <label>Jugadoras Presentes<input type="text" id="presentes" placeholder="Separar por coma"></label>
            <button type="submit">Cargar Resultado</button>
        </form>
        <div id="resultado-feedback"></div>
    `;
    document.getElementById('resultado-form').onsubmit = function(e) {
        e.preventDefault();
        document.getElementById('resultado-feedback').innerHTML = '<p style="color:green;">Resultado enviado. Falta confirmación del otro club.</p>';
        // Aquí se podría guardar en localStorage o enviar a backend
    };
}

// Ejemplo de cómo agregar una sanción automáticamente desde la lógica de resultados:
// window.agregarSancionAutomatica({
//   nombre: 'Ana Pérez',
//   dni: '12345678',
//   division: 'Primera',
//   partidos: 2,
//   motivo: 'Tarjeta roja en partido 10/07/2025'
// });

// Menú hamburguesa para móvil en panel de club
const menuToggle = document.getElementById('panelMenuToggle');
const panelMenu = document.getElementById('panelMenu');
if(menuToggle && panelMenu){
    menuToggle.addEventListener('click', () => {
        panelMenu.classList.toggle('open');
    });
}
