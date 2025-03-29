# <config_dir>/custom_components/heatpump_cloud/api.py
class HeatPumpCloudAPI:
    """API client with installation identifier support"""

    def __init__(self, username: str, password: str, api_url: str, session_url: str, mn: str):
        self._username = username
        self._password = password
        self._api_url = api_url
        self._session_url = session_url
        self._mn = mn  # Store installation identifier
        self._session = aiohttp.ClientSession()
        self._authenticated = False

    async def authenticate(self):
        """Custom authentication flow with configurable session URL"""
        try:
            # First step: Fixed login endpoint
            async with self._session.post(
                    "https://www.myheatpump.com/a/login",
                    json={"username": self._username, "password": self._password}
            ) as response:
                if response.status != 200:
                    raise AuthenticationError("Invalid credentials")

            # Second step: Configurable session endpoint
            async with self._session.get(self._session_url) as response:
                if response.status != 200:
                    raise AuthenticationError("Session setup failed")

                # Verify cookie for API domain
                if "JSESSIONID" not in self._session.cookie_jar.filter_cookies(self._api_url):
                    raise AuthenticationError("Session cookie not found for API domain")

            self._authenticated = True
        except aiohttp.ClientError as err:
            raise AuthenticationError(f"Connection error: {str(err)}") from err

    async def async_get_status(self):
        """Get status for specific installation"""
        if not self._authenticated:
            await self.authenticate()

        async with self._session.get(
                f"{self._api_url}/api/{self._mn}/status"  # Include mn in URL
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def async_set_temperature(self, temperature: float):
        """Set temperature for specific installation"""
        if not self._authenticated:
            await self.authenticate()

        async with self._session.post(
                f"{self._api_url}/api/{self._mn}/temperature",  # Include mn in URL
                json={"temperature": temperature}
        ) as resp:
            resp.raise_for_status()

    async def async_set_mode(self, mode: str):
        """Set operation mode for specific installation"""
        if not self._authenticated:
            await self.authenticate()

        async with self._session.post(
                f"{self._api_url}/api/{self._mn}/mode",  # Include mn in URL
                json={"mode": mode}
        ) as resp:
            resp.raise_for_status()