from pydantic_ai import NativeOutput
from pydantic_ai.models import Model
from pydantic import BaseModel, Field

from common.cache import RedisCache
from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import query_parser


class QueryParserOutput(BaseModel):
    parsed_query: str | None = Field(description="The parsed query.")


class QueryParser(LLMAgent[None, QueryParserOutput]):
    def __init__(
        self,
        conf_path: str = f"{query_parser.__path__[0]}/query-parser.yml",
        model: Model | None = None,
        max_concurrency: int = 10,
        cache: RedisCache | None = None,
        retries: int = 3,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=NativeOutput(QueryParserOutput),  # type: ignore
            model=model,
            max_concurrency=max_concurrency,
            cache=cache,
            retries=retries,
        )
