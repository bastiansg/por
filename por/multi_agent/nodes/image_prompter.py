import random
import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import SceneImagePrompter, SceneImagePrompterInput
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_str_description, get_sensehat_dsp


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing image_prompter...")
    conf = config["configurable"]

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    await asyncio.sleep(1)
    sensehat_dsp.start_intermittent_image(
        image_name="si-03",
        refresh_rate=0.5,
    )

    people_description = state.image_description.people_description
    str_psychological_description = get_str_description(
        description=state.psychological_description.model_dump()
    )

    image_prompter = SceneImagePrompter()
    scene_image_prompter_output = await image_prompter.generate(
        agent_input=SceneImagePrompterInput(
            people_description=people_description,
            psychological_description=str_psychological_description,
            proposed_scene=random.choice(conf["train_image_captions"])[
                "scene_description"
            ],
            output_language="English",
        )
    )

    return {
        "image_generation_prompt": (
            f"{conf['generation_prompt_header']}\n"
            f"People description: {people_description}\n"
            f"Scene description: {scene_image_prompter_output.scene_description}\n"
        ),
    }


image_prompter = Node(
    name="image_prompter",
    run=run,
)
