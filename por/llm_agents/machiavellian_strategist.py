from pydantic_ai import ToolOutput
from pydantic_ai.mcp import MCPServer

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent


from .psychological_describer import PsychologicalDescriberOutput


class MachiavellianStrategistDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    output_language: LanguageName


class MachiavellianStrategistOutput(BaseModel):
    machiavellian_advice: StrictStr = Field(
        description="Ruthless, strategic advice focusing on power and leverage.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of chunk_id values used to generate the advice.",
        min_length=1,
    )


class MachiavellianStrategist(LLMAgent[MachiavellianStrategistDeps, MachiavellianStrategistOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/machiavellian-strategist.yml",
        mcp_servers: list[MCPServer] = [],
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=MachiavellianStrategistDeps,
            output_type=ToolOutput(MachiavellianStrategistOutput),  # type: ignore
            mcp_servers=mcp_servers,
            retries=3,
            max_concurrency=max_concurrency,
        )
