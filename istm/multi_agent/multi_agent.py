from multi_agents.graph import MultiAgentGraph

from .nodes import (
    face_tracker,
    image_describer,
    image_generator,
    image_uploader,
    qr_generator,
    printer,
    recovery,
)

from .edges import (
    face_tracker_image_describer,
    image_describer_image_generator,
    image_generator_image_uploader,
    image_uploader_qr_generator,
    qr_generator_printer,
    printer_recovery,
    recovery_face_tracker,
)

from .schema import StateSchema, ConfigSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        face_tracker,
        image_describer,
        image_generator,
        image_uploader,
        qr_generator,
        printer,
        recovery,
    ]

    edges = [
        face_tracker_image_describer,
        image_describer_image_generator,
        image_generator_image_uploader,
        image_uploader_qr_generator,
        qr_generator_printer,
        printer_recovery,
        recovery_face_tracker,
    ]

    multi_agent = MultiAgentGraph(
        state_schema=StateSchema,
        config_schema=ConfigSchema,
        nodes=nodes,
        edges=edges,
        with_memory=False,
    )

    multi_agent.compile()
    return multi_agent
