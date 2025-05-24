from multi_agents.graph import SimpleEdge


face_tracker_image_describer = SimpleEdge(
    source="face_tracker",
    target="image_describer",
)

face_tracker_psychological_describer = SimpleEdge(
    source="face_tracker",
    target="psychological_describer",
)

psychological_describer_nietzsche_advisor = SimpleEdge(
    source="psychological_describer",
    target="nietzsche_advisor",
)

psychological_describer_ts_advisor = SimpleEdge(
    source="psychological_describer",
    target="ts_advisor",
)

psychological_describer_jung_advisor = SimpleEdge(
    source="psychological_describer",
    target="jung_advisor",
)

psychological_describer_dc_selector = SimpleEdge(
    source="psychological_describer",
    target="dc_selector",
)

psychological_describer_fc_selector = SimpleEdge(
    source="psychological_describer",
    target="fc_selector",
)

psychological_describer_number_archetypes = SimpleEdge(
    source="psychological_describer",
    target="number_archetypes",
)

image_prompter_edges = SimpleEdge(
    source=[
        "image_describer",
        "dc_selector",
        "fc_selector",
        "jung_advisor",
        "nietzsche_advisor",
        "ts_advisor",
        "number_archetypes",
    ],
    target="image_prompter",
)

image_prompter_image_generator = SimpleEdge(
    source="image_prompter",
    target="image_generator",
)

image_generator_image_uploader = SimpleEdge(
    source="image_generator",
    target="image_uploader",
)

image_uploader_printer = SimpleEdge(
    source="image_uploader",
    target="printer",
)


printer_recovery = SimpleEdge(
    source="printer",
    target="recovery",
)
