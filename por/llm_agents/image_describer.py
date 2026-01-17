from pydantic_ai import ToolOutput
from pydantic import BaseModel, StrictStr, Field

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent


class PhysicalDescription(BaseModel):
    gender_presentation: StrictStr = Field(
        description="Apparent gender presentation based only on visible style cues.",
        min_length=1,
    )

    body_proportions: StrictStr = Field(
        description="Visible overall body proportions or build (e.g., slim, broad, petite).",
        min_length=1,
    )

    hairstyle: StrictStr = Field(
        description="Visible hairstyle: length, texture, styling, color.",
        min_length=1,
    )

    facial_features: StrictStr = Field(
        description="Visible facial details: expression category, makeup, piercings, tattoos, or notable features.",
        min_length=1,
    )

    visible_modifications: StrictStr = Field(
        description="Visible body modifications such as tattoos, piercings, or cosmetic enhancements.",
        min_length=1,
    )


class ClothingDescription(BaseModel):
    main_garments: StrictStr = Field(
        description="Primary clothing items: type, fit, silhouette, and notable design details.",
        min_length=1,
    )

    layering: StrictStr = Field(
        description="Description of visible layers (jackets, overshirts, sweaters, etc.).",
        min_length=1,
    )

    fabric_and_texture: StrictStr = Field(
        description="Visible fabric characteristics: texture, material impression, structure.",
        min_length=1,
    )

    patterns_and_details: StrictStr = Field(
        description="Patterns, prints, trims, collars, buttons, stitching, or unique design motifs.",
        min_length=1,
    )

    accessories: StrictStr = Field(
        description="Fashion accessories: jewelry, hats, eyewear, belts, bags (excluding any microphones or cables).",
        min_length=1,
    )

    footwear: StrictStr = Field(
        description="Visible footwear: type, style, silhouette, and notable details.",
        min_length=1,
    )


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
        conf_path=f"{llm_agents.__path__[0]}/image-describer.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=ToolOutput(ImageDescriberOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
