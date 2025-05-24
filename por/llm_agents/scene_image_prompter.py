from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class SceneImagePrompterInput(BaseModel):
    people_description: StrictStr
    psychological_description: StrictStr
    proposed_scene: StrictStr
    output_language: LanguageName


class SceneImagePrompterOutput(BaseModel):
    scene_description: StrictStr = Field(
        description="An adapted version of the proposed scene."
    )


class SceneImagePrompter(
    LLMAgent[SceneImagePrompterInput, SceneImagePrompterOutput]
):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/scene-image-prompter.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=SceneImagePrompterInput,
            agent_output=SceneImagePrompterOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
