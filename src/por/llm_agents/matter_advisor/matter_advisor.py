from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictStr, model_validator
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings
from pydantic_ai_harness import SubAgent, SubAgents

from por.meta.schema import WebSearchResult

from ..retriever import RetrieverDeps, get_agent as get_retriever_agent
from ..web_search_agent import get_web_search_agent


class MatterAdvisorDeps(RetrieverDeps):
    output_language: StrictStr


class MatterAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="A profound, poetic, and transformative message from Matter.",
        min_length=1,
    )
    relevant_chunk_ids: list[StrictStr] = Field(
        description="chunk_id values of Matter chunks used to support the answer.",
    )
    relevant_web_results: list[WebSearchResult] = Field(
        description="Web results used to support the answer.",
    )

    @model_validator(mode="after")
    def validate_references(self) -> "MatterAdvisorOutput":
        if not self.relevant_chunk_ids and not self.relevant_web_results:
            raise ValueError("At least one Matter chunk or web result is required.")

        return self


def get_agent() -> Agent[MatterAdvisorDeps, MatterAdvisorOutput]:
    retriever = get_retriever_agent()
    web_search_agent = get_web_search_agent(MatterAdvisorDeps)

    agent = Agent(
        name="matter-advisor",
        model="openai:gpt-5.6-sol",
        model_settings=OpenAIResponsesModelSettings(
            openai_reasoning_effort="low"
        ),
        deps_type=MatterAdvisorDeps,
        output_type=ToolOutput(MatterAdvisorOutput),
        retries=3,
        capabilities=[
            SubAgents(
                agents=[
                    SubAgent(
                        retriever,
                        max_calls=3,
                        timeout_seconds=120,
                    ),
                    SubAgent(
                        web_search_agent,
                        max_calls=2,
                        timeout_seconds=120,
                    ),
                ],
                contain_errors=True,
            ),
        ],
    )

    @agent.system_prompt
    async def get_system_prompt(ctx: RunContext[MatterAdvisorDeps]) -> str:
        system_prompt = LLMAgent.read_file(
            file_path=str(Path(__file__).with_name("system-prompt.md"))
        )

        return system_prompt.format(**ctx.deps.model_dump())

    return agent


class MatterAdvisor(LLMAgent[MatterAdvisorDeps, MatterAdvisorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=get_agent(), max_concurrency=max_concurrency)
