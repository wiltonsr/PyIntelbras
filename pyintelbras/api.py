import logging
import requests
import re

from requests.auth import HTTPDigestAuth
from urllib.parse import urlencode, urlparse, parse_qsl, ParseResult
from .exceptions import IntelbrasAPIException

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class IntelbrasAPI:
    def __init__(
        self, server: str = 'http://localhost',
        auth: HTTPDigestAuth = None,
        verify_ssl: bool = False
    ) -> None:
        if not server.startswith('http'):
            server = 'http://' + server

        self.server = server.rstrip('/')
        self.auth = auth
        self.verify_ssl = verify_ssl

        logger.info("API Server Endpoint: %s", self.server)

    def login(
            self,
            user: str = "",
            password: str = "") -> None:
        if not user or not password:
            raise IntelbrasAPIException('Empty user or password')
        self.auth = HTTPDigestAuth(user, password)

    def do_request(
        self, method: str, path: str, params: dict,
        extra_path: str = '', headers: dict = {}, body: dict = None
    ):
        res = self._parse_api_url(
            path=path, params=params, extra_path=extra_path
        )

        url = res.geturl()

        logger.debug(f'Requesting {method} to URL {url}')

        extra_headers = {
            "User-Agent": "python/pyintelbras",
            "Cache-Control": "no-cache",
        }

        extra_headers.update(headers)

        return requests.request(
            method=method, url=url,
            auth=self.auth, verify=self.verify_ssl,
            headers=extra_headers, json=body
        )

    def _parse_api_url(
        self, path: str, params: dict, extra_path: str = ''
    ) -> ParseResult:
        url_parts = urlparse(self.server)

        query = dict(parse_qsl(url_parts.params))
        query.update(params)

        if extra_path != '' and not extra_path.startswith('/'):
            extra_path = f"/{extra_path}"

        url_path = (
            f"{url_parts.path}"  # in case of proxy context path
            f"/cgi-bin/"  # requirement of Intelbras API
            f"{path.replace('.', '/')}"  # replacing dots with slashes
            f"{extra_path}"  # add extra path
            f".cgi"  # requirement of Intelbras API
        )

        return ParseResult(
            scheme=url_parts.scheme, netloc=url_parts.netloc,
            path=url_path, params=url_parts.params,
            query=urlencode(params), fragment=url_parts.fragment
        )

    def _method(self, attr: str) -> "IntelbrasAPIMethod":
        """Dynamically create a method (ie: get)"""
        return IntelbrasAPIMethod([attr], self)

    def __getattr__(self, attr: str) -> "IntelbrasAPIMethod":
        return self._method(attr)


class IntelbrasAPIMethod:
    def __init__(self, methods: dict = None, parent: IntelbrasAPI = None):
        self.methods = methods or []
        self.parent = parent

    def __getattr__(self, name):
        return IntelbrasAPIMethod(self.methods + [name], self.parent)

    def __call__(
        self, extra_path: str = '',
        headers: dict = {}, body: dict = None,
        *args, **kwargs
    ):
        method_chain = ".".join(self.methods)
        logger.debug(
            f"Call method '{method_chain}' with arguments: "
            f"{args} and {kwargs}"
        )

        method = method_chain.split('.')[-1].upper()
        if method != 'GET' and method != 'POST':
            method = 'GET'
            path = method_chain
        else:
            pattern = re.compile(r'.(get|post)$', re.IGNORECASE)
            path = pattern.sub('', method_chain)

        return self.parent.do_request(
            method=method, path=path, params=kwargs,
            extra_path=extra_path.strip(), headers=headers, body=body
        )
