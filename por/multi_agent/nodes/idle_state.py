from typing import Any
from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from rich.console import Console

from hailo_apps.servos import Servos, ServoAngles
from por.multi_agent.schema import StateSchema, ContextSchema

from .utils import get_sensehat_dsp, get_button, get_dsp_images


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    console.log("runing idle_state...")

    sensehat_dsp = get_sensehat_dsp()
    dsp_images = get_dsp_images()
    sensehat_dsp.start_image_sequence(
        images=[
            dsp_images["si-01a"],
            dsp_images["si-01b"],
        ],
        refresh_rate=0.5,
    )

    # sensehat_dsp.start_image_sequence(
    #     images=[
    #         dsp_images["08a"],
    #         dsp_images["08b"],
    #     ],
    #     refresh_rate=3.0,
    # )

    servos = Servos()
    idle_angles = runtime_context.idle_angles
    servos.set_angles(
        servo_angles=ServoAngles(
            x=idle_angles.x,
            y=idle_angles.y,
        )
    )

    button = get_button()
    button.wait_for_active()

    return {
        "button_is_active": True,
    }


idle_state = Node(
    name="idle_state",
    run=run,
    is_entry_point=True,
)
