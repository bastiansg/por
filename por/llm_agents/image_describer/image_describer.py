from pydantic_ai import NativeOutput
from pydantic import BaseModel, Field

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import image_describer
from por.meta.schema import PhysicalDescription, ClothingDescription


class ImageDescriberOutput(BaseModel):
    physical_description: PhysicalDescription = Field(
        description="Physical description of the people in the provided image.",
    )

    clothing_description: ClothingDescription = Field(
        description="Clothing and accessory description of the people in the provided image.",
    )


class ImageDescriber(LLMAgent[None, ImageDescriberOutput]):
    def __init__(
        self,
        conf_path=f"{image_describer.__path__[0]}/image-describer.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=NativeOutput(ImageDescriberOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
