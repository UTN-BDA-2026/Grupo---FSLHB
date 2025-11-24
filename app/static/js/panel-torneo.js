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

    // Top form: torneo-select controla division-select (categoría)
    const torneoTop = document.getElementById('torneo-select');
    const categoriaTop = document.getElementById('division-select');
    if (torneoTop && categoriaTop) {
        // set inicial
        setOpcionesCategoria(categoriaTop, torneoTop.value);
        torneoTop.addEventListener('change', () => {
            setOpcionesCategoria(categoriaTop, torneoTop.value);
        });
    }

    // Tabla posiciones form: pos-torneo-select controla pos-division-select
    const torneoPos = document.getElementById('pos-torneo-select');
    const categoriaPos = document.getElementById('pos-division-select');
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
