from pydantic_ai import NativeOutput
from pydantic import BaseModel, StrictStr, Field

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import image_prompter
from por.meta.schema import (
    PhysicalDescription,
    ClothingDescription,
    PsychologicalProfile,
)


class ImagePrompterDeps(BaseModel):
    question: StrictStr
    psychological_profile: PsychologicalProfile
    physical_description: PhysicalDescription
    clothing_description: ClothingDescription


class ImagePrompterOutput(BaseModel):
    flux_prompt: StrictStr = Field(
        description="The surreal image-generation prompt.",
        min_length=1,
    )


class ImagePrompter(LLMAgent[ImagePrompterDeps, ImagePrompterOutput]):
    def __init__(
        self,
        conf_path=f"{image_prompter.__path__[0]}/image-prompter.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=ImagePrompterDeps,
            output_type=NativeOutput(ImagePrompterOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
