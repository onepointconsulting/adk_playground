# ADK Playground

Agents Development Kit playground to play around with Google's new agent toolkit for building agents.

## Setup

We used uv to setup the project.

Execute the following commands:

```bash
uv venv
# Windows
.venv\Scripts\activate
uv sync
```

## Configuration

You will need to configure the environment variables that you can find in the [.env_example](.env_example) file.

## Running the project

In order to run the project you can run this command:

```bash
adk web
```

This will start the Web UI at http://127.0.0.1:8000