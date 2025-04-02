import base64
import logging
from .exceptions import AuthenticationError
import aiohttp

_LOGGER = logging.getLogger(__name__)


class HeatPumpCloudAPI:
    """API client for heat pump cloud service."""

    def __init__(self, username: str, password: str, api_url: str):
        self._username = username
        self._password = password
        self._api_url = api_url
        self._session = aiohttp.ClientSession()
        self._authenticated = False

    async def authenticate(self):
        """Two-step authentication with specific login URL"""
        try:
            # First authentication step to specific login endpoint
            async with self._session.post(
                    f"{self._api_url}/a/login",
                    json={
                        "username": str(base64.b64encode(self._username.encode("UTF-8"))),
                        "password": str(base64.b64encode(self._password.encode("UTF-8")))
                    }
            ) as response:
                if response.status != 200:
                    raise AuthenticationError("Invalid credentials")

            # Second step to get session cookie (using base API URL)
            # THIS IS NOT YET THE CORRECT URL
            # async with self._session.get(f"{self._api_url}/auth/session") as response:
            #     if response.status != 200:
            #         raise AuthenticationError("Session setup failed")
            #
            #     # Verify cookie is present
            #     if "JSESSIONID" not in self._session.cookie_jar.filter_cookies(self._api_url):
            #         raise AuthenticationError("Session cookie not received")

            self._authenticated = True
        except aiohttp.ClientError as err:
            raise AuthenticationError(f"Connection error: {str(err)}") from err

    async def async_get_status(self):
        """Get current status from API."""
        _LOGGER.debug('async_get_status')
        return # TODO NOT YET!
        #async with self._session.get(f"{self._api_url}/status") as resp:
        #    return await resp.json()

    async def async_set_temperature(self, temperature: float):
        """Set target temperature."""
        _LOGGER.debug('async_set_temperature')
        await self._session.post(
            f"{self._api_url}/temperature",
            json={"temperature": temperature}
        )

    async def async_set_mode(self, mode: str):
        """Set operation mode."""
        _LOGGER.debug('async_set_mode')
        await self._session.post(
            f"{self._api_url}/mode",
            json={"mode": mode}
        )

    async def close(self):
        """Close the session."""
        _LOGGER.debug('close')
        await self._session.close()
