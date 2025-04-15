from google.adk.agents import Agent
from adk_playground.config import cfg, load_config
from adk_playground.tools import get_weather_current_str, get_weather_forecast_as_str, get_current_time

config = load_config()

agent_weather_config = config["agent"]["weather"]

def create_agent() -> Agent:
    agent = Agent(
        name=agent_weather_config["name"],
        model=cfg.gemini_model_name,
        description=agent_weather_config["description"],
        instruction=agent_weather_config["instruction"],
        tools=[get_weather_current_str, get_weather_forecast_as_str,get_current_time]
    )
    return agent


root_agent = create_agent()
