// CSRF helper: adds X-CSRFToken header and injects hidden inputs in forms
(function () {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  const CSRF_COOKIE_NAME = 'XSRF-TOKEN';
  const CSRF_HEADER_NAME = 'X-CSRFToken';

  function isUnsafeMethod(method) {
    return ['POST', 'PUT', 'PATCH', 'DELETE'].includes(String(method || 'GET').toUpperCase());
  }

  // Patch window.fetch to add header on unsafe methods
  const origFetch = window.fetch;
  window.fetch = function (input, init) {
    const opts = init || {};
    const method = (opts.method || (typeof input === 'object' && input.method) || 'GET').toUpperCase();
    if (isUnsafeMethod(method)) {
      const token = getCookie(CSRF_COOKIE_NAME);
      if (token) {
        opts.headers = new Headers(opts.headers || {});
        if (!opts.headers.has(CSRF_HEADER_NAME)) {
          opts.headers.set(CSRF_HEADER_NAME, token);
        }
      }
    }
    return origFetch.call(this, input, opts);
  };

  // Inject hidden input into forms that don't have csrf_token
  function injectIntoForms() {
    try {
      const token = getCookie(CSRF_COOKIE_NAME);
      if (!token) return;
      const forms = document.querySelectorAll('form');
      forms.forEach((form) => {
        const method = (form.getAttribute('method') || 'GET').toUpperCase();
        if (!isUnsafeMethod(method)) return;
        if (form.querySelector('input[name="csrf_token"]')) return;
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'csrf_token';
        input.value = token;
        form.appendChild(input);
      });
    } catch (e) {
      // ignore
    }
  }

  document.addEventListener('DOMContentLoaded', injectIntoForms);
})();
