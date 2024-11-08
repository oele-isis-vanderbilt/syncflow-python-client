#!/usr/bin/env python3
import argparse
import asyncio
import json

from dotenv import load_dotenv

from syncflow.models import CreateSessionRequest, RegisterDeviceRequest, TokenRequest
from syncflow.project_client import ProjectClient


async def list_sessions(args, client):
    """List all available sessions"""
    sessions = await client.list_sessions()
    if args.json:
        print(json.dumps([session.__dict__ for session in sessions], indent=2))
    else:
        for session in sessions:
            print(f"Session ID: {session.id}")


async def get_session(args, client):
    """Get details for a specific session"""
    session = await client.list_session(args.session_id)
    if args.json:
        print(json.dumps(session.__dict__, indent=2))
    else:
        print(f"Session Details: {session}")


async def create_session(args, client):
    """Create a new session"""
    request = CreateSessionRequest(
        name=args.name,
        max_participants=args.max_participants,
        recording_enabled=args.recording_enabled,
    )
    session = await client.create_session(request)
    if args.json:
        print(json.dumps(session.__dict__, indent=2))
    else:
        print(f"Created Session: {session}")


async def stop_session(args, client):
    """Stop a specific session"""
    session = await client.stop_session(args.session_id)
    if args.json:
        print(json.dumps(session.__dict__, indent=2))
    else:
        print(f"Stopped Session: {session}")


async def get_project_details(args, client):
    """Get project details"""
    details = await client.get_project_details()
    if args.json:
        print(json.dumps(details.__dict__, indent=2))
    else:
        print(f"Project Details: {details}")


async def get_project_summary(args, client):
    """Get project summary"""
    summary = await client.summarize_project()
    print(f"Project Summary: {summary}")


async def delete_project(args, client):
    """Delete the project"""
    result = await client.delete_project()
    print(f"Project deleted: {result}")


async def list_participants(args, client):
    """List participants for a specific session"""
    participants = await client.list_participants(args.session_id)
    print(participants)
    if args.json:
        print(
            json.dumps([participant.__dict__ for participant in participants], indent=2)
        )
    else:
        for participant in participants:
            print(f"Participant: {participant}")


async def generate_token(args, client):
    """Generate a session token"""
    request = TokenRequest(
        participant_id=args.participant_id, participant_name=args.participant_name
    )
    token = await client.generate_session_token(args.session_id, request)
    if args.json:
        print(json.dumps(token.__dict__, indent=2))
    else:
        print(f"Generated Token: {token}")


async def get_livekit_info(args, client):
    """Get LiveKit session information"""
    info = await client.get_livekit_session_info(args.session_id)
    print(json.dumps(info, indent=2))


async def register_device(args, client):
    """Register a new device"""
    request = RegisterDeviceRequest(
        name=args.name,
        device_type=args.device_type,
        metadata=json.loads(args.metadata) if args.metadata else {},
    )
    device = await client.register_device(request)
    if args.json:
        print(json.dumps(device.__dict__, indent=2))
    else:
        print(f"Registered Device: {device}")


async def list_devices(args, client):
    """List all registered devices"""
    devices = await client.list_devices()
    if args.json:
        print(json.dumps([device.__dict__ for device in devices], indent=2))
    else:
        for device in devices:
            print(f"Device: {device}")


async def get_device(args, client):
    """Get details for a specific device"""
    device = await client.list_device(args.device_id)
    if args.json:
        print(json.dumps(device.__dict__, indent=2))
    else:
        print(f"Device Details: {device}")


async def delete_device(args, client):
    """Delete a specific device"""
    device = await client.delete_device(args.device_id)
    if args.json:
        print(json.dumps(device.__dict__, indent=2))
    else:
        print(f"Deleted Device: {device}")


async def main():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.required = True

    # Sessions commands
    sessions_parser = subparsers.add_parser("sessions", help="List all sessions")
    sessions_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    sessions_parser.set_defaults(func=list_sessions)

    session_parser = subparsers.add_parser("session", help="Get session details")
    session_parser.add_argument("session_id", help="Session ID")
    session_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    session_parser.set_defaults(func=get_session)

    create_session_parser = subparsers.add_parser(
        "create-session", help="Create a new session"
    )
    create_session_parser.add_argument("name", help="Session name")
    create_session_parser.add_argument(
        "--max-participants", type=int, default=10, help="Maximum participants"
    )
    create_session_parser.add_argument(
        "--recording-enabled", action="store_true", help="Enable recording"
    )
    create_session_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    create_session_parser.set_defaults(func=create_session)

    stop_session_parser = subparsers.add_parser("stop-session", help="Stop a session")
    stop_session_parser.add_argument("session_id", help="Session ID")
    stop_session_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    stop_session_parser.set_defaults(func=stop_session)

    # Project commands
    details_parser = subparsers.add_parser("details", help="Get project details")
    details_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    details_parser.set_defaults(func=get_project_details)

    summary_parser = subparsers.add_parser("summary", help="Get project summary")
    summary_parser.set_defaults(func=get_project_summary)

    delete_project_parser = subparsers.add_parser(
        "delete-project", help="Delete the project"
    )
    delete_project_parser.set_defaults(func=delete_project)

    # Participants commands
    participants_parser = subparsers.add_parser(
        "participants", help="List participants for a session"
    )
    participants_parser.add_argument("session_id", help="Session ID")
    participants_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    participants_parser.set_defaults(func=list_participants)

    # Token commands
    token_parser = subparsers.add_parser(
        "generate-token", help="Generate a session token"
    )
    token_parser.add_argument("session_id", help="Session ID")
    token_parser.add_argument("participant_id", help="Participant ID")
    token_parser.add_argument("participant_name", help="Participant name")
    token_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    token_parser.set_defaults(func=generate_token)

    # LiveKit commands
    livekit_parser = subparsers.add_parser(
        "livekit-info", help="Get LiveKit session information"
    )
    livekit_parser.add_argument("session_id", help="Session ID")
    livekit_parser.set_defaults(func=get_livekit_info)

    # Device commands
    register_device_parser = subparsers.add_parser(
        "register-device", help="Register a new device"
    )
    register_device_parser.add_argument("name", help="Device name")
    register_device_parser.add_argument("device_type", help="Device type")
    register_device_parser.add_argument(
        "--metadata", help="Device metadata as JSON string"
    )
    register_device_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    register_device_parser.set_defaults(func=register_device)

    devices_parser = subparsers.add_parser("devices", help="List all devices")
    devices_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    devices_parser.set_defaults(func=list_devices)

    device_parser = subparsers.add_parser("device", help="Get device details")
    device_parser.add_argument("device_id", help="Device ID")
    device_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    device_parser.set_defaults(func=get_device)

    delete_device_parser = subparsers.add_parser(
        "delete-device", help="Delete a device"
    )
    delete_device_parser.add_argument("device_id", help="Device ID")
    delete_device_parser.add_argument(
        "--json", action="store_true", help="Output in JSON format"
    )
    delete_device_parser.set_defaults(func=delete_device)

    args = parser.parse_args()
    client = ProjectClient()

    try:
        await args.func(args, client)
    finally:
        await client.aclose()


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
