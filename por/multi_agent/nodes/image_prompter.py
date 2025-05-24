import random
import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.utils.tokens import validate_num_tokens
from por.llm_agents import ImagePrompter, ImagePrompterInput
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


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
    selected_scene_description = random.choice(conf["train_image_captions"])[
        "scene_description"
    ]

    image_prompter = ImagePrompter()
    scene_image_prompter_output = await image_prompter.generate(
        agent_input=ImagePrompterInput(
            people_description=people_description,
            scene_description=selected_scene_description,
            output_language="English",
        )
    )

    image_generation_prompt = (
        f"{conf['generation_prompt_header']}\n"
        f"People description: {people_description}\n"
        f"Scene description: {scene_image_prompter_output.scene_description}\n"
    )

    assert validate_num_tokens(text=image_generation_prompt)
    return {
        "selected_scene_description": selected_scene_description,
        "image_generation_prompt": image_generation_prompt,
    }


image_prompter = Node(
    name="image_prompter",
    run=run,
)
