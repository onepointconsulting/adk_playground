from adk_playground.config import cfg

def test_config():
    assert cfg.open_meteo_api_url, "OPEN_METEO_API_URL is not set"
    assert cfg.cache_expiry, "CACHE_EXPIRY is not set"
    assert cfg.cache_expiry > 0, "CACHE_EXPIRY must be greater than 0"

