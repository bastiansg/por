from multi_agents.graph import Node

from common.logger import get_logger
from common.utils.json_data import get_pretty

from por.llm_agents import NumberArchetypes, NumberArchetypesInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_str_description


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing number_archetypes...")
    conf = config["configurable"]

    number_archetypes = NumberArchetypes()
    str_psychological_description = get_str_description(
        description=state.psychological_description.model_dump()
    )

    str_archetypes = get_pretty(obj=conf["number_archetypes"], indent=1)
    number_archetypes_output = await number_archetypes.generate(
        agent_input=NumberArchetypesInput(
            number_archetypes=str_archetypes,
            psychological_description=str_psychological_description,
        )
    )

    return {
        "lucky_number": number_archetypes_output.number,
    }


number_archetypes = Node(
    name="number_archetypes",
    run=run,
)
