import asyncio

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import ImagePrompter, ImagePrompterInput
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import (
    dry_mode_handler,
    get_str_person_description,
    get_sensehat_dsp,
)


logger = get_logger(__name__)


@dry_mode_handler(
    func_name="person_describer",
    return_fields=["image_prompt"],
)
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
        image_name="si-02",
        refresh_rate=0.25,
    )

    str_person_description = get_str_person_description(state=state)
    image_prompter = ImagePrompter()
    image_prompter_output = await image_prompter.generate(
        agent_input=ImagePrompterInput(
            image_description=state.image_description,
            person_description=str_person_description,
            nietzsche_advice=state.nietzsche_advise,
            jung_advice=state.jung_advise,
            ts_advice=state.taylor_swift_advise,
            output_language="English",
        )
    )

    image_generation_prompt = image_prompter_output.image_generation_prompt
    image_generation_prompt = f"{conf['generation_prompt_header']} {image_generation_prompt} {conf['generation_prompt_footer']}"
    return {
        "image_generation_prompt": image_generation_prompt,
    }


image_prompter = Node(
    name="image_prompter",
    run=run,
)
