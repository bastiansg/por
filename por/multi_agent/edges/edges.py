from multi_agents.graph import SimpleEdge


face_tracker_image_describer = SimpleEdge(
    source="face_tracker",
    target="image_describer",
)

face_tracker_person_describer = SimpleEdge(
    source="face_tracker",
    target="person_describer",
)

person_describer_nietzsche_advisor = SimpleEdge(
    source="person_describer",
    target="nietzsche_advisor",
)

person_describer_ts_advisor = SimpleEdge(
    source="person_describer",
    target="ts_advisor",
)

person_describer_jung_advisor = SimpleEdge(
    source="person_describer",
    target="jung_advisor",
)

person_describer_dc_selector = SimpleEdge(
    source="person_describer",
    target="dc_selector",
)

person_describer_fc_selector = SimpleEdge(
    source="person_describer",
    target="fc_selector",
)

image_prompter_edges = SimpleEdge(
    source=[
        "image_describer",
        "dc_selector",
        "fc_selector",
        "jung_advisor",
        "nietzsche_advisor",
        "ts_advisor",
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
