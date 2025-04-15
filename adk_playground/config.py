import os
from pathlib import Path

import tomli
from dotenv import load_dotenv

load_dotenv()


class Config:
    open_meteo_api_url = os.getenv("OPEN_METEO_API_URL")
    assert open_meteo_api_url, "OPEN_METEO_API_URL is not set"
    cache_expiry_str = os.getenv("CACHE_EXPIRY")
    assert cache_expiry_str, "CACHE_EXPIRY is not set"
    cache_expiry = int(cache_expiry_str)
    google_api_key = os.getenv("GOOGLE_API_KEY")
    assert google_api_key, "GOOGLE_API_KEY is not set"
    gemini_model_name = os.getenv("GEMINI_MODEL_NAME")
    assert gemini_model_name, "GEMINI_MODEL_NAME is not set"
    agent_root_folder = os.getenv("AGENT_ROOT_FOLDER")
    assert agent_root_folder, "AGENT_ROOT_FOLDER is not set"
    geo_coder_api_key = os.getenv("GEO_CODER_API_KEY")
    assert geo_coder_api_key, "GEO_CODER_API_KEY is not set"


cfg = Config()


def load_config() -> dict:
    config_path = Path(cfg.agent_root_folder) / "config.toml"
    return tomli.loads(config_path.read_text(encoding="utf-8"))
