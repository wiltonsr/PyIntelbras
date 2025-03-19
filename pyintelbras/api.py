import logging
import requests
import re
from typing import Union, Tuple, Dict, List
from requests.auth import HTTPDigestAuth
from requests import Response
from urllib.parse import urlencode, urlparse, parse_qsl, ParseResult
from .exceptions import IntelbrasAPIException
from .helpers import parse_response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class IntelbrasAPI:
    def __init__(
        self, server: str = 'http://localhost',
        user: str = '',
        password: str = '',
        auth: HTTPDigestAuth = None,
        verify_ssl: bool = False,
    ) -> None:
        self.server = server if server.startswith(
            'http') else f'http://{server}'
        self.server = self.server.rstrip('/')
        self.auth = auth
        self.user = self.auth.username if auth else user
        self.password = self.auth.password if auth else password
        self.verify_ssl = verify_ssl
        self.last_request_url = None

        if user and password and not auth:
            self.login(user, password)

        logger.info(f"API Server Endpoint: {self.server}")

    def login(self, user: str, password: str) -> None:
        if not user or not password:
            raise IntelbrasAPIException('Empty user or password')
        self.user = user
        self.password = password
        self.auth = HTTPDigestAuth(user, password)

    @property
    def api_version(self) -> dict:
        response = self.IntervideoManager(action='getVersion', Name='CGI')
        return parse_response(response.text)

    @property
    def channels(self) -> list:
        response = self.configManager(action='getConfig', name='ChannelTitle')
        parsed_response = parse_response(response.text)
        return parsed_response.get('table', {}).get('ChannelTitle', [])

    def rtsp_url(self, protocol: str = 'rtsp', port: int = 554, channel: int = 1, subtype: int = 0) -> str:
        url_parts = urlparse(self.server)
        query = dict(parse_qsl(url_parts.query))
        query.update({'channel': channel, 'subtype': subtype})
        path = f'{url_parts.path}/cam/realmonitor'
        netloc = f'{url_parts.hostname}:{port}'
        if self.user and self.password:
            netloc = f'{self.user}:{self.password}@{netloc}'
        return ParseResult(
            scheme=protocol, netloc=netloc,
            path=path, params=url_parts.params,
            query=urlencode(query), fragment=url_parts.fragment
        ).geturl()

    def find_media_files(self, params: dict) -> dict:
        # Helper method to docs section 4.10.5 Find Media Files
        def execute_action(action: str, **kwargs) -> dict:
            response = self.mediaFileFind(action=action, **kwargs)
            return parse_response(response.text)

        # Step 1 - Create a media files finder.
        create_response = execute_action('factory.create')
        object_number = create_response.get('result')

        if not object_number:
            raise IntelbrasAPIException("Failed to create media file finder")

        # Step 2 - Start to find media files satisfied the conditions with the finder.
        params.update({'action': 'findFile', 'object': object_number})
        execute_action(**params)

        # Step 3 - Get the media file information found by the finder.
        find_next_response = execute_action(
            'findNextFile', object=object_number, count=100)
        found = find_next_response.get('found')
        logger.debug(f"Found {found} media files.")

        # Step 4 - Close the finder.
        execute_action('close', object=object_number)

        # Step 5 - Destroy the finder.
        execute_action('destroy', object=object_number)

        return find_next_response

    def do_request(
        self, method: str, path: str, params: dict,
        timeout: Union[float, Tuple[float, float]] = None,
        extra_path: str = '', headers: dict = {}, body: dict = None
    ) -> Response:
        url = self._parse_api_url(
            path=path, params=params, extra_path=extra_path).geturl()
        logger.debug(f'Requesting {method} to URL {url}')
        self.last_request_url = url

        extra_headers = {
            "User-Agent": "python/pyintelbras",
            "Cache-Control": "no-cache",
        }
        extra_headers.update(headers)

        response = requests.request(
            method=method, url=url, timeout=timeout,
            auth=self.auth, verify=self.verify_ssl,
            headers=extra_headers, json=body
        )

        logger.debug(
            f'Request status_code {response.status_code} - {response.reason}')
        return response

    def _parse_api_url(self, path: str, params: dict, extra_path: str = '') -> ParseResult:
        url_parts = urlparse(self.server)
        query = dict(parse_qsl(url_parts.query))
        query.update(params)

        if extra_path and not extra_path.startswith('/'):
            extra_path = f"/{extra_path}"

        url_path = (
            f"{url_parts.path}"          # in case of proxy context path
            f"/cgi-bin/"                 # requirement of Intelbras API
            f"{path.replace('.', '/')}"  # replacing dots with slashes
            f"{extra_path}"              # needed to download media file with filename # noqa: E501
            f".cgi"                      # requirement of Intelbras API
        )

        return ParseResult(
            scheme=url_parts.scheme, netloc=url_parts.netloc,
            path=url_path, params=url_parts.params,
            query=urlencode(query), fragment=url_parts.fragment
        )

    def _method(self, attr: str) -> "IntelbrasAPIMethod":
        return IntelbrasAPIMethod([attr], self)

    def __getattr__(self, attr: str) -> "IntelbrasAPIMethod":
        return self._method(attr)


class IntelbrasAPIMethod:
    def __init__(self, methods: List[str] = None, parent: IntelbrasAPI = None):
        self.methods = methods or []
        self.parent = parent

    def __getattr__(self, name: str) -> "IntelbrasAPIMethod":
        return IntelbrasAPIMethod(self.methods + [name], self.parent)

    def __call__(
        self, extra_path: str = '',
        headers: dict = {}, body: dict = None,
        timeout: Union[float, Tuple[float, float]] = None,
        *args, **kwargs
    ) -> Response:
        method_chain = ".".join(self.methods)
        logger.debug(
            f"Call method '{method_chain}' with arguments: {args} and {kwargs}")

        method = method_chain.split('.')[-1].upper()
        if method not in {'GET', 'POST'}:
            method = 'GET'
            path = method_chain
        else:
            path = re.sub(r'.(get|post)$', '',
                          method_chain, flags=re.IGNORECASE)

        return self.parent.do_request(
            method=method, path=path, params=kwargs, timeout=timeout,
            extra_path=extra_path.strip(), headers=headers, body=body
        )
