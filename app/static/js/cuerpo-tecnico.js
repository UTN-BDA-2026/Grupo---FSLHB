// Cuerpo Técnico: manejo de formulario y tabla con backend

const API_URL = '/cuerpo-tecnico/';
const rawClubId = localStorage.getItem('club_id');
const clubId = rawClubId ? parseInt(String(rawClubId).replace(/[^0-9]/g, ''), 10) : null;

function fetchCuerpoTecnico() {
    return fetch(API_URL + '?club_id=' + clubId)
        .then(async r => {
            if (!r.ok) {
                const text = await r.text();
                throw new Error('Listado falló: ' + text);
            }
            return r.json();
        });
}

function crearCuerpoTecnico(data) {
    return fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(async r => {
        if (!r.ok) {
            const text = await r.text();
            throw new Error('Crear falló: ' + text);
        }
        return r.json();
    });
}

function actualizarCuerpoTecnico(id, data) {
    return fetch(API_URL + id, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(async r => {
        if (!r.ok) {
            const text = await r.text();
            throw new Error('Actualizar falló: ' + text);
        }
        return r.json();
    });
}

function eliminarCuerpoTecnico(id) {
    return fetch(API_URL + id, {
        method: 'DELETE'
    }).then(async r => {
        if (!r.ok) {
            const text = await r.text();
            throw new Error('Eliminar falló: ' + text);
        }
        return r.json();
    });
}

function renderTabla(rows) {
    const tbody = document.querySelector('#tabla-ct tbody');
    tbody.innerHTML = rows.length ? '' : '<tr><td colspan="5" style="color:#666;text-align:center;">Sin integrantes cargados</td></tr>';
    rows.forEach((r, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${escapeHtml(r.nombre||'')}</td>
            <td>${escapeHtml(r.apellido||'')}</td>
            <td>${escapeHtml(r.dni||'')}</td>
            <td>${escapeHtml(roleLabel(r.rol)||'')}</td>
            <td style="text-align:center; vertical-align: middle;">
                <button class="panel-btn" data-del="${r.id}" type="button" style="padding:4px 10px;font-size:12px;line-height:12px;background:#e53935;border-color:#e53935;display:inline-block;">Eliminar</button>
            </td>`;
        tbody.appendChild(tr);
    });
}

function escapeHtml(s){ return String(s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c])); }

function roleLabel(code) {
    const map = {
        'DT': 'Director Técnico',
        'PF': 'Preparador Físico'
    };
    return map[code] || code;
}

function cargarTabla() {
    fetchCuerpoTecnico().then(renderTabla);
}

function limpiarForm() {
    document.getElementById('ct-nombre').value = '';
    document.getElementById('ct-apellido').value = '';
    document.getElementById('ct-dni').value = '';
    document.getElementById('ct-rol').value = 'DT';
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-ct');
    const msg = document.getElementById('ct-msg');
    const tbody = document.querySelector('#tabla-ct tbody');

    if (!clubId || Number.isNaN(clubId)) {
        msg.textContent = 'club_id inválido o ausente';
        msg.style.color = '#e53935';
        return;
    }
    cargarTabla();

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const data = {
            club_id: clubId,
            nombre: document.getElementById('ct-nombre').value.trim(),
            apellido: document.getElementById('ct-apellido').value.trim(),
            dni: document.getElementById('ct-dni').value.trim(),
            rol: document.getElementById('ct-rol').value
        };
        if (!data.nombre || !data.apellido || !data.dni) return;
        crearCuerpoTecnico(data).then(() => {
            msg.textContent = 'Agregado';
            msg.style.color = '#16a34a';
            setTimeout(()=> msg.textContent = '', 1500);
            limpiarForm();
            cargarTabla();
        }).catch(err => {
            console.error(err);
            msg.textContent = 'Error: ' + err.message;
            msg.style.color = '#e53935';
            setTimeout(()=> { msg.textContent=''; msg.style.color = '#16a34a'; }, 2500);
        });
    });

    tbody.addEventListener('click', function(e) {
        const idDel = e.target.getAttribute('data-del');
        if (idDel) {
            eliminarCuerpoTecnico(idDel).then(() => cargarTabla());
            return;
        }
    });
});
