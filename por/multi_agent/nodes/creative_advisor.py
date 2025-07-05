from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema, ConfigSchema
from por.llm_agents import CreativeAdvisor, CreativeAdvisorDeps


from .utils import get_retriever


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing creative_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    question = state.audio_transcription

    retriever_items = await retriever.dense_search(
        collection_name="el-arte-del-pensamiento-creativo",
        query=question,
        k=1,
    )

    creative_advisor = CreativeAdvisor()
    creative_capsule = retriever_items[0].text
    creative_advisor_output = await creative_advisor.generate(
        user_prompt="Provide your energetic and creatively actionable insights.",
        agent_deps=CreativeAdvisorDeps(
            psychological_profile=state.psychological_profile,
            creative_capsule=creative_capsule,
            question=question,
            output_language=conf["output_language"],
        ),
    )

    return {
        "creative_capsule": creative_capsule,
        "creative_advice": creative_advisor_output.creative_advice,
    }


creative_advisor = Node(
    name="creative_advisor",
    run=run,
)
