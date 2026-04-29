"""Hooks/handlers de Flask (headers, errores, HTTPS, CSRF cookie)."""

import logging
import os

from flask import redirect, render_template, request
from flask_wtf.csrf import generate_csrf


def register_error_handlers(app) -> None:
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500


def register_security_headers(app) -> None:
    @app.after_request
    def set_security_headers(resp):
        resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
        resp.headers.setdefault('X-Frame-Options', 'DENY')
        resp.headers.setdefault('Referrer-Policy', 'no-referrer-when-downgrade')
        resp.headers.setdefault(
            'Content-Security-Policy',
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://www.instagram.com; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https://res.cloudinary.com; "
            "font-src 'self' https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "frame-src https://www.google.com https://www.facebook.com https://www.instagram.com; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';",
        )

        try:
            if request.is_secure or app.config.get('SESSION_COOKIE_SECURE'):
                resp.headers.setdefault(
                    'Strict-Transport-Security', 'max-age=31536000; includeSubDomains'
                )
        except Exception:
            pass

        try:
            if request.path.startswith('/static/'):
                resp.headers.setdefault(
                    'Cache-Control', 'public, max-age=2592000, immutable'
                )
        except Exception:
            pass

        try:
            if 'csrf' in app.extensions:
                token = generate_csrf()
                resp.set_cookie(
                    'XSRF-TOKEN',
                    token,
                    secure=app.config.get('SESSION_COOKIE_SECURE', True),
                    httponly=False,
                    samesite=app.config.get('SESSION_COOKIE_SAMESITE', 'Lax'),
                )
        except Exception as e:
            logging.getLogger(__name__).debug(f'No se pudo generar cookie CSRF: {e}')

        return resp


def register_https_enforcement(app) -> None:
    @app.before_request
    def enforce_https():
        force_https = os.getenv('FORCE_HTTPS', 'true').lower() == 'true'
        if not force_https or app.debug:
            return
        if request.is_secure:
            return
        xf_proto = request.headers.get('X-Forwarded-Proto', '')
        if 'https' in xf_proto:
            return
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
