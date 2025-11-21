from pydantic_ai import ToolOutput
from pydantic_ai.mcp import MCPServer

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent


from .psychological_describer import PsychologicalDescriberOutput


class NietzscheAdvisorDeps(BaseModel):
    collection: StrictStr
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    output_language: LanguageName


class NietzscheAdvisorOutput(BaseModel):
    nietzsche_advise: StrictStr = Field(
        description="A profound, poetic, and incisive piece of Nietzschean advice.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of chunk_id values used to generate the advice.",
        min_length=1,
    )


class NietzscheAdvisor(LLMAgent[NietzscheAdvisorDeps, NietzscheAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/nietzsche-advisor.yml",
        mcp_servers: list[MCPServer] = [],
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=NietzscheAdvisorDeps,
            output_type=ToolOutput(NietzscheAdvisorOutput),  # type: ignore
            mcp_servers=mcp_servers,
            retries=3,
            max_concurrency=max_concurrency,
        )
