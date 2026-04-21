from langgraph.graph import END
from multi_agents.graph import SimpleEdge, ConditionalEdge

from .routers import (
    validation_checkpoint_conditional_router,
    recorder_conditional_router,
)


idle_state_face_tracker = SimpleEdge(
    source="idle_state",
    target="face_tracker",
)

idle_state_recorder = SimpleEdge(
    source="idle_state",
    target="recorder",
)

recorder_conditional = ConditionalEdge(
    source="recorder",
    intermediates=[
        "audio_transcriber",
        END,
    ],
    router=recorder_conditional_router,
)

audio_transcriber_language_detector = SimpleEdge(
    source="audio_transcriber",
    target="language_detector",
)

audio_transcriber_astrology_placements_extractor = SimpleEdge(
    source="audio_transcriber",
    target="astrology_placements_extractor",
)

language_detector_gatekeeper = SimpleEdge(
    source="language_detector",
    target="gatekeeper",
)

validation_checkpoint_edges = SimpleEdge(
    source=[
        "gatekeeper",
        "astrology_placements_extractor",
    ],
    target="validation_checkpoint",
)

validation_checkpoint_conditional = ConditionalEdge(
    source="validation_checkpoint",
    intermediates=[
        "random_selector",
        "image_describer",
        "psychological_describer",
        "printer",
    ],
    router=validation_checkpoint_conditional_router,
)

psychological_describer_lyrics_advisor = SimpleEdge(
    source="psychological_describer",
    target="lyrics_advisor",
)

psychological_describer_nietzsche_advisor = SimpleEdge(
    source="psychological_describer",
    target="nietzsche_advisor",
)

psychological_describer_astrology_advisor = SimpleEdge(
    source="psychological_describer",
    target="astrology_advisor",
)

psychological_describer_satc_advisor = SimpleEdge(
    source="psychological_describer",
    target="satc_advisor",
)

image_prompter_image_generator = SimpleEdge(
    source=[
        "image_describer",
        "psychological_describer",
    ],
    target="image_generator",
)

printer_edges = SimpleEdge(
    source=[
        "lyrics_advisor",
        "nietzsche_advisor",
        "astrology_advisor",
        "random_selector",
        "satc_advisor",
        "image_generator",
    ],
    target="printer",
)
