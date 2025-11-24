// equipos-categorias.js
// Este script carga dinámicamente la tabla de equipos y categorías desde el backend

document.addEventListener('DOMContentLoaded', async () => {
    const tabla = document.querySelector('#tabla-equipos-categorias tbody');
    tabla.innerHTML = '<tr><td colspan="4">Cargando...</td></tr>';
    try {
        // Cambia la URL según tu backend
    const response = await fetch('/api/equipos-categorias');
        if (!response.ok) throw new Error('Error al obtener los datos');
        const datos = await response.json();
        if (!Array.isArray(datos) || datos.length === 0) {
            tabla.innerHTML = '<tr><td colspan="4">No hay datos para mostrar</td></tr>';
            return;
        }
        tabla.innerHTML = '';
        datos.forEach(e => {
            const fila = document.createElement('tr');
            fila.innerHTML = `
                <td>${e.rama && e.rama.trim() !== '' ? e.rama : '—'}</td>
                <td>${e.division && e.division.trim() !== '' ? e.division : '—'}</td>
                <td>${e.bloque && e.bloque.trim() !== '' ? e.bloque : '—'}</td>
                <td>${e.jugadores || 0}</td>
            `;
            tabla.appendChild(fila);
        });
    } catch (err) {
        tabla.innerHTML = `<tr><td colspan="4" style="color:red;">${err.message}</td></tr>`;
    }
});
