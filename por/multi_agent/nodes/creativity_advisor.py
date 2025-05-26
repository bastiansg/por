from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import CreativityAdvisor, CreativityAdvisorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_retriever


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing creativity_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    creative_status = state.psychological_description.creative_status

    retriever_items = await retriever.dense_search(
        collection_name="el-arte-del-pensamiento-creativo",
        query=creative_status,
        k=10,
    )

    creativity_text_chunks = [ri.text for ri in retriever_items]
    creativity_advisor = CreativityAdvisor()
    creativity_advisor_output = await creativity_advisor.generate(
        agent_input=CreativityAdvisorInput(
            creative_status=creative_status,
            creativity_text_chunks=creativity_text_chunks,
            output_language=conf["output_language"],
        )
    )

    return {
        "creativity_text_chunks": creativity_text_chunks,
        "creativity_advice": creativity_advisor_output.creativity_advice,
    }


creativity_advisor = Node(
    name="creativity_advisor",
    run=run,
)
