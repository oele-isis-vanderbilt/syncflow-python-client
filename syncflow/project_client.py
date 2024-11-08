import os
import time
from typing import List

import httpx
import jwt

from syncflow.models import (
    CreateSessionRequest,
    DeviceResponse,
    ParticipantInfo,
    ProjectInfo,
    ProjectSessionResponse,
    ProjectSummary,
    ProjectTokenClaims,
    RegisterDeviceRequest,
    TokenRequest,
    TokenResponse,
)


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class ProjectClient:
    def __init__(
        self,
        server_url: str = None,
        project_id: str = None,
        api_key: str = None,
        api_secret: str = None,
    ):
        self.server_url = server_url or os.getenv("SYNCFLOW_SERVER_URL")
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

    async def authorized_fetch(self, url, method="GET", data=None):
        """
        Perform an authorized API fetch with the necessary headers.

        Args:
            url (str): The API endpoint URL.
            method (str, optional): The HTTP method. Defaults to "GET".
            data (dict, optional): The request payload. Defaults to None.

        Returns:
            Any: The API response JSON parsed into a Pydantic model.
        """
        jwt_token = self.api_token
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }

        try:
            if method == "GET":
                response = await self.httpx_client.get(url, headers=headers)
            elif method == "POST":
                response = await self.httpx_client.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = await self.httpx_client.put(url, headers=headers, json=data)
            elif method == "DELETE":
                response = await self.httpx_client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            raise HttpError(e.response.status_code, e.response.text)

    async def get_project_details(self) -> ProjectInfo:
        response_data = await self.authorized_fetch(f"/projects/{self.project_id}")
        return ProjectInfo(**response_data)

    async def delete_project(self) -> ProjectInfo:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}", method="DELETE"
        )
        return ProjectInfo(**response_data)

    async def summarize_project(self) -> ProjectSummary:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/summarize"
        )
        return ProjectSummary(**response_data)

    async def create_session(
        self, new_session_request: CreateSessionRequest
    ) -> ProjectSessionResponse:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/create-session",
            method="POST",
            data=new_session_request.dict(),
        )
        return ProjectSessionResponse(**response_data)

    async def list_sessions(self) -> List[ProjectSessionResponse]:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/sessions"
        )
        return [ProjectSessionResponse(**session) for session in response_data]

    async def list_session(self, session_id: str) -> ProjectSessionResponse:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/sessions/{session_id}"
        )
        return ProjectSessionResponse(**response_data)

    async def list_participants(self, session_id: str) -> List[ParticipantInfo]:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/sessions/{session_id}/participants"
        )
        return [ParticipantInfo(**participant) for participant in response_data]

    async def generate_session_token(
        self, session_id: str, token_request: TokenRequest
    ) -> TokenResponse:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/sessions/{session_id}/token",
            method="POST",
            data=token_request.model_dump(mode="json", by_alias=True),
        )
        return TokenResponse(**response_data)

    async def get_livekit_session_info(self, session_id: str) -> dict:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/sessions/{session_id}/livekit-session-info"
        )
        return response_data

    async def stop_session(self, session_id: str) -> ProjectSessionResponse:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/sessions/{session_id}/stop",
            method="POST",
            data={},
        )
        return ProjectSessionResponse(**response_data)

    async def register_device(self, device: RegisterDeviceRequest) -> DeviceResponse:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/devices/register",
            method="POST",
            data=device.dict(),
        )
        return DeviceResponse(**response_data)

    async def list_devices(self) -> List[DeviceResponse]:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/devices"
        )
        return [DeviceResponse(**device) for device in response_data]

    async def list_device(self, device_id: str) -> DeviceResponse:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/devices/{device_id}"
        )
        return DeviceResponse(**response_data)

    async def delete_device(self, device_id: str) -> DeviceResponse:
        response_data = await self.authorized_fetch(
            f"/projects/{self.project_id}/devices/{device_id}", method="DELETE"
        )
        return DeviceResponse(**response_data)

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
