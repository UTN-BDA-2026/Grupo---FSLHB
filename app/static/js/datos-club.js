// datos-club.js
// Carga los datos del club desde el backend y los muestra en los campos del formulario

// Utilidad para obtener el club_id del usuario logueado
function getClubId() {
    return localStorage.getItem('club_id');
}

document.addEventListener('DOMContentLoaded', async () => {
    const clubId = getClubId();
    if (!clubId) {
        // Operador sin club: redirigir al panel
        window.location.replace('/panel-clubes');
        return;
    }
    try {
    const response = await fetch(`/clubs/${clubId}`);
        if (!response.ok) throw new Error('No se pudo obtener los datos del club');
        const club = await response.json();
        document.getElementById('club-name').textContent = club.nombre || '';
        document.getElementById('nombre-club').value = club.nombre || '';
        document.getElementById('razon-social').value = club.razon_social || '';
        document.getElementById('contacto').value = club.contacto || '';
        document.getElementById('email').value = club.email || '';
        document.getElementById('cancha-local').value = club.cancha_local || '';
        document.getElementById('domicilio').value = club.domicilio || '';
        document.getElementById('telefono').value = club.telefono || '';
        document.getElementById('web').value = club.web || '';
        // document.getElementById('arbitro').value = club.arbitro_id || '';
    } catch (err) {
        alert(err.message);
    }
});
