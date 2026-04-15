document.addEventListener('DOMContentLoaded', () => {
    const dropdownToggle = document.querySelector('.panel-nav-dropdown-toggle');
    const dropdownMenu = document.querySelector('.panel-nav-dropdown');

    // Lógica para mostrar mensaje al agregar jugadora
    const formJugadora = document.getElementById('form-jugadora');
    const formMsg = document.getElementById('form-msg');
    if (formJugadora) {
        formJugadora.addEventListener('submit', async function(e) {
            e.preventDefault();
            const clubId = localStorage.getItem('club_id');
            const data = {
                dni: formJugadora.dni.value,
                apellido: formJugadora.apellido.value,
                nombre: formJugadora.nombre.value,
                fecha_nacimiento: formJugadora.fecha_nacimiento.value,
                categoria: formJugadora.categoria.value,
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
                    formMsg.textContent = 'Jugadora agregada correctamente';
                    formMsg.style.color = 'green';
                    formJugadora.reset();
                    setTimeout(() => { formMsg.textContent = ''; }, 2500);

                    // Si la página de jugadores está abierta, recargar la tabla automáticamente
                    if (window.location.pathname.includes('jugadores.html')) {
                        if (typeof cargarJugadoras === 'function') {
                            cargarJugadoras();
                        } else {
                            // Forzar recarga si no se puede llamar a la función
                            window.location.reload();
                        }
                    }
                } else {
                    formMsg.textContent = 'Error al agregar jugadora';
                    formMsg.style.color = 'red';
                    setTimeout(() => { formMsg.textContent = ''; }, 2500);
                }
            } catch (err) {
                formMsg.textContent = 'Error de conexión';
                formMsg.style.color = 'red';
                setTimeout(() => { formMsg.textContent = ''; }, 2500);
            }
        });
    }

    dropdownToggle.addEventListener('mouseenter', () => {
        dropdownMenu.style.display = 'block';
    });

    dropdownToggle.addEventListener('mouseleave', () => {
        if (!dropdownMenu.matches(':hover')) {
            dropdownMenu.style.display = 'none';
        }
    });

    dropdownMenu.addEventListener('mouseleave', () => {
        dropdownMenu.style.display = 'none';
    });

    dropdownMenu.addEventListener('mouseenter', () => {
        dropdownMenu.style.display = 'block';
    });
});
