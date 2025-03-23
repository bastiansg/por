from multi_agents.graph import SimpleEdge


face_tracker_image_describer = SimpleEdge(
    source="face_tracker",
    target="image_describer",
)


image_describer_image_generator = SimpleEdge(
    source="image_describer",
    target="image_generator",
)

image_generator_image_uploader = SimpleEdge(
    source="image_generator",
    target="image_uploader",
)

image_uploader_qr_generator = SimpleEdge(
    source="image_uploader",
    target="qr_generator",
)

qr_generator_printer = SimpleEdge(
    source="qr_generator",
    target="printer",
)

printer_recovery = SimpleEdge(
    source="printer",
    target="recovery",
)
