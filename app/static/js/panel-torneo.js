// panel-torneo.js
// Lógica para guardar selección de torneo, categoría (division) y fecha en la API

document.addEventListener('DOMContentLoaded', function() {
    const torneoForm = document.getElementById('torneo-form');
    // Mapeo de categorías por torneo
    const categoriasPorTorneo = {
        'Clausura Caballeros': ['Caballeros'],
        'Clausura Damas': ['Damas A', 'Damas B', 'Damas C'],
        'Clausura Mamis': ['Mamis']
    };

    function setOpcionesCategoria(selectCategoria, torneoValue) {
        if (!selectCategoria) return;
        const opciones = categoriasPorTorneo[torneoValue] || ['Damas A', 'Damas B', 'Damas C', 'Caballeros', 'Mamis'];
        const previo = selectCategoria.value;
        selectCategoria.innerHTML = '';
        opciones.forEach(txt => {
            const opt = document.createElement('option');
            opt.value = txt;
            opt.textContent = txt;
            selectCategoria.appendChild(opt);
        });
        if (opciones.includes(previo)) {
            selectCategoria.value = previo;
        }
    }

    // Referencias a selects de torneo/categoría (superior e inferior)
    const torneoTop = document.getElementById('torneo-select');
    const categoriaTop = document.getElementById('division-select');
    const torneoPos = document.getElementById('pos-torneo-select');
    const categoriaPos = document.getElementById('pos-division-select');

    // Cargar opciones de torneos desde la API para que coincidan con
    // los torneos administrados en el panel de "Gestión de Torneos".
    (async () => {
        if (!torneoTop && !torneoPos) return;
        try {
            const resp = await fetch('/torneo/seleccion');
            if (!resp.ok) return;
            const torneos = await resp.json();
            if (!Array.isArray(torneos) || torneos.length === 0) return;

            const rellenarSelect = (selectEl) => {
                if (!selectEl) return;
                const previo = selectEl.value;
                selectEl.innerHTML = '';
                torneos.forEach(t => {
                    const opt = document.createElement('option');
                    opt.value = t.nombre;
                    opt.textContent = t.nombre;
                    selectEl.appendChild(opt);
                });
                // Intentar conservar valor previo si sigue existiendo
                if (previo) {
                    const existe = torneos.some(t => t.nombre === previo);
                    if (existe) {
                        selectEl.value = previo;
                    }
                }
            };

            rellenarSelect(torneoTop);
            rellenarSelect(torneoPos);

            // Reajustar categorías según el torneo seleccionado
            if (torneoTop && categoriaTop) {
                setOpcionesCategoria(categoriaTop, torneoTop.value);
            }
            if (torneoPos && categoriaPos) {
                setOpcionesCategoria(categoriaPos, torneoPos.value);
            }
        } catch (err) {
            console.error('No se pudieron cargar los torneos para los selects', err);
        }
    })();

    // Top form: torneo-select controla division-select (categoría)
    if (torneoTop && categoriaTop) {
        // set inicial
        setOpcionesCategoria(categoriaTop, torneoTop.value);
        torneoTop.addEventListener('change', () => {
            setOpcionesCategoria(categoriaTop, torneoTop.value);
        });
    }

    // Tabla posiciones form: pos-torneo-select controla pos-division-select
    if (torneoPos && categoriaPos) {
        // set inicial
        setOpcionesCategoria(categoriaPos, torneoPos.value);
        torneoPos.addEventListener('change', () => {
            setOpcionesCategoria(categoriaPos, torneoPos.value);
            // disparar cambio para que panel-posiciones.js refresque la tabla
            categoriaPos.dispatchEvent(new Event('change'));
        });
    }
    if (torneoForm) {
        // Crear el contenedor de mensajes si no existe
        let msgContainer = document.getElementById('msg-seleccion-torneo');
        if (!msgContainer) {
            msgContainer = document.createElement('div');
            msgContainer.id = 'msg-seleccion-torneo';
            torneoForm.parentNode.insertBefore(msgContainer, torneoForm.nextSibling);
        }
        torneoForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const data = {
                torneo: torneoForm['torneo'].value,
                division: torneoForm['division'].value,
                fecha: torneoForm['fecha'].value
            };
            try {
                const response = await fetch('/torneo/seleccion', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    msgContainer.textContent = 'Selección guardada correctamente.';
                    msgContainer.style.color = '#2e7d32';
                    msgContainer.style.fontWeight = 'bold';
                    msgContainer.style.marginTop = '10px';
                    setTimeout(() => { msgContainer.textContent = ''; }, 3000);
                    // Refrescar tabla de posiciones con los selects de la sección inferior si existen
                    const posForm = document.getElementById('posiciones-form');
                    if (posForm) {
                        // Alinear selects inferiores a lo elegido arriba
                        const posTorneo = document.getElementById('pos-torneo-select');
                        const posCat = document.getElementById('pos-division-select');
                        const topTorneo = document.getElementById('torneo-select');
                        const topCat = document.getElementById('division-select');
                        if (posTorneo && topTorneo) posTorneo.value = topTorneo.value;
                        if (posCat && topCat) {
                            // actualizar opciones segun torneo
                            setOpcionesCategoria(posCat, (posTorneo && posTorneo.value) || (topTorneo && topTorneo.value));
                            posCat.value = topCat.value;
                        }
                        // Disparar cambio para que panel-posiciones.js renderice
                        posForm.dispatchEvent(new Event('change'));
                        if (posTorneo) posTorneo.dispatchEvent(new Event('change'));
                    }
                } else {
                    msgContainer.textContent = 'Error al guardar la selección.';
                    msgContainer.style.color = '#d32f2f';
                    msgContainer.style.fontWeight = 'bold';
                    msgContainer.style.marginTop = '10px';
                    setTimeout(() => { msgContainer.textContent = ''; }, 3000);
                }
            } catch (err) {
                msgContainer.textContent = 'Error de conexión con el servidor.';
                msgContainer.style.color = '#d32f2f';
                msgContainer.style.fontWeight = 'bold';
                msgContainer.style.marginTop = '10px';
                setTimeout(() => { msgContainer.textContent = ''; }, 3000);
            }
        });
    }
});
