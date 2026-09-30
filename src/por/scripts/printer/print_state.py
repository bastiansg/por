from pathlib import Path

from por.multi_agent.config import MultiAgentConfig
from por.multi_agent.nodes.printer import main_pipeline, rejection_pipeline
from por.multi_agent.nodes.utils import get_printer
from por.multi_agent.schema import StateSchema
from por.utils.json import load_json

STATES_PATH = Path("/resources/states")
STATE_FILE = "2026-09-30T00:37:47.310267+00:00-b355f5870283420bb952831eb7c0eb6c.json"


def print_state() -> None:
    state_path = STATES_PATH / STATE_FILE
    state = StateSchema.model_validate(load_json(str(state_path)))
    printer = get_printer()
    por_logo_path = MultiAgentConfig().printer.por_logo_path

    if state.message_accepted:
        main_pipeline(
            printer=printer,
            por_logo_path=por_logo_path,
            state=state,
        )

    else:
        rejection_pipeline(
            printer=printer,
            por_logo_path=por_logo_path,
            state=state,
        )


def main() -> None:
    print_state()


if __name__ == "__main__":
    main()
