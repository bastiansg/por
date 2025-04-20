from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import TSAdvisor, TSAdvisorAdvisorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler, get_retriever, get_str_person_description


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["taylor_swift_advise"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing ts_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    str_person_description = get_str_person_description(state=state)

    retriever_items = await retriever.dense_search(
        collection_name="taylor-swift",
        query=str_person_description,
    )

    ts_text_chunks = [ri.text for ri in retriever_items]
    ts_advisor = TSAdvisor()
    ts_advisor_output = await ts_advisor.generate(
        agent_input=TSAdvisorAdvisorInput(
            person_description=str_person_description,
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
