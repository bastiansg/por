from pydantic_ai import NativeOutput
from pydantic import BaseModel, StrictStr, Field

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import image_prompter


class OracleImagePrompterDeps(BaseModel):
    question: StrictStr


class OracleImagePrompterOutput(BaseModel):
    flux_prompt: StrictStr = Field(
        description="The surreal image-generation prompt.",
        min_length=1,
    )


class OracleImagePrompter(
    LLMAgent[OracleImagePrompterDeps, OracleImagePrompterOutput]
):
    def __init__(
        self,
        conf_path=f"{image_prompter.__path__[0]}/oracle-image-prompter.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=OracleImagePrompterDeps,
            output_type=NativeOutput(OracleImagePrompterOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
