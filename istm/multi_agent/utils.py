from functools import lru_cache

from istm.conf import multi_agent
from common.utils.yaml_data import load_yaml

from .schema import ConfigSchema


BASE_CONF_PATH = multi_agent.__path__[0]


@lru_cache(maxsize=1)
def get_multi_agent_config() -> ConfigSchema:
    return ConfigSchema(**load_yaml(file_path=f"{BASE_CONF_PATH}/conf.yml"))
