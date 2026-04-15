// galeria-home.js
// Carga galería de la portada desde galeria.json
fetch('data/galeria.json')
  .then(res => res.json())
  .then(galerias => {
    const cont = document.querySelector('.ultimas-galerias-mini-card');
    if(!cont) return;
    cont.innerHTML = `<h3>Últimas Galerías</h3><div class="galerias-home-list"></div>`;
    const list = cont.querySelector('.galerias-home-list');
    list.style.display = 'flex';
    list.style.gap = '18px';
    list.style.overflowX = 'auto';
    list.style.scrollSnapType = 'x mandatory';
    list.style.paddingBottom = '0.5rem';
    list.style.flexWrap = 'nowrap';
    galerias.forEach(gal => {
      const item = document.createElement('a');
      item.href = gal.enlace;
      item.className = 'galeria-mini-item';
      item.style.display = 'flex';
      item.style.flexDirection = 'column';
      item.style.alignItems = 'center';
      item.style.width = '140px';
      item.style.textDecoration = 'none';
      item.style.color = '#1976d2';
      item.style.scrollSnapAlign = 'start';
      item.style.position = 'relative';
      item.style.transition = 'transform 0.18s, box-shadow 0.18s';
      // Tooltip accesible (paso 8)
      item.title = `${gal.titulo}${gal.fecha ? ' - ' + gal.fecha : ''}${gal.cantidad ? ' - ' + gal.cantidad + ' fotos' : ''}`;
      item.innerHTML = `
        <div class="galeria-img-wrap" style="position:relative;width:100%;max-width:120px;">
          <img src="${gal.imagen}" alt="${gal.titulo}" loading="lazy" style="width:100%;height:80px;object-fit:cover;border-radius:8px;box-shadow:0 2px 8px rgba(25,118,210,0.10);margin-bottom:6px;transition:filter 0.18s;">
          <button class="ver-galeria-btn" tabindex="-1" style="display:none;position:absolute;bottom:8px;left:50%;transform:translateX(-50%);background:#1976d2;color:#fff;border:none;border-radius:6px;padding:2px 10px;font-size:0.93rem;box-shadow:0 2px 8px rgba(25,118,210,0.10);cursor:pointer;">Ver galería</button>
          <div class="galeria-social" style="position:absolute;top:6px;right:6px;display:flex;gap:4px;z-index:2;">
            <a href="https://wa.me/?text=${encodeURIComponent('Mirá la galería: ' + gal.titulo + ' ' + window.location.origin + '/' + gal.enlace)}" target="_blank" title="Compartir en WhatsApp" tabindex="-1" style="background:#25d366;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;"><img src="assets/img/whatsapp.svg" alt="WhatsApp" style="width:14px;height:14px;"></a>
            <a href="https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.origin + '/' + gal.enlace)}" target="_blank" title="Compartir en Facebook" tabindex="-1" style="background:#1877f2;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;"><img src="assets/img/facebook.svg" alt="Facebook" style="width:14px;height:14px;"></a>
          </div>
          <div class="galeria-likes" style="position:absolute;top:6px;left:6px;background:rgba(255,255,255,0.85);border-radius:12px;padding:1px 7px;font-size:0.92rem;color:#d32f2f;display:flex;align-items:center;gap:3px;">
            <span class="like-count">${gal.likes || Math.floor(Math.random()*30+1)}</span> <span aria-label="Me gusta" title="Me gusta">❤</span>
          </div>
        </div>
        <span style="font-size:0.98rem;font-weight:bold;text-align:center;">${gal.titulo}</span>
        <span style="font-size:0.92rem;text-align:center;">${gal.descripcion}</span>
        ${gal.fecha ? `<span style='font-size:0.85rem;color:#555;margin-top:2px;'>${gal.fecha}</span>` : ''}
        ${gal.cantidad ? `<span style='font-size:0.85rem;color:#888;'>${gal.cantidad} fotos</span>` : ''}
      `;
      // Like (paso 10, simulado en localStorage)
      const likeDiv = document.createElement('div');
      // Efecto hover para mostrar botón y resaltar imagen
      item.addEventListener('mouseenter', () => {
        const img = item.querySelector('img');
        const btn = item.querySelector('.ver-galeria-btn');
        if(img) img.style.filter = 'brightness(0.85)';
        if(btn) btn.style.display = 'block';
        item.style.transform = 'scale(1.04)';
        item.style.boxShadow = '0 4px 16px 0 rgba(25,118,210,0.18)';
      });
      item.addEventListener('mouseleave', () => {
        const img = item.querySelector('img');
        const btn = item.querySelector('.ver-galeria-btn');
        if(img) img.style.filter = '';
        if(btn) btn.style.display = 'none';
        item.style.transform = '';
        item.style.boxShadow = '';
      });
      // Accesibilidad: mostrar botón con tab
      item.addEventListener('focusin', () => {
        const btn = item.querySelector('.ver-galeria-btn');
        if(btn) btn.style.display = 'block';
      });
      item.addEventListener('focusout', () => {
        const btn = item.querySelector('.ver-galeria-btn');
        if(btn) btn.style.display = 'none';
      });
      // Click en botón también navega
      item.querySelector('.ver-galeria-btn').addEventListener('click', e => {
        e.preventDefault();
        window.location = gal.enlace;
      });
      // Like click (paso 10)
      const likeBtn = item.querySelector('.galeria-likes');
      if(likeBtn) {
        likeBtn.style.cursor = 'pointer';
        likeBtn.addEventListener('click', e => {
          e.preventDefault();
          e.stopPropagation();
          const key = 'galeria-like-' + gal.titulo.replace(/\s+/g,'-').toLowerCase();
          let count = parseInt(localStorage.getItem(key) || '0', 10);
          if(count < 1) {
            count++;
            localStorage.setItem(key, count);
            likeBtn.querySelector('.like-count').textContent = count;
            likeBtn.style.color = '#1976d2';
          }
        });
        // Mostrar likes guardados
        const key = 'galeria-like-' + gal.titulo.replace(/\s+/g,'-').toLowerCase();
        let count = parseInt(localStorage.getItem(key) || '');
        if(count) likeBtn.querySelector('.like-count').textContent = count;
      }
      list.appendChild(item);
    });
    // Botón "Ver todas las galerías"
    const verTodas = document.createElement('a');
    verTodas.href = 'pages/galeria.html';
    verTodas.className = 'ver-todas-galerias-btn';
    verTodas.textContent = 'Ver todas las galerías →';
    verTodas.style.display = 'inline-block';
    verTodas.style.margin = '1rem auto 0 auto';
    verTodas.style.background = 'linear-gradient(90deg,#1976d2 60%,#006400 100%)';
    verTodas.style.color = '#fff';
    verTodas.style.borderRadius = '8px';
    verTodas.style.padding = '0.6rem 1.5rem';
    verTodas.style.fontWeight = 'bold';
    verTodas.style.textAlign = 'center';
    verTodas.style.textDecoration = 'none';
    verTodas.style.boxShadow = '0 2px 8px 0 rgba(25,118,210,0.10)';
    verTodas.style.fontSize = '1.08rem';
    verTodas.style.transition = 'background 0.2s, box-shadow 0.2s';
    verTodas.addEventListener('mouseenter',()=>{
      verTodas.style.background = 'linear-gradient(90deg,#006400 60%,#1976d2 100%)';
      verTodas.style.boxShadow = '0 4px 16px 0 rgba(25,118,210,0.18)';
    });
    verTodas.addEventListener('mouseleave',()=>{
      verTodas.style.background = 'linear-gradient(90deg,#1976d2 60%,#006400 100%)';
      verTodas.style.boxShadow = '0 2px 8px 0 rgba(25,118,210,0.10)';
    });
    cont.appendChild(verTodas);
    // Animación fade-in
    Array.from(list.children).forEach((el,i)=>{
      el.style.opacity = 0;
      el.style.transform += ' translateY(16px)';
      setTimeout(()=>{
        el.style.transition = 'opacity 0.5s, transform 0.5s';
        el.style.opacity = 1;
        el.style.transform = el.style.transform.replace(' translateY(16px)','');
      }, 80*i+100);
    });
  });
