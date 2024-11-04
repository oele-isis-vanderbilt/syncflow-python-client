import os
import time

import httpx
import jwt

from syncflow.models import ProjectTokenClaims, RegisterDeviceRequest



class ProjectClient:
    def __init__(
        self,
        server_url: str = None,
        project_id: str = None,
        api_key: str = None,
        api_secret: str = None,
    ):
        self.server_url = server_url or os.getenv("SYNCFLOW_API_URL")
        self.project_id = project_id or os.getenv("SYNCFLOW_PROJECT_ID")
        self.api_key = api_key or os.getenv("SYNCFLOW_API_KEY")
        self.api_secret = api_secret or os.getenv("SYNCFLOW_API_SECRET")
        self.httpx_client = httpx.AsyncClient(base_url=self.server_url)
        self._api_token = None

    @property
    def api_token(self):
        if not self._api_token:
            self._api_token = self.get_api_token()
        if self.is_expired(self._api_token):
            self._api_token = self.get_api_token()
        return self._api_token

    def is_expired(self, token):
        decoded_jwt = jwt.decode(token, self.api_secret, algorithms=["HS256"])
        api_token = ProjectTokenClaims.model_validate(decoded_jwt)
        return api_token.is_expired()
    
    async def list_sessions(self):
        jwt = self.api_token
        response = await self.httpx_client.get(
            f"/projects/{self.project_id}/sessions",
            headers={
                "Authorization": f"Bearer {jwt}",
                "Content-Type": "application/json",
            },
        )

        response.raise_for_status()
        return response.json()

    async def summarize_project(self):
        jwt = self.api_token
        response = await self.httpx_client.get(
            f"/projects/{self.project_id}/summarize",
            headers={
                "Authorization": f"Bearer {jwt}",
                "Content-Type": "application/json",
            },
        )

        response.raise_for_status()
        return response.json()

    async def register_device(self, device: RegisterDeviceRequest):
        jwt = self.api_token

        response = await self.httpx_client.post(
            f"/projects/{self.project_id}/devices/register",
            headers={
                "Authorization": f"Bearer {jwt}",
                "Content-Type": "application/json",
            },
            json=device.model_dump(mode="json", by_alias=True),
        )
        response.raise_for_status()
        return response.json()

    async def list_devices(self):
        jwt = self.api_token
        response = await self.httpx_client.get(
            f"/projects/{self.project_id}/devices",
            headers={
                "Authorization": f"Bearer {jwt}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()

    async def aclose(self):
        await self.httpx_client.aclose()

    def get_api_token(self):
        claims = ProjectTokenClaims(
            iat=int(time.time()),
            exp=int(time.time()) + 60 * 60,
            iss=self.api_key,
            project_id=self.project_id,
        )

        dict_model = claims.model_dump(by_alias=True)

        return jwt.encode(dict_model, self.api_secret, algorithm="HS256")
