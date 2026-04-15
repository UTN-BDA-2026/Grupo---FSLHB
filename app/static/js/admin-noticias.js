// admin-noticias.js
// Gestión simple de noticias usando la API /api/noticias

async function cargarNoticias() {
  const contenedor = document.getElementById('lista-noticias');
  if (!contenedor) return;
  contenedor.innerHTML = '<p>Cargando noticias...</p>';
  try {
    const resp = await fetch('/api/noticias/');
    if (!resp.ok) throw new Error('Error al obtener noticias');
    const noticias = await resp.json();

    if (!Array.isArray(noticias) || noticias.length === 0) {
      contenedor.innerHTML = '<p>No hay noticias cargadas.</p>';
      return;
    }

    const html = noticias
      .map(n => `
        <div class="noticia-admin-item" data-id="${n.id}">
          <div class="noticia-admin-texto">
            <h4>${n.titulo}</h4>
            <p class="noticia-admin-fecha">${n.fecha || ''}</p>
            ${n.resumen ? `<p class="noticia-admin-resumen">${n.resumen}</p>` : ''}
          </div>
          <div class="noticia-admin-acciones">
            <button type="button" class="btn-eliminar-noticia" data-id="${n.id}">
              <i class="fas fa-trash-alt"></i> Eliminar
            </button>
          </div>
        </div>
      `)
      .join('');

    contenedor.innerHTML = html;
  } catch (err) {
    console.error(err);
    contenedor.innerHTML = '<p>Error al cargar las noticias.</p>';
  }
}

async function crearNoticiaDesdeFormulario(event) {
  event.preventDefault();
  const form = event.target;
  const msg = document.getElementById('form-noticia-msg');
  if (msg) msg.textContent = '';

  // Normalizar imagen: guardar solo el nombre de archivo si viene una ruta completa
  let imagenInput = form.imagen.value.trim();
  if (imagenInput) {
    const parts = imagenInput.split(/[\\/]/); // separa por / o \
    imagenInput = parts[parts.length - 1];
  }

  const data = {
    titulo: form.titulo.value.trim(),
    resumen: form.resumen.value.trim() || null,
    contenido: form.contenido.value.trim(),
    imagen: imagenInput || null,
    fecha: form.fecha.value || null,
  };

  if (!data.titulo || !data.contenido) {
    if (msg) msg.textContent = 'Título y contenido son obligatorios.';
    return;
  }

  try {
    const resp = await fetch('/api/noticias/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!resp.ok) throw new Error('Error al crear noticia');

    form.reset();
    if (msg) msg.textContent = 'Noticia creada correctamente.';
    cargarNoticias();
  } catch (err) {
    console.error(err);
    if (msg) msg.textContent = 'Hubo un error al guardar la noticia.';
  }
}

async function eliminarNoticia(id) {
  if (!id) return;
  if (!confirm('¿Seguro que deseas eliminar esta noticia?')) return;

  try {
    const resp = await fetch(`/api/noticias/${id}`, { method: 'DELETE' });
    if (!resp.ok) throw new Error('Error al eliminar noticia');
    cargarNoticias();
  } catch (err) {
    console.error(err);
    alert('No se pudo eliminar la noticia.');
  }
}

function inicializarEventosNoticias() {
  const form = document.getElementById('form-noticia');
  if (form) {
    form.addEventListener('submit', crearNoticiaDesdeFormulario);
  }

  const contenedor = document.getElementById('lista-noticias');
  if (contenedor) {
    contenedor.addEventListener('click', (e) => {
      const btn = e.target.closest('.btn-eliminar-noticia');
      if (btn) {
        const id = btn.getAttribute('data-id');
        eliminarNoticia(id);
      }
    });
  }
}

window.addEventListener('DOMContentLoaded', () => {
  inicializarEventosNoticias();
  cargarNoticias();
});
