// galeria.js - versión tarjeta única + modal con thumbnails y navegación
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('modal-galeria');
  const closeBtn = modal?.querySelector('.gal-close');
  const viewImg = document.getElementById('galeria-view');
  const thumbsContainer = document.getElementById('galeria-thumbs');
  const prevBtn = modal?.querySelector('.gal-nav-prev');
  const nextBtn = modal?.querySelector('.gal-nav-next');
  let galeriaData = [];
  let currentGal = 0;
  let images = [];
  let currentIndex = 0;

  // Recoge datos de cada galería desde el DOM
  document.querySelectorAll('.galeria-card').forEach((card, galIdx) => {
    let imgs = [];
    const dataImgs = card.getAttribute('data-imagenes');
    if (dataImgs) {
      try { imgs = JSON.parse(dataImgs); } catch(e) { imgs = []; }
    }
    galeriaData.push({ card, imgs });
    card.addEventListener('click', () => openModal(galIdx, 0));
  });

  const openModal = (galIdx=0, imgIdx=0) => {
    if(!modal) return;
    currentGal = galIdx;
    images = galeriaData[galIdx]?.imgs || [];
    currentIndex = imgIdx;
    buildThumbs();
    updateMainView();
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
  };

  const closeModal = () => {
    if(!modal) return;
    modal.style.display = 'none';
    document.body.style.overflow = '';
  };

  const updateMainView = () => {
    if(!viewImg || !images.length) return;
    const img = images[currentIndex];
    viewImg.src = img.full;
    highlightThumb();
  };

  const highlightThumb = () => {
    if(!thumbsContainer) return;
    thumbsContainer.querySelectorAll('img').forEach((t,i)=>{
      t.classList.toggle('active', i===currentIndex);
    });
  };

  const buildThumbs = () => {
    if(!thumbsContainer) return;
    thumbsContainer.innerHTML = images.map((img,i)=>`<img src="${img.thumbnail}" data-index="${i}" alt="thumb-${i}" loading="lazy" decoding="async">`).join('');
    thumbsContainer.querySelectorAll('img').forEach(t=>{
      t.addEventListener('click', ()=>{
        currentIndex = parseInt(t.getAttribute('data-index'),10);
        updateMainView();
      });
    });
  };

  const navigate = (delta) => {
    if(!images.length) return;
    currentIndex = (currentIndex + delta + images.length) % images.length;
    updateMainView();
  };

  prevBtn?.addEventListener('click', ()=> navigate(-1));
  nextBtn?.addEventListener('click', ()=> navigate(1));
  closeBtn?.addEventListener('click', closeModal);
  modal?.addEventListener('click', (e)=>{ if(e.target === modal) closeModal(); });
  document.addEventListener('keyup', (e)=>{ if(e.key==='Escape') closeModal(); });
});
