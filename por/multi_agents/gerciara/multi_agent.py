from multi_agents.graph import MultiAgentGraph

from .nodes import (
    face_tracker,
    image_describer,
    person_describer,
    nietzsche_advisor,
    ts_advisor,
    jung_advisor,
    dc_selector,
    fc_selector,
    number_archetypes,
    image_prompter,
    image_generator,
    image_uploader,
    printer,
    recovery,
)

from .edges import (
    face_tracker_image_describer,
    face_tracker_person_describer,
    person_describer_nietzsche_advisor,
    person_describer_ts_advisor,
    person_describer_jung_advisor,
    person_describer_dc_selector,
    person_describer_fc_selector,
    person_describer_number_archetypes,
    image_prompter_edges,
    image_prompter_image_generator,
    image_generator_image_uploader,
    image_uploader_printer,
    printer_recovery,
)

from .schema import StateSchema, ConfigSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        face_tracker,
        image_describer,
        person_describer,
        nietzsche_advisor,
        ts_advisor,
        jung_advisor,
        dc_selector,
        fc_selector,
        number_archetypes,
        image_prompter,
        image_generator,
        image_uploader,
        printer,
        recovery,
    ]

    edges = [
        face_tracker_image_describer,
        face_tracker_person_describer,
        person_describer_nietzsche_advisor,
        person_describer_ts_advisor,
        person_describer_jung_advisor,
        person_describer_dc_selector,
        person_describer_fc_selector,
        person_describer_number_archetypes,
        image_prompter_edges,
        image_prompter_image_generator,
        image_generator_image_uploader,
        image_uploader_printer,
        printer_recovery,
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
