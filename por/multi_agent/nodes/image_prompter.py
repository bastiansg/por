from typing import Any
# from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents import ImagePrompter, ImagePrompterDeps
# from por.multi_agent.schema import StateSchema, ContextSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    # runtime = get_runtime(ContextSchema)
    # runtime_context = runtime.context

    # if runtime_context.test_mode:
    #     return {}

    logger.info("runing image_prompter...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    psychological_profile = state.psychological_profile
    assert psychological_profile is not None

    image_description = state.image_description
    assert image_description is not None

    ip = ImagePrompter()
    ip_output = await ip.generate(
        user_prompt="Provide your surreal Flux image-generation prompt.",
        agent_deps=ImagePrompterDeps(
            question=audio_transcription,
            psychological_profile=psychological_profile,
            physical_description=image_description.physical_description,
            clothing_description=image_description.clothing_description,
        ),
    )

    return {
        "image_generation_prompt": ip_output.flux_prompt,
    }


image_prompter = Node(
    name="image_prompter",
    run=run,
)
