from pydantic_ai import ToolOutput
from pydantic_ai.mcp import MCPServer

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent


# from .psychological_describer import PsychologicalDescriberOutput


class SATCAdvisorDeps(BaseModel):
    # psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    output_language: LanguageName


class SATCAdvisorOutput(BaseModel):
    satc_advice: StrictStr = Field(
        description="Advice written in Carrie Bradshaw's voice, as if speaking to a close friend at a restaurant.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of chunk_id values used to generate the advice.",
        min_length=1,
    )


class SATCAdvisor(LLMAgent[SATCAdvisorDeps, SATCAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/satc-advisor.yml",
        mcp_servers: list[MCPServer] = [],
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=SATCAdvisorDeps,
            output_type=ToolOutput(SATCAdvisorOutput),  # type: ignore
            mcp_servers=mcp_servers,
            retries=3,
            max_concurrency=max_concurrency,
        )
