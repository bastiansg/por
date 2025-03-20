from multi_agents.graph import MultiAgentGraph

from .nodes import face_tracker, image_describer
from .edges import face_tracker_image_describer

from .schema import StateSchema, ConfigSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        face_tracker,
        image_describer,
    ]

    edges = [
        face_tracker_image_describer,
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
