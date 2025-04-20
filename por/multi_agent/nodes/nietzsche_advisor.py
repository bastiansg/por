from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import NietzscheAdvisor, NietzscheAdvisorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler, get_retriever, get_str_person_description


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["nietzsche_advise"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing nietzsche_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    str_person_description = get_str_person_description(state=state)

    retriever_items = await retriever.dense_search(
        collection_name="nietzsche",
        query=str_person_description,
    )

    nietzsche_text_chunks = [ri.text for ri in retriever_items]
    nietzsche_advisor = NietzscheAdvisor()
    nietzsche_advisor_output = await nietzsche_advisor.generate(
        agent_input=NietzscheAdvisorInput(
            person_description=str_person_description,
            nietzsche_text_chunks=nietzsche_text_chunks,
            output_language=conf["output_language"],
        )
    )

    return {
        "nietzsche_text_chunks": nietzsche_text_chunks,
        "nietzsche_advise": nietzsche_advisor_output.nietzsche_advise,
    }


nietzsche_advisor = Node(
    name="nietzsche_advisor",
    run=run,
)
