import time
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


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
    name: Optional[str] = Field(
        None,
        description="The name of the session",
    )

    comments: Optional[str] = Field(
        None,
        description="Comments about the session",
    )

    empty_timeout: Optional[int] = Field(
        None,
        description="The timeout period when the session is empty",
    )

    max_participants: Optional[int] = Field(
        None,
        description="Maximum number of participants allowed in the session",
    )

    auto_recording: Optional[bool] = Field(
        None,
        description="Whether the session should automatically start recording",
    )

    device_groups: Optional[List[str]] = Field(
        None,
        description="List of device groups associated with the session",
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class VideoGrantsWrapper(BaseModel):
    can_publish: bool = Field(
        default=True, description="Permission to publish media streams"
    )

    can_publish_data: bool = Field(
        default=True, description="Permission to publish data"
    )

    can_publish_sources: List[str] = Field(
        default=["camera", "micropohone", "screen_share", "screen_share_audio"],
        description="List of allowed publishing sources",
    )

    can_subscribe: bool = Field(
        default=True, description="Permission to subscribe to streams"
    )

    can_update_own_metadata: bool = Field(
        default=True, description="Permission to update own metadata"
    )

    hidden: bool = Field(default=False, description="Whether the participant is hidden")

    ingress_admin: bool = Field(
        default=False, description="Permission to administer ingress"
    )

    recorder: bool = Field(default=False, description="Permission to record")

    room: str = Field(..., description="Room identifier")

    room_admin: bool = Field(
        default=False, description="Permission to administer the room"
    )

    room_create: bool = Field(default=False, description="Permission to create rooms")

    room_join: bool = Field(default=True, description="Permission to join rooms")

    room_list: bool = Field(default=True, description="Permission to list rooms")

    room_record: bool = Field(default=False, description="Permission to record rooms")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class TokenRequest(BaseModel):
    identity: str = Field(
        ...,
        description="Identity of the token",
    )

    name: Optional[str] = Field(
        None,
        description="Name of the token",
    )

    video_grants: VideoGrantsWrapper = Field(
        ...,
        description="Video permissions and grant settings for the token",
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class MultimediaDetailsResponse(BaseModel):
    file_name: Optional[str] = None
    destination: Optional[str] = None
    publisher: Optional[str] = None
    track_id: Optional[str] = None
    presigned_url: Optional[str] = None
    presigned_url_expires: Optional[int] = None
    recording_start_time: Optional[int] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ParticipantTrackResponse(BaseModel):
    id: str
    sid: str
    name: Optional[str] = None
    kind: str
    source: str
    participant_id: str
    multimedia_details: Optional[MultimediaDetailsResponse] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class SessionParticipantResponse(BaseModel):
    id: str
    identity: str
    name: Optional[str]
    joined_at: int
    left_at: Optional[int] = None
    session_id: str
    tracks: List[ParticipantTrackResponse] = Field(
        default_factory=list,
        description="List of tracks in the session for the participant",
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class SessionEgressResponse(BaseModel):
    id: str
    track_id: str
    egress_id: str
    started_at: int
    egress_type: Optional[str] = None
    status: str
    destination: Optional[str] = None
    room_name: str
    session_id: str
    participant_id: Optional[str] = None
    db_track_id: Optional[str] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ProjectSessionResponse(BaseModel):
    id: str
    name: str
    started_at: int
    comments: str
    empty_timeout: int
    max_participants: int
    livekit_room_name: str
    project_id: str
    status: str
    num_participants: int
    num_recordings: int
    participants: List[SessionParticipantResponse] = Field(
        default_factory=list, description="List of participants in the session"
    )
    recordings: List[SessionEgressResponse] = Field(
        default_factory=list, description="List of recordings in the session"
    )
    duration: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ProjectInfo(BaseModel):
    id: str
    name: str
    description: str
    livekit_server_url: str
    storage_type: str
    bucket_name: str
    endpoint: str
    last_updated: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class TokenResponse(BaseModel):
    token: str
    identity: str
    livekit_server_url: Optional[str]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class DeviceResponse(BaseModel):
    id: str
    name: str
    group: str
    comments: Optional[str]
    registered_at: int
    registered_by: int
    project_id: str
    session_notification_exchange_name: Optional[str]
    session_notification_binding_key: Optional[str]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ProjectSummary(BaseModel):
    num_sessions: int
    num_active_sessions: int
    num_participants: int
    num_recordings: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ParticipantState(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    JOINING = "JOINING"


class ParticipantInfo(BaseModel):
    id: str
    identity: str
    name: Optional[str] = None
    state: ParticipantState
    tracks: List[dict]
    metadata: str
    joined_at: int
    permission: dict
    is_publisher: bool

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
