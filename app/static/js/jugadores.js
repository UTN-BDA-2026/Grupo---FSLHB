async function cargarJugadoras() {
    const tablaJugadores = document.getElementById('tabla-jugadores').querySelector('tbody');
    tablaJugadores.innerHTML = '';
    try {
        const clubId = localStorage.getItem('club_id');
    const response = await fetch(`/jugadoras?club_id=${clubId}`);
        if (!response.ok) throw new Error('Error al obtener jugadoras');
        let jugadoras = await response.json();
        // Filtro por categoría si se selecciona alguna
        const filtro = (document.getElementById('filtro-categoria')?.value || '').trim();
        if (filtro) {
            const norm = (s)=> (s||'').toString().trim().toUpperCase();
            jugadoras = jugadoras.filter(j => norm(j.categoria) === norm(filtro));
        }
        jugadoras.forEach(jugadora => {
            const nuevaFila = document.createElement('tr');
            // Formatear fecha de nacimiento a DD-MM-YYYY
            let fechaFormateada = '';
            if (jugadora.fecha_nacimiento) {
                const partes = jugadora.fecha_nacimiento.split('-');
                if (partes.length === 3) {
                    fechaFormateada = `${partes[2]}-${partes[1]}-${partes[0]}`;
                } else {
                    fechaFormateada = jugadora.fecha_nacimiento;
                }
            }
            nuevaFila.innerHTML = `
                <td>${jugadora.dni || ''}</td>
                <td>${jugadora.apellido || ''}</td>
                <td>${jugadora.nombre || ''}</td>
                <td>${fechaFormateada}</td>
                <td>${jugadora.categoria || ''}</td>
                <td><button class="btn-borrar-jugador" onclick="borrarJugador(${jugadora.id}, this)"><i class='fas fa-trash'></i> Borrar</button></td>
            `;
            tablaJugadores.appendChild(nuevaFila);
        });
    } catch (e) {
    const row = document.createElement('tr');
    row.innerHTML = `<td colspan="6" style="color:red;">No se pudieron cargar las jugadoras</td>`;
    tablaJugadores.appendChild(row);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Re-cargar al cambiar el filtro
    const filtroSel = document.getElementById('filtro-categoria');
    if (filtroSel) {
        filtroSel.addEventListener('change', cargarJugadoras);
    }
    const formJugadora = document.getElementById('form-jugadora');
    if (formJugadora) {
        formJugadora.addEventListener('submit', async function(event) {
            event.preventDefault();
            const form = event.target;
            const msg = document.getElementById('form-msg');
            msg.textContent = '';
            const clubId = localStorage.getItem('club_id');
            const data = {
                dni: form.dni.value,
                apellido: form.apellido.value,
                nombre: form.nombre.value,
                fecha_nacimiento: form.fecha_nacimiento.value,
                division: form.categoria.value,
                club_id: clubId
            };
            try {
                const response = await fetch('/jugadoras', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                if(response.ok) {
                    msg.style.color = 'green';
                    msg.textContent = 'Jugadora agregada correctamente';
                    form.reset();
                    cargarJugadoras();
                    setTimeout(() => {
                        msg.textContent = '';
                    }, 3000);
                } else {
                    msg.style.color = 'red';
                    if (response.status === 409) {
                        const errorData = await response.json();
                        msg.textContent = errorData.error || 'Ya existe una jugadora con ese DNI';
                    } else {
                        msg.textContent = 'Error al agregar jugadora';
                    }
                    setTimeout(() => {
                        msg.textContent = '';
                    }, 4000);
                }
            } catch (e) {
                msg.style.color = 'red';
                msg.textContent = 'Error de conexión';
            }
        });
    }
    cargarJugadoras();
});

async function borrarJugador(id, btn) {
    if (!confirm('¿Seguro que desea borrar este jugador?')) return;
    try {
        const response = await fetch(`/jugadoras/${id}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            // Eliminar la fila del DOM
            const fila = btn.closest('tr');
            fila.remove();
        } else {
            alert('No se pudo borrar el jugador');
        }
    } catch (e) {
        alert('Error de conexión al borrar jugador');
    }
}
