// clubes-slider.js
// Muestra un slider de logos de clubes en la portada
fetch('/static/data/clubes.json')
  .then(response => response.json())
  .then(clubes => {
    const container = document.querySelector('.clubes-slider-card');
    if (!container) return;
    container.innerHTML = `
      <h2>EQUIPOS</h2>
      <div class="clubes-slider-list" style="display:flex;flex-direction:row;flex-wrap:nowrap;gap:2rem;justify-content:flex-start;align-items:center;overflow-x:auto;padding:1rem 0;">
        ${clubes.map(club => `
          <div class="club-card" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.5rem;min-width:120px;max-width:140px;background:#fff;border-radius:12px;box-shadow:0 1px 6px rgba(0,0,0,0.08);padding:0.5rem;">
              <img src="/static/${club.logo}" alt="${club.nombre}" style="height:${club.nombre === 'Banco Municipal' ? '100px' : club.nombre === 'Xeneizes' ? '80px' : '70px'};width:auto;object-fit:contain;border-radius:12px;background:#fff;">
            <span style="font-size:1rem;font-weight:500;text-align:center;">${club.nombre}</span>
          </div>
        `).join('')}
      </div>
    `;
  });
