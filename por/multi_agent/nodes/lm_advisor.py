from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import LMAdvisor, LMAdvisorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_retriever


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing lm_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    love_status = state.psychological_description.love_status

    retriever_items = await retriever.dense_search(
        collection_name="luis-miguel",
        query=love_status,
        k=10,
    )

    lm_text_chunks = [ri.text for ri in retriever_items]
    lm_advisor = LMAdvisor()
    lm_advisor_output = await lm_advisor.generate(
        agent_input=LMAdvisorInput(
            love_status=love_status,
            lm_text_chunks=lm_text_chunks,
            output_language=conf["output_language"],
        )
    )

    return {
        "lm_text_chunks": lm_text_chunks,
        "luis_miguel_advise": lm_advisor_output.luis_miguel_advise,
    }


lm_advisor = Node(
    name="lm_advisor",
    run=run,
)
