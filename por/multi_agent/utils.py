from typing import Literal
from functools import lru_cache

from por.conf import multi_agent
from common.utils.yaml_data import load_yaml

from .schema import ConfigSchema


BASE_CONF_PATH = multi_agent.__path__[0]
MODEL_CONF_MAP = {
    "grcra": f"{BASE_CONF_PATH}/grcra-conf.yml",
}


@lru_cache(maxsize=1)
def get_multi_agent_config(model: Literal["grcra"]) -> ConfigSchema:
    base_conf = load_yaml(file_path=f"{BASE_CONF_PATH}/conf.yml")
    model_conf = load_yaml(file_path=MODEL_CONF_MAP[model])

    return ConfigSchema(**(base_conf | model_conf))
