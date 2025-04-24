from typing import Literal
from functools import lru_cache

from por.conf import multi_agent
from common.utils.json_data import load_json
from common.utils.yaml_data import load_yaml

from .schema import ConfigSchema


BASE_CONF_PATH = multi_agent.__path__[0]
MODEL_CONF_MAP = {
    "grcra": f"{BASE_CONF_PATH}/grcra-conf.yml",
}


@lru_cache(maxsize=1)
def get_multi_agent_config(model: Literal["grcra"]) -> ConfigSchema:
    return ConfigSchema(
        **(
            load_yaml(file_path=f"{BASE_CONF_PATH}/conf.yml")
            | load_yaml(file_path=MODEL_CONF_MAP[model])
            | {
                "dc_poems": [
                    {
                        "poem_id": idx,
                        "poem": poem,
                    }
                    for idx, poem in enumerate(
                        load_json(
                            "/resources/documents/dos-corazones/poemas.json"
                        ),
                        start=1,
                    )
                ],
                "fc_messages": [
                    {
                        "message_id": idx,
                        "message": message,
                    }
                    for idx, message in enumerate(
                        load_json(
                            "/resources/documents/fortune-cookie/messages.json"
                        ),
                        start=1,
                    )
                ],
                "number_archetypes": load_json(
                    "/resources/documents/numerology/archetypes.json"
                ),
            }
        )
    )
