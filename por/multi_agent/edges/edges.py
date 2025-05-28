from multi_agents.graph import SimpleEdge

idle_state_face_tracker = SimpleEdge(
    source="idle_state",
    target="face_tracker",
)

face_tracker_image_describer = SimpleEdge(
    source="face_tracker",
    target="image_describer",
)

image_describer_psychological_describer = SimpleEdge(
    source="image_describer",
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

psychological_describer_lm_advisor = SimpleEdge(
    source="psychological_describer",
    target="lm_advisor",
)

psychological_describer_creative_advisor = SimpleEdge(
    source="psychological_describer",
    target="creative_advisor",
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
        "dc_selector",
        "fc_selector",
        "creative_advisor",
        "nietzsche_advisor",
        # "ts_advisor",
        "lm_advisor",
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
