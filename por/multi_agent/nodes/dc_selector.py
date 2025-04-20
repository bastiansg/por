from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import DCSelector, DCSelectorInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import dry_mode_handler, get_str_person_description


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["selected_dc_poem"],
)
async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing dc_selector...")
    conf = config["configurable"]

    dc_poems = conf["dc_poems"]
    dc_poem_map = {poem["poem_id"]: poem["poem"] for poem in dc_poems}
    str_person_description = get_str_person_description(state=state)

    dc_selector = DCSelector()
    dc_selector_output = await dc_selector.generate(
        agent_input=DCSelectorInput(
            person_description=str_person_description,
            dc_poems=conf["dc_poems"],
        )
    )

    return {
        "selected_dc_poem": dc_poem_map[dc_selector_output.poem_id],
    }


dc_selector = Node(
    name="dc_selector",
    run=run,
)
