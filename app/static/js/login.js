document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');

    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const usuario = loginForm.usuario.value.trim();
        const password = loginForm.password.value.trim();

        try {
            // Usar ruta relativa para funcionar igual en http/https y detrás de Traefik
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: usuario,
                    password: password
                })
            });

            if (response.ok) {
                const data = await response.json();

                // Limpiar claves antiguas para evitar que queden valores de una sesión previa
                ['club_id','club_nombre','clubName','nombreClub','isOperador'].forEach(k => localStorage.removeItem(k));

                // Guardar información de club de forma unificada
                if (data.club) {
                    localStorage.setItem('club_id', String(data.club.id));
                    localStorage.setItem('nombreClub', data.club.nombre || '');
                    localStorage.setItem('isOperador', 'false');
                } else {
                    // Usuario operador (sin club asociado)
                    localStorage.setItem('isOperador', 'true');
                }

                // Guardar usuario si se desea
                localStorage.setItem('usuario', data.username);

                // Redirigir según tipo de usuario
                if (data.is_admin) {
                    window.location.href = '/admin-panel';
                } else {
                    window.location.href = '/panel-clubes';
                }
            } else {
                loginError.style.display = 'block';
            }

        } catch (error) {
            console.error('Error al conectar con el servidor:', error);
            loginError.innerText = 'Error del servidor. Intente más tarde.';
            loginError.style.display = 'block';
        }
    });
});