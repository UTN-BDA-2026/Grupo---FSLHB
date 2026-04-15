// calendario.js
// Calendario interactivo: filtra partidos por equipo
fetch('data/calendario.json')
  .then(response => response.json())
  .then(partidos => {
    const filtro = document.getElementById('filtro-equipo');
    const lista = document.getElementById('lista-partidos');
    if(filtro && lista){
      filtro.addEventListener('change', () => mostrarPartidos(filtro.value));
      function mostrarPartidos(equipo){
        lista.innerHTML = partidos.filter(p => equipo === 'todos' || p.equipo === equipo)
          .map(p => `<li>${p.fecha} - ${p.equipo} vs. ${p.rival}</li>`).join('');
      }
      mostrarPartidos('todos');
    }
  });
