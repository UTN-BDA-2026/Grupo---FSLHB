// JS para precarga de equipos por club

document.addEventListener('DOMContentLoaded', function() {
    const clubId = localStorage.getItem('club_id');
    const tablaEquipos = document.getElementById('tabla-equipos').querySelector('tbody');
    const form = document.getElementById('form-equipo');
    const msg = document.getElementById('form-msg');

    async function cargarEquipos() {
        tablaEquipos.innerHTML = '';
        try {
            const response = await fetch(`/equipos?club_id=${clubId}&estado_not=jugado`);
            if (!response.ok) throw new Error('Error al obtener equipos');
            const equipos = await response.json();
            equipos.forEach(equipo => {
                const fila = document.createElement('tr');
                fila.innerHTML = `
                    <td>${equipo.nombre || ''}</td>
                    <td>${equipo.categoria || ''}</td>
                    <td><button class="btn-borrar" data-id="${equipo.id}">Borrar</button></td>
                `;
                tablaEquipos.appendChild(fila);
            });
            document.querySelectorAll('.btn-borrar').forEach(btn => {
                btn.addEventListener('click', async function() {
                    const id = this.getAttribute('data-id');
                    try {
                        const response = await fetch(`/equipos/${id}`, {
                            method: 'DELETE'
                        });
                        if(response.ok) {
                            msg.style.color = 'green';
                            msg.textContent = 'Equipo eliminado correctamente';
                            cargarEquipos();
                            setTimeout(() => { msg.textContent = ''; }, 3000);
                        } else {
                            msg.style.color = 'red';
                            msg.textContent = 'Error al eliminar equipo';
                            setTimeout(() => { msg.textContent = ''; }, 3000);
                        }
                    } catch (e) {
                        msg.style.color = 'red';
                        msg.textContent = 'Error de conexión';
                        setTimeout(() => { msg.textContent = ''; }, 3000);
                    }
                });
            });
        } catch (e) {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="3" style="color:red;">No se pudieron cargar los equipos</td>`;
            tablaEquipos.appendChild(row);
        }
    }

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        msg.textContent = '';
        const data = {
            nombre: form.nombre.value,
            categoria: form.categoria.value,
            club_id: clubId
        };
        try {
            const response = await fetch('/equipos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if(response.ok) {
                msg.style.color = 'green';
                msg.textContent = 'Equipo agregado correctamente';
                form.reset();
                cargarEquipos();
                setTimeout(() => { msg.textContent = ''; }, 3000);
            } else {
                msg.style.color = 'red';
                msg.textContent = 'Error al agregar equipo';
                setTimeout(() => { msg.textContent = ''; }, 3000);
            }
        } catch (e) {
            msg.style.color = 'red';
            msg.textContent = 'Error de conexión';
            setTimeout(() => { msg.textContent = ''; }, 3000);
        }
    });

    cargarEquipos();
});
