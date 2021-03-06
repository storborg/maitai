import logging

from webob import Request
from webob.exc import HTTPTemporaryRedirect

log = logging.getLogger(__name__)


class RenameCookieMiddleware(object):
    """
    This middleware looks for a cookie named ``from_key`` in the request. If
    found, it issues an immediate 302 response that renames the cookie to
    ``to_key``. Other requests are directly passed through.
    """
    def __init__(self, app, from_key, to_key, **kwargs):
        self.app = app
        self.from_key = from_key
        self.to_key = to_key
        self.cookie_kwargs = kwargs

    def __call__(self, environ, start_response):
        req = Request(environ)

        val = req.cookies.get(self.from_key)
        if val:
            log.info("Renaming %s=%s to %s on client IP %s",
                     self.from_key, val, self.to_key, req.remote_addr)
            resp = HTTPTemporaryRedirect(location=req.url)
            resp.delete_cookie(self.from_key)
            resp.set_cookie(self.to_key, val, **self.cookie_kwargs)
        else:
            resp = req.get_response(self.app)

        return resp(environ, start_response)
