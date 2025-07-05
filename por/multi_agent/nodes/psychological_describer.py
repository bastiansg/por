from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import PsychologicalDescriber, PsychologicalDescriberDeps
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing psychological_describer...")
    # conf = config["configurable"]

    psychological_describer_agent = PsychologicalDescriber()
    psychological_describer_output = await psychological_describer_agent.generate(
        user_prompt="Provide a psychological profile based on the provided information.",
        agent_deps=PsychologicalDescriberDeps(
            physical_description=state.image_description.physical_description,
            clothing_description=state.image_description.clothing_description,
            question=state.audio_transcription,
        ),
    )

    return {
        "psychological_profile": psychological_describer_output.psychological_profile,
    }


psychological_describer = Node(
    name="psychological_describer",
    run=run,
)
