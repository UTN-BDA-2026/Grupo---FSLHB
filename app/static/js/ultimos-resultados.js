// ultimos-resultados.js
// Renderiza los últimos resultados dinámicamente y permite filtrar por categoría

document.addEventListener('DOMContentLoaded', function() {
    const resultadosLista = document.getElementById('ultimos-resultados');
    const resultadosSection = document.getElementById('ultimos-resultados-section');
    if (!resultadosLista || !resultadosSection) return;

    // Estilos para centrar la lista y sus elementos
    resultadosLista.style.listStyle = 'none';
    resultadosLista.style.padding = '0';
    resultadosLista.style.margin = '0';
    resultadosLista.style.display = 'flex';
    resultadosLista.style.flexDirection = 'column';
    resultadosLista.style.alignItems = 'center';
    resultadosLista.style.gap = '10px';

    // Crear selector de categoría
    const selector = document.createElement('select');
    selector.id = 'categoria-resultados-selector';
    selector.style.display = 'block';
    selector.style.margin = '0.5rem 0 1rem 0';
    selector.style.clear = 'both';
    selector.innerHTML = '<option value="">Todas las categorías</option>' +
        ['Damas A', 'Damas B', 'Damas C', 'Caballeros', 'Mamis'].map(cat =>
            `<option value="${cat}">${cat}</option>`).join('');
    const heading = resultadosSection.querySelector('h2');
    if (heading) {
        heading.insertAdjacentElement('afterend', selector);
    } else {
        resultadosSection.insertBefore(selector, resultadosLista.parentElement);
    }

    function renderResultados(categoria = '') {
        resultadosLista.innerHTML = '<li style="color:#888;">Cargando...</li>';
        let url = '/resultados/ultimos';
        if (categoria) url += `?categoria=${encodeURIComponent(categoria)}`;
        fetch(url)
            .then(res => res.json())
            .then(data => {
                if (!Array.isArray(data) || data.length === 0) {
                    resultadosLista.innerHTML = '<li style="color:#d32f2f;font-weight:600;">No hay resultados para la selección.</li>';
                    return;
                }
                resultadosLista.innerHTML = data.map(r =>
                    `<li style="text-align:center;">` +
                    `<span>${r.local}</span> <span style="font-weight:bold;">${r.goles_local != null ? r.goles_local : 0}</span> : <span style="font-weight:bold;">${r.goles_visitante != null ? r.goles_visitante : 0}</span> <span>${r.visitante}</span> ` +
                    `<span style="font-size:0.95em;color:#555;">(${r.categoria})</span>` +
                    `</li>`
                ).join('');
            })
            .catch(() => {
                resultadosLista.innerHTML = '<li style="color:red;">Error al cargar resultados</li>';
            });
    }

    selector.addEventListener('change', function() {
        renderResultados(selector.value);
    });

    renderResultados(); // Inicial
});
