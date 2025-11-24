from pydantic_ai import ToolOutput
from pydantic_ai.mcp import MCPServer
from pydantic_extra_types.language_code import LanguageName

from pydantic import BaseModel, StrictStr, Field

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent


class OracleDeps(BaseModel):
    gender_presentation: StrictStr
    question: StrictStr
    advice: StrictStr
    output_language: LanguageName


class OrcaleOutput(BaseModel):
    oracle_prophecy: StrictStr = Field(
        description="A future-directed message spoken in the Oracle's voice.",
        min_length=1,
    )


class Oracle(LLMAgent[OracleDeps, OrcaleOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/oracle.yml",
        mcp_servers: list[MCPServer] = [],
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=OracleDeps,
            output_type=ToolOutput(OrcaleOutput),  # type: ignore
            mcp_servers=mcp_servers,
            retries=3,
            max_concurrency=max_concurrency,
        )
