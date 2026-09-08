from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, PositiveInt, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

from por.config import config
from por.llm_agents.schema import ImageDescriptionOutput, SceneDescription
from por.prompt import format_prompt
from por.utils.tokens import count_t5_tokens, validate_t5_token_count


class PBFImageDescriberDeps(BaseModel):
    caption_header: StrictStr
    t5_tokenizer_name: StrictStr
    flux_max_tokens: PositiveInt


class PBFSceneDescription(SceneDescription):
    composition: StrictStr = Field(
        description="Framing and viewpoint only.",
        min_length=1,
    )


class PBFImageDescriberOutput(ImageDescriptionOutput[PBFSceneDescription]):
    def count_prompt_tokens(
        self,
        caption_header: str,
        tokenizer_name: str,
    ) -> int:
        return count_t5_tokens(
            format_prompt(self, caption_header),
            tokenizer_name,
        )


agent = Agent(
    name="pbf-image-describer",
    model="openai:gpt-5.6-sol",
    model_settings=OpenAIResponsesModelSettings(
        openai_reasoning_effort="low",
        max_tokens=config.flux_max_tokens,
    ),
    deps_type=PBFImageDescriberDeps,
    output_type=ToolOutput(PBFImageDescriberOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


@agent.output_validator
async def validate_prompt_tokens(
    ctx: RunContext[PBFImageDescriberDeps],
    output: PBFImageDescriberOutput,
) -> PBFImageDescriberOutput:
    token_count = output.count_prompt_tokens(
        ctx.deps.caption_header,
        ctx.deps.t5_tokenizer_name,
    )

    validate_t5_token_count(token_count, ctx.deps.flux_max_tokens)

    return output


class PBFImageDescriber(
    LLMAgent[PBFImageDescriberDeps, PBFImageDescriberOutput]
):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
