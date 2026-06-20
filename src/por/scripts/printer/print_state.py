import argparse
from pathlib import Path

from por.multi_agent.config import MultiAgentConfig
from por.multi_agent.nodes.printer import main_pipeline, rejection_pipeline
from por.multi_agent.nodes.utils import get_printer
from por.multi_agent.schema import StateSchema
from por.utils.json import load_json


STATES_PATH = Path("/resources/states")


def print_state(state_file: str) -> None:
    state_path = STATES_PATH / state_file
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
    parser = argparse.ArgumentParser(description="Print a stored oracle state.")
    parser.add_argument(
        "--state-file",
        required=True,
        help="State JSON filename.",
    )
    args = parser.parse_args()

    print_state(state_file=args.state_file)


if __name__ == "__main__":
    main()
