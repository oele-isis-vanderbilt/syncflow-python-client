from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
import time

class ProjectTokenClaims(BaseModel):
    iat: int = Field()
    iss: str = Field()
    exp: int = Field()

    project_id: str = Field()

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    def is_expired(self):
        return self.exp < time.time()


class RegisterDeviceRequest(BaseModel):
    name: str = Field(
        ...,
        description="The name of the device",
    )

    group: str = Field(
        ...,
        description="The group of the device",
    )

    comments: Optional[str] = Field(
        None,
        description="Comments about the device",
    )


class CreateSessionRequest(BaseModel):
    