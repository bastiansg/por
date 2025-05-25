import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.utils.tokens import get_num_tokens
from por.llm_agents import ImagePrompter, ImagePrompterInput
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp, get_str_description


logger = get_logger(__name__)


MAX_TOKENS = 512


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
    psychological_description = get_str_description(
        description=state.psychological_description.model_dump()
    )

    image_prompter = ImagePrompter()
    scene_image_prompter_output = await image_prompter.generate(
        agent_input=ImagePrompterInput(
            people_description=people_description,
            psychological_description=psychological_description,
            output_language="English",
        )
    )

    image_generation_prompt = (
        f"{conf['generation_prompt_header']}\n"
        f"People description: {people_description}\n"
        f"Scene description: {scene_image_prompter_output.scene_description}\n"
        f"{conf['generation_prompt_footer']}"
    )

    num_tokens = get_num_tokens(text=image_generation_prompt)
    if num_tokens > MAX_TOKENS:
        logger.warning(f"image_prompt_tokens: {num_tokens} > {MAX_TOKENS}")

    return {
        "image_generation_prompt": {
            "prompt": image_generation_prompt,
            "num_tokens": num_tokens,
        },
    }


image_prompter = Node(
    name="image_prompter",
    run=run,
)
