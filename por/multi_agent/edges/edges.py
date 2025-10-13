from multi_agents.graph import SimpleEdge, ConditionalEdge

from .routers import validation_checkpoint_conditional_router


idle_state_face_tracker = SimpleEdge(
    source="idle_state",
    target="face_tracker",
)

idle_state_recorder = SimpleEdge(
    source="idle_state",
    target="recorder",
)

recorder_audio_transcriber = SimpleEdge(
    source="recorder",
    target="audio_transcriber",
)

recorder_image_describer = SimpleEdge(
    source="recorder",
    target="image_describer",
)

audio_transcriber_language_detector = SimpleEdge(
    source="audio_transcriber",
    target="language_detector",
)

language_detector_gatekeeper = SimpleEdge(
    source="language_detector",
    target="gatekeeper",
)

validation_checkpoint_edges = SimpleEdge(
    source=[
        "gatekeeper",
        "image_describer",
    ],
    target="validation_checkpoint",
)

validation_checkpoint_conditional = ConditionalEdge(
    source="validation_checkpoint",
    intermediates=[
        "random_selector",
        "psychological_describer",
        "printer",
    ],
    router=validation_checkpoint_conditional_router,
)

psychological_describer_nietzsche_advisor = SimpleEdge(
    source="psychological_describer",
    target="nietzsche_advisor",
)

psychological_describer_creative_advisor = SimpleEdge(
    source="psychological_describer",
    target="creative_advisor",
)

psychological_describer_music_advisor = SimpleEdge(
    source="psychological_describer",
    target="music_advisor",
)

psychological_describer_image_generator = SimpleEdge(
    source="psychological_describer",
    target="image_generator",
)

printer_edges = SimpleEdge(
    source=[
        "creative_advisor",
        "nietzsche_advisor",
        "music_advisor",
        "random_selector",
        "image_generator",
    ],
    target="printer",
)
