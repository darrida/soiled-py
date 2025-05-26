"""Victor Smart Kill API module."""

import logging

# from httpx import URL, AsyncClient, Response, codes
import requests
from requests import Response, Session

log = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://www.victorsmartkill.com"


class InvalidCredentialsError(Exception):
    """Invalid authentication credentials."""


class VictorClient(Session):
    """An asynchronous HTTP client to Victor Smart Kill API."""

    def __init__(self, username: str, password: str, **kwargs) -> None:
        """
        Initialize VictorAsyncClient.

        :param username: User name used to access Victor API.
        :param username: Password used to access Victor API.
        :param kwargs: Arguments to pass to the httpx.AsyncClient constructor.
        """
        super().__init__(**kwargs)

        if not username:
            raise ValueError("User name is required.")

        if not password:
            raise ValueError("Password is required.")

        self.base_url = DEFAULT_BASE_URL

        self._credentials = {"password": password, "username": username}
        self._token = None

    @property
    def has_token(self) -> bool:
        """Boolean that indicates whether this session has an token or not."""
        return self._token is not None

    def fetch_token(self) -> None:
        """Fetch token and store in client."""
        self._token = None

        response = requests.post(f"{DEFAULT_BASE_URL}/api-token-auth/",
            json=self._credentials,
        )

        if response.status_code == 400:
            if response.content.find(b"credentials") != -1:
                log.debug("Credentials error: %s", str(response.content))
                raise InvalidCredentialsError(response.content)

        response.raise_for_status()

        token = response.json().get("token")
        if token:
            self._token = token
            log.info("Fetched token.")
        else:
            raise Exception("Unexpected response from token endpoind")

    def request(
        self,
        *args,
        **kwargs,
    ) -> Response:
        """Intercept all requests and add token. Fetches token if needed."""
        return self._request(True, *args, **kwargs)

    def _request(
        self, retry_unauthorized: bool, method: str, url: str, data: dict = None, headers: dict = None, **kwargs
    ) -> Response:
        if not self.has_token:
            log.info("Token is missing. Fetch token.")
            self.fetch_token()

        url = f"{DEFAULT_BASE_URL}/{url}"

        if not headers:
            request_headers = {}
        else:
            request_headers = headers.copy()

        request_headers["Authorization"] = f"Token {self._token}"

        if log.isEnabledFor(logging.DEBUG):
            log.debug("Adding token to request.")
            log.debug("Requesting url %s using method %s.", url, method)
            log.debug("Supplying headers %s and data %s.", request_headers.keys(), data)
            log.debug("Passing through key word arguments %s.", kwargs)

        response = super().request(
            method, url, headers=request_headers, data=data, **kwargs
        )

        if retry_unauthorized and response.status_code == 401:
            log.info("Unauthorized response code. Fetch token and retry.")
            self.fetch_token()
            response = self._request(
                False, method, url, data=data, headers=headers, **kwargs
            )

        if log.isEnabledFor(logging.DEBUG):
            log.debug(
                "Response status code %d from %s %s with content: %s",
                response.status_code,
                method,
                url,
                response.content,
            )

        return response
