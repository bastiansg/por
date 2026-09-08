from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, PositiveInt, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from por.config import config
from por.llm_agents.schema import ImageDescriptionOutput, SceneDescription
from por.prompt import format_prompt
from por.utils.tokens import count_t5_tokens, validate_t5_token_count


class ImagePrompterDeps(BaseModel):
    caption_header: StrictStr
    t5_tokenizer_name: StrictStr
    flux_max_tokens: PositiveInt


class ImagePrompterOutput(ImageDescriptionOutput[SceneDescription]):
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
    name="image-prompter",
    model="openai-chat:gpt-5.6-sol",
    model_settings=OpenAIChatModelSettings(
        openai_reasoning_effort="none",
        max_tokens=config.flux_max_tokens,
    ),
    deps_type=ImagePrompterDeps,
    output_type=ToolOutput(ImagePrompterOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


@agent.output_validator
async def validate_prompt_tokens(
    ctx: RunContext[ImagePrompterDeps],
    output: ImagePrompterOutput,
) -> ImagePrompterOutput:
    token_count = output.count_prompt_tokens(
        ctx.deps.caption_header,
        ctx.deps.t5_tokenizer_name,
    )

    validate_t5_token_count(token_count, ctx.deps.flux_max_tokens)

    return output


class ImagePrompter(LLMAgent[ImagePrompterDeps, ImagePrompterOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
