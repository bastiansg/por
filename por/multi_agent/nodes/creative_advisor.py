from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import CreativeAdvisor, CreativeAdvisorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_retriever


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing creative_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    creative_status = state.psychological_description.creative_status

    retriever_items = await retriever.dense_search(
        collection_name="el-arte-del-pensamiento-creativo",
        query=creative_status,
        k=10,
    )

    creative_text_chunks = [ri.text for ri in retriever_items]
    creative_advisor = CreativeAdvisor()
    creative_advisor_output = await creative_advisor.generate(
        agent_input=CreativeAdvisorInput(
            creative_status=creative_status,
            creative_text_chunks=creative_text_chunks,
            output_language=conf["output_language"],
        )
    )

    return {
        "creative_text_chunks": creative_text_chunks,
        "creative_advice": creative_advisor_output.creative_advice,
    }


creative_advisor = Node(
    name="creative_advisor",
    run=run,
)
