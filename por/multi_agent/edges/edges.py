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

language_detector_gatekeeper = SimpleEdge(
    source="language_detector",
    target="gatekeeper",
)

gatekeeper_validation_checkpoint = SimpleEdge(
    source="gatekeeper",
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

psychological_describer_matter_advisor = SimpleEdge(
    source="psychological_describer",
    target="matter_advisor",
)

image_prompter_edges = SimpleEdge(
    source=[
        "image_describer",
        "psychological_describer",
    ],
    target="image_prompter",
)

image_prompter_image_generator = SimpleEdge(
    source="image_prompter",
    target="image_generator",
)

printer_edges = SimpleEdge(
    source=[
        "matter_advisor",
        "random_selector",
        "image_generator",
    ],
    target="printer",
)
