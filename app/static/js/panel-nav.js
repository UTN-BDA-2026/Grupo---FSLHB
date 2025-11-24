// Reusable nav dropdown logic for all pages
(function(){
  function textClub(){
    try{
      const nombre = localStorage.getItem('nombreClub');
      const span = document.getElementById('nombre-club-nav');
      if (span) span.textContent = (nombre && nombre.trim() !== '') ? nombre : 'Mesa de Control';
    }catch{}
  }
  function resetInline(menu){ if(!menu) return; menu.style.left=''; menu.style.top=''; menu.style.transform=''; }
  function positionBelow(trigger, menu){
    if (!trigger || !menu) return;
    if (window.innerWidth > 768) return; // desktop: dejar CSS
    const r = trigger.getBoundingClientRect();
    // mostrar para medir
    if (!menu.classList.contains('show')) menu.classList.add('show');
    const margin = 8;
    const naturalWidth = menu.offsetWidth || 0; // width real (max-content)
    const w = Math.min(Math.max(naturalWidth, 0), window.innerWidth - 2*margin);
    let left = r.left + (r.width - w)/2;
    left = Math.max(margin, Math.min(left, window.innerWidth - w - margin));
    const top = r.bottom + 6;
    menu.style.left = left + 'px';
    menu.style.top = top + 'px';
    menu.style.transform = 'none';
  }
  function setup(){
    textClub();
    const adminLink = document.getElementById('admin-plantel-link');
    const adminMenu = document.getElementById('admin-plantel-dropdown');
    const paramLink = document.getElementById('param-club-link');
    const paramMenu = document.getElementById('param-club-dropdown');

    function closeAll(){
      if (adminMenu){ adminMenu.classList.remove('show'); resetInline(adminMenu); }
      if (paramMenu){ paramMenu.classList.remove('show'); resetInline(paramMenu); }
    }
    function toggle(link, menu){
      if (!link || !menu) return;
      const open = menu.classList.contains('show');
      closeAll();
      if (!open){
        menu.classList.add('show');
        positionBelow(link, menu);
      }
    }
    if (adminLink && adminMenu){
      adminLink.addEventListener('click', function(e){ e.preventDefault(); toggle(adminLink, adminMenu); });
    }
    if (paramLink && paramMenu){
      paramLink.addEventListener('click', function(e){ e.preventDefault(); toggle(paramLink, paramMenu); });
    }
    document.addEventListener('click', function(e){
      const inside = (adminLink && (adminLink.contains(e.target) || (adminMenu && adminMenu.contains(e.target)))) ||
                     (paramLink && (paramLink.contains(e.target) || (paramMenu && paramMenu.contains(e.target))));
      if (!inside) closeAll();
    });
    window.addEventListener('resize', function(){
      // si alguno está abierto en móvil, re-posicionar
      if (window.innerWidth <= 768){
        if (adminMenu && adminMenu.classList.contains('show')) positionBelow(adminLink, adminMenu);
        if (paramMenu && paramMenu.classList.contains('show')) positionBelow(paramLink, paramMenu);
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup); else setup();
})();
