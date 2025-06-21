# from langgraph.graph import END
from multi_agents.graph import SimpleEdge, ConditionalEdge

from .routers import gatekeeper_conditional_router


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

gatekeeper_edges = SimpleEdge(
    source=[
        "audio_transcriber",
        "image_describer",
    ],
    target="gatekeeper",
)

gatekeeper_conditional = ConditionalEdge(
    source="gatekeeper",
    intermediates=[
        "random_selector",
        "psychological_describer",
        "printer",
    ],
    router=gatekeeper_conditional_router,
)

psychological_describer_image_prompter = SimpleEdge(
    source="psychological_describer",
    target="image_prompter",
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

image_prompter_image_generator = SimpleEdge(
    source="image_prompter",
    target="image_generator",
)

printer_edges = SimpleEdge(
    source=[
        "random_selector",
        "creative_advisor",
        "nietzsche_advisor",
        "music_advisor",
        "image_generator",
    ],
    target="printer",
)
