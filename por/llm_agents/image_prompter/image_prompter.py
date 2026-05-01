from pathlib import Path

from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings
from pydantic import BaseModel, StrictStr, Field

from llm_agents.meta.interfaces import LLMAgent

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


agent = Agent(  # type: ignore
    name="image-prompter",
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=ImagePrompterDeps,
    output_type=NativeOutput(ImagePrompterOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[ImagePrompterDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class ImagePrompter(LLMAgent[ImagePrompterDeps, ImagePrompterOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
