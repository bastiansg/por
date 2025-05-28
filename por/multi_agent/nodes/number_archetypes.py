from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import NumberArchetypes, NumberArchetypesInput
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


def get_number_archetype_map(number_archetypes: list[dict]) -> dict:
    return {na["archetype_name"]: na["number"] for na in number_archetypes}


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
    archetype_map = {na["archetype_name"]: na["number"] for na in archetypes}

    number_archetypes = NumberArchetypes()
    number_archetypes_output = await number_archetypes.generate(
        agent_input=NumberArchetypesInput(
            number_archetypes=archetypes,
            psychological_description=state.psychological_description,
        )
    )

    return {
        "lucky_number": archetype_map[number_archetypes_output.archetype_name],
    }


number_archetypes = Node(
    name="number_archetypes",
    run=run,
)
