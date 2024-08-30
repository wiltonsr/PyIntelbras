import logging
import requests

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

        logger.info("API Server Endpoint: %s", self.server)

    def login(
            self,
            user: str = "",
            password: str = "") -> None:
        if not user or not password:
            raise IntelbrasAPIException('Empty user or password')
        self.auth = HTTPDigestAuth(user, password)

    def do_request(
        self, method: str, path: str, params: dict, extra_path: str = ''
    ):
        url_parts = urlparse(self.server)

        query = dict(parse_qsl(url_parts.params))
        query.update(params)

        url_path = (
            f"{url_parts.path}"  # in case of proxy context path
            f"/cgi-bin/"  # requirement of Intelbras API
            f"{path.replace('.', '/')}"  # replacing dots with slashes
            f"{extra_path}"  # add extra path
            f".cgi"  # requirement of Intelbras API
        )

        res = ParseResult(
            scheme=url_parts.scheme, netloc=url_parts.netloc,
            path=url_path, params=url_parts.params,
            query=urlencode(params), fragment=url_parts.fragment
        )

        url = res.geturl()

        logger.debug(f'Requesting to URL {url}')

        return requests.request(
            method=method, url=url, auth=self.auth, verify=self.verify_ssl
        )

    def __getattr__(self, name):
        def method(extra_path: str = '', *args, **kwargs):
            logger.debug(
                f"Call method '{name}' with arguments: {args} and {kwargs}"
            )
            return self.do_request('GET', name, kwargs, extra_path)
        return method
