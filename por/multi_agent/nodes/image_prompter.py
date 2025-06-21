import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.utils.tokens import get_num_tokens
from por.llm_agents import ImagePrompter, ImagePrompterInput
from por.multi_agent.schema import StateSchema, ConfigSchema

from .utils import get_sensehat_dsp


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

    image_prompter = ImagePrompter()
    image_prompter_output = await image_prompter.generate(
        agent_input=ImagePrompterInput(
            question=state.audio_transcription,
            psychological_profile=state.psychological_profile,
            physical_description=state.image_description.physical_description,
            clothing_description=state.image_description.clothing_description,
            output_language="English",
        )
    )

    prompt = image_prompter_output.image_generation_prompt
    num_tokens = get_num_tokens(text=prompt)
    if num_tokens > MAX_TOKENS:
        logger.warning(f"image_prompt_tokens: {num_tokens} > {MAX_TOKENS}")

    return {
        "image_generation_prompt": {
            "prompt": prompt,
            "num_tokens": num_tokens,
        },
    }


image_prompter = Node(
    name="image_prompter",
    run=run,
)
