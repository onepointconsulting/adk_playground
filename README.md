# ADK Playground

Agents Development Kit playground that implements a weather agent that know the current weather and time in a city and can also forecast the weather using https://open-meteo.com/.

## Setup

We used uv to setup the project.

Execute the following commands:

```bash
uv venv
# Windows
.venv\Scripts\activate
# Linix
source .venv/bin/activate
uv sync
```

## Configuration

You will need to configure the environment variables that you can find in the [.env_example](.env_example) file.

## Running the project

In order to run the project using a web UI you can run this command:

```bash
adk web
```

This will start the Web UI at http://127.0.0.1:8000

In order to run this project using the command line, you can use:

```bash
adk run adk_playground
```