import io
import base64

from typing import Any
from langgraph.runtime import get_runtime

from PIL import Image
from openai import AsyncOpenAI
from torchvision import transforms

from multi_agents.graph import Node
from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ContextSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing image_generator...")
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    image_extension = runtime_context.image_extension
    image_description = state.image_description
    assert image_description is not None

    image_generation_prompt = (
        runtime_context.image_generation_prompt_template.format(
            psychological_profile=state.psychological_profile,
            physical_description=image_description.physical_description,
            clothing_description=image_description.clothing_description,
        )
    )

    client = AsyncOpenAI()
    response = await client.responses.create(
        model="gpt-4o-mini",
        input=image_generation_prompt,
        tools=[
            {"type": "image_generation"},
        ],
    )

    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    image_base64 = image_data[0]
    assert image_base64 is not None

    io_bytes = io.BytesIO(base64.b64decode(image_base64))
    image = Image.open(io_bytes).convert("RGB")

    resize_transform = transforms.Resize(size=576)
    image = resize_transform(image)

    images_path = runtime_context.images_path
    gen_image_path = f"{images_path}/{state.image_id}-gen.{image_extension}"
    image.save(gen_image_path)

    return {
        "image_generation_prompt": image_generation_prompt,
        "gen_image_path": gen_image_path,
    }


image_generator = Node(
    name="image_generator",
    run=run,
)
