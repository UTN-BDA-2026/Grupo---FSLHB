// main.js
// Aquí puedes agregar funcionalidades JS generales para la web
console.log('Página de Hockey sobre Césped cargada');

// Lógica general para la página principal (index.html)
document.addEventListener('DOMContentLoaded', function() {
    const fechaHoy = document.getElementById('fecha-hoy');
    if (fechaHoy) {
        const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
        const hoy = new Date();
        fechaHoy.textContent = `${hoy.getDate()} de ${meses[hoy.getMonth()]} de ${hoy.getFullYear()}`;
    }

    // Menú desplegable: delegación de eventos (más robusto)
    const mainMenu = document.getElementById('main-menu');
    const menuToggleBtn = document.querySelector('.menu-toggle');
    if (mainMenu) {
        mainMenu.addEventListener('click', function(e) {
            const toggle = e.target.closest('.submenu-toggle');
            if (!toggle) return; // no es click en el toggle
            e.preventDefault();
            e.stopPropagation();
            const li = toggle.closest('.submenu');
            const dropdown = li ? li.querySelector('.dropdown') : null;
            if (!dropdown) return;
            // Cierra otros abiertos
            document.querySelectorAll('.dropdown.open').forEach(function(el){
                if (el !== dropdown) el.classList.remove('open');
            });
            const willOpen = !dropdown.classList.contains('open');
            dropdown.classList.toggle('open', willOpen);
            // accesibilidad
            toggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
        });

        // Hover solo escritorio para mejor UX
        mainMenu.querySelectorAll('.submenu').forEach(function(submenu){
            const dropdown = submenu.querySelector('.dropdown');
            if (!dropdown) return;
            submenu.addEventListener('mouseenter', function(){
                if (window.innerWidth > 900) dropdown.classList.add('open');
            });
            submenu.addEventListener('mouseleave', function(){
                if (window.innerWidth > 900) dropdown.classList.remove('open');
            });
        });
    }

    // Botón hamburguesa (móvil): abre/cierra el menú principal
    if (mainMenu && menuToggleBtn) {
        menuToggleBtn.addEventListener('click', function(e){
            e.stopPropagation();
            const isOpen = mainMenu.classList.toggle('open');
            menuToggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
        // Cerrar menú al elegir una opción en móvil, excepto al abrir submenú
        mainMenu.addEventListener('click', function(e){
            if (window.innerWidth <= 900) {
                // Si el click fue en el toggle del submenú, no cerrar el menú hamburguesa
                if (e.target.closest('.submenu-toggle')) return;
                const link = e.target.closest('a');
                if (link) {
                    mainMenu.classList.remove('open');
                    menuToggleBtn.setAttribute('aria-expanded', 'false');
                }
            }
        });
    }

    // Cierra al hacer clic fuera
    document.addEventListener('click', function(e){
        if (!e.target.closest('.submenu')) {
            document.querySelectorAll('.dropdown.open').forEach(function(el){ el.classList.remove('open'); });
        }
        // Si se hace click fuera del nav, cerrar menú móvil
        const clickedInsideNav = e.target.closest && e.target.closest('nav');
        if (!clickedInsideNav && mainMenu && menuToggleBtn) {
            if (mainMenu.classList.contains('open')) {
                mainMenu.classList.remove('open');
                menuToggleBtn.setAttribute('aria-expanded', 'false');
            }
        }
    });

    // Escape para cerrar
    document.addEventListener('keydown', function(e){
        if (e.key === 'Escape') {
            document.querySelectorAll('.dropdown.open').forEach(function(el){ el.classList.remove('open'); });
            if (mainMenu && menuToggleBtn && mainMenu.classList.contains('open')) {
                mainMenu.classList.remove('open');
                menuToggleBtn.setAttribute('aria-expanded', 'false');
            }
        }
    });

});
