// resultados.js
// Muestra tabla de posiciones y últimos resultados desde JSON estático
const resultadosUrl = window.RESULTADOS_JSON_URL || '/static/data/resultados.json';
fetch(resultadosUrl)
  .then(response => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then(data => {
    const tabla = document.getElementById('tabla-posiciones');
    if(tabla){
      tabla.innerHTML = data.posiciones.map(e => `<tr><td>${e.equipo}</td><td>${e.puntos}</td></tr>`).join('');
    }
    const ultimos = document.getElementById('ultimos-resultados');
    if(ultimos){
      ultimos.innerHTML = data.ultimos.map(r => `<li>${r.fecha} - ${r.local} ${r.golesLocal} : ${r.golesVisita} ${r.visita}</li>`).join('');
    }
  })
  .catch(err => {
    console.error('Error cargando resultados.json:', err);
  });
