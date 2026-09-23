from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multi_agents.graph import MultiAgentGraph

    from .schema import ContextSchema


def get_multi_agent() -> "MultiAgentGraph":
    from .multi_agent import get_multi_agent as create_multi_agent

    return create_multi_agent()


def get_multi_agent_context(test_mode: bool = False) -> "ContextSchema":
    from .utils import get_multi_agent_context as create_multi_agent_context

    return create_multi_agent_context(test_mode=test_mode)
