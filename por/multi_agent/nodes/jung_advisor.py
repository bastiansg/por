from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import JungAdvisor, JungAdvisorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler, get_retriever, get_str_person_description


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["jung_advise"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing jung_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    str_person_description = get_str_person_description(state=state)

    retriever_items = await retriever.dense_search(
        collection_name="el-libro-rojo",
        query=str_person_description,
    )

    jung_text_chunks = [ri.text for ri in retriever_items]

    jung_advisor = JungAdvisor()
    jung_advisor_output = await jung_advisor.generate(
        agent_input=JungAdvisorInput(
            person_description=str_person_description,
            jung_text_chunks=jung_text_chunks,
            output_language=conf["output_language"],
        )
    )

    return {
        "jung_text_chunks": jung_text_chunks,
        "jung_advise": jung_advisor_output.jung_advise,
    }


jung_advisor = Node(
    name="jung_advisor",
    run=run,
)
