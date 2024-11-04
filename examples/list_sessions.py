from syncflow.project_client import ProjectClient
from dotenv import load_dotenv


async def main():
    project_client = ProjectClient()
    sessions = await project_client.list_sessions()
    print(sessions)

if __name__ == "__main__":
    import asyncio
    load_dotenv()
    asyncio.run(main())
