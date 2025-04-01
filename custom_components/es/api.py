import base64
import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)


class HeatPumpCloudAPI:
    """API client for heat pump cloud service."""

    def __init__(self, username: str, password: str, api_url: str):
        self._username = username
        self._password = password
        self._api_url = api_url
        self._session = aiohttp.ClientSession()

    async def authenticate(self):
        """Authenticate with the API."""
        _LOGGER.debug('authenticate')

        result = await self._session.post(
            f"{self._api_url}/a/login",
            json={
                "username": str(base64.b64encode(self._username.encode("UTF-8"))),
                "password": str(base64.b64encode(self._password.encode("UTF-8")))
            }
        )
        _LOGGER.debug(f'authenticate:{result.text()=}')

    async def async_get_status(self):
        """Get current status from API."""
        _LOGGER.debug('async_get_status')
        async with self._session.get(f"{self._api_url}/status") as resp:
            return await resp.json()

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
