// noticias.js
// Carga noticias desde un archivo JSON y las muestra en la portada y sección de noticias
let noticiasData = [];
let pageIndex = 0; // índice de página (no de tarjeta)

function renderNoticiasSlider() {
  const contenedor = document.getElementById('noticias-destacadas');
  if (!contenedor) return;
  contenedor.innerHTML = noticiasData.map((noticia) => {
  const noticiaHref = `/noticias?noticia=${noticia.id}`;
    return `
      <a class="noticia-slider" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-decoration:none;color:inherit;cursor:pointer;" href="${noticiaHref}">
        <div style="width:100%;display:flex;justify-content:center;align-items:center;">
          <img src="/static/assets/img/${noticia.imagen}" alt="${noticia.titulo}" style="width:100%;max-width:220px;height:140px;object-fit:cover;border-radius:10px 10px 0 0;margin-bottom:0.7rem;box-shadow:0 2px 8px rgba(25,118,210,0.10);display:block;">
        </div>
        <h3 style="font-size:1.15rem;margin:0 0 0.5rem 0;color:#1976d2;">${noticia.titulo}</h3>
        <p style="font-size:1rem;margin:0 0 0.7rem 0;color:#333;">${noticia.resumen}</p>
        <span style="display:inline-block;font-size:0.95rem;color:#1976d2;font-weight:bold;">Ver más <i class='fas fa-arrow-right'></i></span>
      </a>
    `;
  }).join('');

  // Ajuste de ancho para desktop: limitar track a exactamente 3 tarjetas (o menos si hay menos datos)
  requestAnimationFrame(() => {
    if (window.innerWidth >= 900) {
      const track = document.querySelector('.slider-track');
      if (track) {
        const cards = track.querySelectorAll('.noticia-slider');
        if (cards.length) {
          const visible = Math.min(cards.length, 3);
          const gap = parseFloat(getComputedStyle(track).gap || '0');
          const cardWidth = cards[0].getBoundingClientRect().width;
          const total = visible * cardWidth + (visible - 1) * gap;
          track.style.maxWidth = total + 'px';
          track.style.margin = '0 auto';
        }
      }
    }
  });
}

// Usar ruta relativa para evitar contenido mixto y funcionar detrás de proxy
const API_BASE = '/api/noticias/?limit=6';
fetch(API_BASE)
  .then(response => response.json())
  .then(noticias => {
    // Ya pedimos limit=6 al backend, tomamos tal cual
    noticiasData = [...noticias];
    renderNoticiasSlider();
    const track = document.querySelector('.slider-track');
    const prev = document.getElementById('slider-prev');
    const next = document.getElementById('slider-next');

    if (track && prev && next) {
      const getItemsPerPage = () => (window.innerWidth >= 900 ? 3 : 1);
      const getCardFullWidth = () => {
        const card = track.querySelector('.noticia-slider');
        if (!card) return 0;
        const cardRect = card.getBoundingClientRect();
        const gap = parseFloat(getComputedStyle(track).gap || '0') || 0;
        return cardRect.width + gap;
      };
      const cards = track.querySelectorAll('.noticia-slider');

      const updateVisibility = () => {
        const ipp = getItemsPerPage();
        if (ipp === 1) {
          cards.forEach((card, i) => {
            card.style.display = (i === pageIndex) ? 'flex' : 'none';
          });
        } else {
          cards.forEach(card => { card.style.display = 'flex'; });
        }
      };

      const scrollToPage = (p) => {
        const npp = getItemsPerPage();
        const totalPages = Math.max(1, Math.ceil(noticiasData.length / npp));
        pageIndex = (p + totalPages) % totalPages; // circular
        if (npp === 1) {
          updateVisibility();
        } else {
          const left = pageIndex * npp * getCardFullWidth();
          track.scrollTo({ left, behavior: 'smooth' });
        }
      };

      prev.onclick = () => scrollToPage(pageIndex - 1);
      next.onclick = () => scrollToPage(pageIndex + 1);

      // Reset al cambiar tamaño para mantener páginas consistentes
      window.addEventListener('resize', () => {
        updateVisibility();
        if (getItemsPerPage() > 1) {
          scrollToPage(pageIndex);
        }
      });
      window.addEventListener('resize', () => {
        // Recalcular limite de ancho al cambiar tamaño
        if (window.innerWidth >= 900) {
          const cards = track.querySelectorAll('.noticia-slider');
          if (cards.length) {
            const visible = Math.min(cards.length, 3);
            const gap = parseFloat(getComputedStyle(track).gap || '0');
            const cardWidth = cards[0].getBoundingClientRect().width;
            const total = visible * cardWidth + (visible - 1) * gap;
            track.style.maxWidth = total + 'px';
            track.style.margin = '0 auto';
          }
        } else {
          track.style.maxWidth = '';
          updateVisibility();
        }
      });
      // Inicializar visibilidad correcta para móvil
      updateVisibility();
    }
  });

const noticiasDestacadas = [
    {
        titulo: "Hockey Acción: última fecha de la fase regular",
        descripcion: "Programa de partidos confirmados para la última fecha de la fase regular del Torneo Apertura Hockey Acción.",
        imagen: "static/assets/img/hockey-accion-fase-regular.png",
        enlace: "/noticias#hockey-accion-fase-regular"
    },
    {
        titulo: "Hockey Acción: así están las posiciones",
        descripcion: "Descubre cómo están las posiciones en el Torneo Apertura Hockey Acción tras los últimos resultados.",
        imagen: "static/assets/img/Posicion.png",
        enlace: "/noticias#hockey-accion-posiciones"
    }
];
