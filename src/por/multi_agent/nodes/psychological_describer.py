from typing import Any
from langgraph.runtime import get_runtime

from pydantic_ai import BinaryContent
from pydantic_extra_types.language_code import LanguageName

from multi_agents.graph import Node
from rich.console import Console

from por.multi_agent.schema import StateSchema, ContextSchema
from por.llm_agents import PsychologicalDescriber, PsychologicalDescriberDeps

from .utils import get_sensehat_dsp, get_dsp_images


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("runing psychological_describer...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    sensehat_dsp = get_sensehat_dsp()
    sensehat_dsp.stop()
    sensehat_dsp.clear()

    dsp_images = get_dsp_images()
    sensehat_dsp.start_image_sequence(
        images=[
            dsp_images["si-04a"],
            dsp_images["si-04b"],
        ],
        refresh_rate=0.5,
    )

    question = state.audio_transcription
    assert question is not None

    image_path = state.image_path
    assert image_path is not None

    psychological_describer_agent = PsychologicalDescriber()
    with open(image_path, "rb") as image_file:
        psychological_describer_output = await psychological_describer_agent.generate(
            user_prompt="Provide a psychological profile based on the provided information.",
            agent_deps=PsychologicalDescriberDeps(
                question=question,
                output_language=LanguageName("English"),
            ),
            user_content=BinaryContent(
                data=image_file.read(),
                media_type=f"image/{runtime_context.image_extension}",
            ),
        )

    sensehat_dsp.stop()
    sensehat_dsp.clear()
    sensehat_dsp.start_image_sequence(
        images=[
            dsp_images["si-05a"],
            dsp_images["si-05b"],
        ],
        refresh_rate=0.4,
    )

    return {
        "psychological_profile": psychological_describer_output,
    }


psychological_describer = Node(
    name="psychological_describer",
    run=run,
)
