from multi_agents.graph import Node

from common.logger import get_logger
from common.utils.json_data import get_pretty

from por.llm_agents import NumberArchetypes, NumberArchetypesInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_str_description


logger = get_logger(__name__)


def get_number_archetype_map(number_archetypes: list[dict]) -> dict:
    return {na["archetype_name"]: na for na in number_archetypes}


def parse_archetypes(number_archetypes: list[dict]) -> list[dict]:
    return [
        {
            "archetype_name": na["archetype_name"],
            "traits": na["traits"],
        }
        for na in number_archetypes
    ]


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing number_archetypes...")
    conf = config["configurable"]

    archetypes = conf["number_archetypes"]
    archetype_map = get_number_archetype_map(number_archetypes=archetypes)

    parsed_archetypes = parse_archetypes(number_archetypes=archetypes)
    str_archetypes = get_pretty(obj=parsed_archetypes, indent=1)

    str_psychological_description = get_str_description(
        description=state.psychological_description.model_dump()
    )

    number_archetypes = NumberArchetypes()
    number_archetypes_output = await number_archetypes.generate(
        agent_input=NumberArchetypesInput(
            number_archetypes=str_archetypes,
            psychological_description=str_psychological_description,
        )
    )

    return {
        "lucky_number": archetype_map[number_archetypes_output.archetype_name],
    }


number_archetypes = Node(
    name="number_archetypes",
    run=run,
)
