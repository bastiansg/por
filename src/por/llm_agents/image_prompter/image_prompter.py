import warnings
from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, PositiveInt
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

from por.config import config
from por.llm_agents.schema import ImageDescriptionOutput, SceneDescription
from por.llm_agents.tools import count_flux_tokens_tool
from por.prompt import format_prompt
from por.utils.tokens import count_t5_tokens


class ImagePrompterDeps(BaseModel):
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
    model="openai:gpt-5.6-sol",
    model_settings=OpenAIResponsesModelSettings(openai_reasoning_effort="low"),
    deps_type=ImagePrompterDeps,
    output_type=ToolOutput(ImagePrompterOutput),
    retries=3,
    tools=[count_flux_tokens_tool],
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[ImagePrompterDeps]) -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ).format(flux_max_tokens=ctx.deps.flux_max_tokens)


@agent.output_validator
async def warn_if_prompt_exceeds_token_limit(
    ctx: RunContext[ImagePrompterDeps],
    output: ImagePrompterOutput,
) -> ImagePrompterOutput:
    token_count = output.count_prompt_tokens(
        config.caption_header,
        config.t5_tokenizer_name,
    )

    if token_count > ctx.deps.flux_max_tokens:
        warnings.warn(
            f"The formatted FLUX prompt contains {token_count} T5 tokens; "
            f"the configured limit is {ctx.deps.flux_max_tokens} tokens.",
            stacklevel=2,
        )

    return output


class ImagePrompter(LLMAgent[ImagePrompterDeps, ImagePrompterOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
