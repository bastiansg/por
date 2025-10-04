from typing import Any
from langgraph.runtime import get_runtime

from pydantic_ai import BinaryContent

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import ImageDescriber
from por.multi_agent.schema import StateSchema, ContextSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing image_describer...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    image_path = state.image_path
    assert image_path is not None

    image_describer_agent = ImageDescriber()
    with open(image_path, "rb") as image_file:
        image_describer_output = await image_describer_agent.generate(
            user_prompt=runtime_context.image_description_guidelines,
            user_content=BinaryContent(
                data=image_file.read(),
                media_type=f"image/{runtime_context.image_extension}",
            ),
        )

    return {
        "image_description": image_describer_output,
    }


image_describer = Node(
    name="image_describer",
    run=run,
)
