# P.O.R. (Pop Oracle Robot)

P.O.R. is a machine oracle: you ask, it judges, consults its synthetic ghosts,
and prints an answer you probably should not trust.

## Components

The application is organized as a multi-agent workflow. It captures a
participant's input, analyzes it through specialized agents, retrieves relevant
material from a curated bibliography, generates a response, and sends the
result to the robot's output devices.

```text
┌─────────────────────────────────────────────────────────────────────┐
│  P.O.R. // ORACLE PIPELINE                                         │
└─────────────────────────────────────────────────────────────────────┘

 [ PARTICIPANT ]
        │
        │ voice + image
        ▼
 ┌─────────────────────┐
 │   INPUT CAPTURE     │
 │ CAMERA :: AUDIO     │
 └──────────┬──────────┘
            ▼
 ┌─────────────────────┐
 │ MULTI-AGENT GRAPH   │
 │ ROUTE :: COORDINATE │
 └──────────┬──────────┘
            │
      ┌─────┴──────────────┐
      ▼                    ▼
 ┌──────────────┐   ┌──────────────┐
 │  LLM AGENTS  │   │  RETRIEVAL   │
 │ ANALYZE      │   │ KNOWLEDGE    │
 └──────┬───────┘   └──────┬───────┘
        └──────────┬────────┘
                   ▼
          ┌─────────────────┐
          │ RESPONSE OUTPUT │
          │ THERMAL :: PRINT│
          └─────────────────┘
```

### [Application](src/por/app/app.py)

The application starts and continuously runs the oracle workflow, preserving
the resulting state for each interaction.

### [Multi-agent workflow](src/por/multi_agent)

The multi-agent workflow defines the processing stages, shared state, routing,
and transitions that coordinate an interaction from input to output.

```text
┌─────────────────────────────────────────────────────────────────────┐
│  P.O.R. // MULTI-AGENT GRAPH                                      │
└─────────────────────────────────────────────────────────────────────┘

 [ idle_state ]
        │
        ▼
 [ recorder ] ── failed ──► [ END ]
        │ accepted
        ▼
 [ audio_transcriber ]
        │
        ├──► [ language_detector ] ──► [ gatekeeper ] ──┐
        │                                                │
        └──► [ astrology_placements_extractor ] ─────────┤
                                                         ▼
                                            [ validation_checkpoint ]
                                                         │
                  ┌──────────────────────┴──────────────────────┐
                  │ rejected                                   │ accepted
                  ▼                                            │
             [ printer ]                                       ├── [ random_selector ] ──► [ printer ]
                                                               │
                                                               ├── [ image_describer ] ──┐
                                                               │                         ├──► [ image_generator ] ──► [ printer ]
                                                               └── [ psychological_describer ] ─┘
                                                                          │
                                                ┌─────────────┬───────────┼───────────┐
                                                ▼             ▼           ▼           ▼
                                      [ lyrics_advisor ] [ nietzsche_advisor ] [ astrology_advisor ] [ satc_advisor ]
                                                │             │           │           │
                                                └─────────────┴───────────┴───────────┴──► [ printer ]
```

### [LLM agents](src/por/llm_agents)

The LLM agents provide the specialized reasoning roles used to interpret the
participant and produce the different parts of the oracle response.

### [Retrieval](src/por/db)

The retrieval layer provides the agents with relevant material from a curated
bibliography.

### [Data loaders](src/por/loaders)

The data loaders prepare external material for the retrieval layer.

### [Hardware integration](src/por/multi_agent/nodes)

The hardware integration connects the workflow to the camera, microphone,
controls, display, and motion system.

### [Thermal printer](src/por/multi_agent/nodes/printer.py)

The thermal printer turns the generated oracle response into a physical receipt
for the participant.

## Package dependencies

P.O.R. delegates hardware control, agent orchestration, LLM integration, and
retrieval infrastructure to five project dependencies.

```text
┌─────────────────────────────────────────────────────────────────────┐
│  P.O.R. // PACKAGE DEPENDENCY MAP                                  │
└─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────┐
 │        P.O.R.       │
 │  ORACLE :: RUNTIME  │
 └──────────┬──────────┘
            │
            ├── HARDWARE :: PERCEPTION
            │      ├── hailo_apps
            │      └── sensehat_dsp
            │
            ├── AGENTS :: ORCHESTRATION
            │      ├── multi_agents
            │      └── llm_agents
            │
            └── KNOWLEDGE :: RETRIEVAL
                   └── rage
```

### [hailo_apps](https://github.com/bastiansg/hailo-apps)

Provides camera capture, Hailo-powered face detection, face tracking, and
pan-and-tilt control.

### [sensehat_dsp](https://github.com/bastiansg/sensehat-dsp)

Provides visual feedback through images and animations on the Raspberry Pi
Sense HAT display.

### [multi_agents](https://github.com/aureka-team/multi-agents)

Provides the graph, nodes, edges, routing, state, and execution model used to
coordinate the workflow.

### [llm_agents](https://github.com/aureka-team/llm-agents)

Provides the common interface used to define and run P.O.R.'s specialized
language-model agents.

### [rage](https://github.com/aureka-team/rage2)

Provides document loading, text processing, embeddings, indexing, and
retrieval for the curated bibliography used by the agents.

## Setup

### Qdrant

To run Qdrant on a Raspberry Pi 5, append `kernel=kernel8.img` to
`/boot/firmware/config.txt` and reboot. This changes the kernel page size to
4 KB.

### Static IP

```bash
nmcli device status
sudo nmtui edit "Wired connection 1"
```
