from functools import lru_cache

from por.conf import multi_agent
from por.data import dc_poems, fc_messages

from common.utils.yaml_data import load_yaml

from .schema import ConfigSchema


CONF_PATH = multi_agent.__path__[0]


@lru_cache(maxsize=1)
def get_multi_agent_config() -> ConfigSchema:
    return ConfigSchema(
        **(
            load_yaml(file_path=f"{CONF_PATH}/conf.yml")
            | {
                "dc_poems": [
                    {
                        "poem_id": idx,
                        "poem": poem,
                    }
                    for idx, poem in enumerate(
                        dc_poems,
                        start=1,
                    )
                ],
                "fc_messages": [
                    {
                        "message_id": idx,
                        "message": message,
                    }
                    for idx, message in enumerate(
                        fc_messages,
                        start=1,
                    )
                ],
            }
        )
    )
