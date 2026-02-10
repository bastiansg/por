from pydantic_ai import ToolOutput

from pydantic import BaseModel, StrictStr, Field

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent

from .psychological_describer import PsychologicalDescriberOutput
from .image_describer import PhysicalDescription, ClothingDescription


class ImagePrompterDeps(BaseModel):
    question: StrictStr
    psychological_profile: PsychologicalDescriberOutput
    physical_description: PhysicalDescription
    clothing_description: ClothingDescription


class ImagePrompterOutput(BaseModel):
    flux_prompt: StrictStr = Field(
        description="Flux image-generation prompt.",
        min_length=1,
    )


class ImagePrompter(LLMAgent[ImagePrompterDeps, ImagePrompterOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/image-prompter.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=ImagePrompterDeps,
            output_type=ToolOutput(ImagePrompterOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
