// redes.js
// Render de botones de redes sociales (no sobrescribe si ya hay enlaces en el HTML)
const contenedor = document.getElementById('redes-sociales');
if (contenedor) {
  // Si el HTML ya trae enlaces, respetarlos y no hacer nada
  if (contenedor.querySelector('a')) {
    // Ya configurado desde la plantilla
  } else {
    // Permite configurar URLs vía data-attributes en el contenedor (opcional)
    const igUrl = contenedor.dataset.instagramUrl || 'https://www.instagram.com/deportes.sanrafael/';
    const fbUrl = contenedor.dataset.facebookUrl || 'https://www.facebook.com/mdzhockey';
    const twUrl = contenedor.dataset.twitterUrl || 'https://twitter.com/mdzhockey';

    const redes = [
      { nombre: 'Instagram', url: igUrl, icono: '<i class="fab fa-instagram"></i>' },
      { nombre: 'Facebook', url: fbUrl, icono: '<i class="fab fa-facebook"></i>' },
      { nombre: 'Twitter', url: twUrl, icono: '<i class="fab fa-twitter"></i>' }
    ];
    contenedor.innerHTML = redes.map(r => `<a href="${r.url}" target="_blank" rel="noopener noreferrer" title="${r.nombre}">${r.icono}</a>`).join(' ');
  }
}
