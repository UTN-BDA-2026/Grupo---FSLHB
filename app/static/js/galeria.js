// galeria.js
// Galería interactiva: muestra imagen ampliada al hacer clic
const imagenes = document.querySelectorAll('.galeria-img');
const modal = document.getElementById('modal-img');
const modalImg = document.getElementById('img-ampliada');
if(imagenes && modal && modalImg){
  imagenes.forEach(img => {
    img.addEventListener('click', () => {
      modal.style.display = 'block';
      modalImg.src = img.src;
    });
  });
  modal.addEventListener('click', () => {
    modal.style.display = 'none';
  });
}
