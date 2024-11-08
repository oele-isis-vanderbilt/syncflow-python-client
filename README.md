# `SyncFlow` Python Client

<p align="center">
  <a href="https://github.com/oele-isis-vanderbilt/syncflow-python-client.git"><img src="./images/syncflow-python-client.png" alt="syncflow-node-client"></a>
</p>
<p align="center">
    <em>Reusable Python client implementation for SyncFlow.</em>
</p>


This is a reusable Python client implementation for SyncFlow. The idea here is to create necessary functionality to interact with the SyncFlow api, in a Python application. Primary beneficiaries of this package could be clients to SyncFlow, who have their own backend in Python and want to integrate with SyncFlow.

## Features
- Manage sessions, participants and recordings for a SyncFlow project
- Easy integration with existing Client applications

## Installation
Install the package using pip.

```sh
$ pip install .
```

## Usage
Installation provides a package client for SyncFlow projects:

```python
from syncflow.project_client import ProjectClient
from syncflow.models import CreateSessionRequest

async def main():
  client = ProjectClient(
    server_url="SYNCFLOW_SERVER_URL", # Or set the environment variable SYNCFLOW_SERVER_URL
    project_id="YOUR_SYNCFLOW_PROJECT_ID", # Or set the environment variable SYNCFLOW_PROJECT_ID
    api_key="YOUR_PROJECT_API_KEY", # Or set the environment variable SYNCFLOW_API_KEY
    api_secret="YOUR_PROJECT_API_SECRET", # Or set the environment variable SYNCFLOW_API_SECRET
  )

  # Create a new session
  session = await client.create_session(CreateSessionRequest(
    ...
  ))
  ...


if __name__ == "__main__":
  import asyncio
  asyncio.run(main())
```

See this example [file](./examples/main.py) for a detailed usage example.

## License
[APACHE 2.0](./LICENSE)

## Funding Information
This work is supported by the National Science Foundation under Grant No. DRL-2112635.
