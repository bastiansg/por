from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from por.llm_agents.schema import (
    ClothingDescription,
    PBFImageDescriberOutput,
    PeopleDescription,
    SceneDescription,
)
from por.meta.schema import PsychologicalProfile


class ImagePrompterDeps(BaseModel):
    question: StrictStr
    psychological_profile: PsychologicalProfile
    scene_description: SceneDescription
    people_description: PeopleDescription
    clothing_description: ClothingDescription


agent = Agent(  # type: ignore
    name="image-prompter",
    model="gpt-5.6-sol",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=ImagePrompterDeps,
    output_type=ToolOutput(PBFImageDescriberOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[ImagePrompterDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class ImagePrompter(LLMAgent[ImagePrompterDeps, PBFImageDescriberOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
