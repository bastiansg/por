from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import TSAdvisor, TSAdvisorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_retriever


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing ts_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    love_status = state.psychological_description.love_status

    retriever_items = await retriever.dense_search(
        collection_name="taylor-swift",
        query=love_status,
        k=10,
    )

    ts_text_chunks = [ri.text for ri in retriever_items]
    ts_advisor = TSAdvisor()
    ts_advisor_output = await ts_advisor.generate(
        agent_input=TSAdvisorInput(
            love_status=love_status,
            ts_text_chunks=ts_text_chunks,
            output_language=conf["output_language"],
        )
    )

    return {
        "ts_text_chunks": ts_text_chunks,
        "taylor_swift_advise": ts_advisor_output.taylor_swift_advise,
    }


ts_advisor = Node(
    name="ts_advisor",
    run=run,
)
