from multi_agents.graph import MultiAgentGraph

from .nodes import (
    idle_state,
    face_tracker,
    image_describer,
    psychological_describer,
    nietzsche_advisor,
    # ts_advisor,
    lm_advisor,
    creative_advisor,
    dc_selector,
    fc_selector,
    number_generator,
    image_prompter,
    image_generator,
    image_uploader,
    printer,
)

from .edges import (
    idle_state_face_tracker,
    face_tracker_image_describer,
    image_describer_psychological_describer,
    psychological_describer_nietzsche_advisor,
    # psychological_describer_ts_advisor,
    psychological_describer_lm_advisor,
    psychological_describer_creative_advisor,
    psychological_describer_dc_selector,
    psychological_describer_fc_selector,
    psychological_describer_number_generator,
    image_prompter_edges,
    image_prompter_image_generator,
    image_generator_image_uploader,
    image_uploader_printer,
)

from .schema import StateSchema, ConfigSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        idle_state,
        face_tracker,
        image_describer,
        psychological_describer,
        nietzsche_advisor,
        # ts_advisor,
        lm_advisor,
        creative_advisor,
        dc_selector,
        fc_selector,
        number_generator,
        image_prompter,
        image_generator,
        image_uploader,
        printer,
    ]

    edges = [
        idle_state_face_tracker,
        face_tracker_image_describer,
        image_describer_psychological_describer,
        psychological_describer_nietzsche_advisor,
        # psychological_describer_ts_advisor,
        psychological_describer_lm_advisor,
        psychological_describer_creative_advisor,
        psychological_describer_dc_selector,
        psychological_describer_fc_selector,
        psychological_describer_number_generator,
        image_prompter_edges,
        image_prompter_image_generator,
        image_generator_image_uploader,
        image_uploader_printer,
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
