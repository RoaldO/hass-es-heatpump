# <config_dir>/custom_components/heatpump_cloud/api.py
class HeatPumpCloudAPI:
    """API client with installation identifier support"""

    def __init__(self, username: str, password: str, api_url: str, session_url: str, mn: str):
        self._username = username
        self._password = password
        self._api_url = api_url
        self._session_url = session_url
        self._mn = mn
        self._session = aiohttp.ClientSession()
        self._authenticated = False
        self._base_payload = {
            "mn": self._mn,
            "devid": 1  # Hardcoded device ID
        }

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
        """Get all sensor data from consolidated endpoint"""
        if not self._authenticated:
            await self.authenticate()

        async with self._session.post(
                "https://www.myheatpump.com/a/amt/realdata/get",
                json=self._base_payload
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

            # Map the API response to our expected format
            return {
                "current_temp": data.get("roomTemp"),
                "target_temp": data.get("setTemp"),
                "mode": data.get("workMode"),
                # Add other relevant fields from the response
                "outdoor_temp": data.get("outdoorTemp"),
                "power": data.get("powerConsumption")
            }

    async def async_set_temperature(self, temperature: float):
        """Set temperature through dedicated endpoint (if still valid)"""
        if not self._authenticated:
            await self.authenticate()

        payload = self._base_payload.copy()
        payload.update({"temperature": temperature})

        async with self._session.post(
                f"{self._api_url}/temperature",
                json=payload
        ) as resp:
            resp.raise_for_status()

    async def async_set_mode(self, mode: str):
        """Set operation mode through dedicated endpoint (if still valid)"""
        if not self._authenticated:
            await self.authenticate()

        payload = self._base_payload.copy()
        payload.update({"mode": mode})

        async with self._session.post(
                f"{self._api_url}/mode",
                json=payload
        ) as resp:
            resp.raise_for_status()