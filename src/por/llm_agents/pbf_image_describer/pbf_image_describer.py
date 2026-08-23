from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictStr
from pydantic_ai import Agent, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings


class PeopleDescription(BaseModel):
    general_description: StrictStr = Field(
        description="Very brief general description of the people in the image.",
        min_length=1,
    )

    pose_and_posture: StrictStr = Field(
        description="Visible poses, posture, limb placement, and interactions.",
        min_length=1,
    )

    body_proportions: StrictStr = Field(
        description="Visible overall body proportions and builds.",
        min_length=1,
    )

    silhouette_shape: StrictStr = Field(
        description="Overall silhouettes formed by the people and their clothing.",
        min_length=1,
    )

    facial_expression: StrictStr | None = Field(
        description="Visible facial expressions and facial characteristics.",
        default=None,
        min_length=1,
    )

    hair_style: StrictStr | None = Field(
        description="Visible hair lengths, textures, and styling.",
        default=None,
        min_length=1,
    )

    visible_modifications: StrictStr | None = Field(
        description="Visible tattoos, piercings, makeup, or cosmetic enhancements.",
        default=None,
        min_length=1,
    )


class ClothingDescription(BaseModel):
    main_garments: StrictStr = Field(
        description="Primary garments, including type, fit, silhouette, and design details.",
        min_length=1,
    )

    layering: StrictStr | None = Field(
        description="Visible garment layers and how they overlap.",
        default=None,
        min_length=1,
    )

    fabric_and_texture: StrictStr | None = Field(
        description="Visible fabric texture, material impression, weight, and structure.",
        default=None,
        min_length=1,
    )

    patterns_and_details: StrictStr | None = Field(
        description="Visible patterns, trims, collars, fastenings, stitching, and motifs.",
        default=None,
        min_length=1,
    )

    accessories: StrictStr | None = Field(
        description="Visible jewelry, hats, eyewear, belts, bags, and other wearable accessories.",
        default=None,
        min_length=1,
    )

    footwear: StrictStr | None = Field(
        description="Visible footwear type, style, silhouette, and notable details.",
        default=None,
        min_length=1,
    )


class SceneDescription(BaseModel):
    setting_and_background: StrictStr = Field(
        description=(
            "Visible environment, location type, background structures, "
            "and environmental details."
        ),
        min_length=1,
    )

    composition: StrictStr = Field(
        description=(
            "Framing, viewpoint, subject placement, and spatial arrangement."
        ),
        min_length=1,
    )

    objects: StrictStr = Field(
        description="Important visible objects and their positions.",
        min_length=1,
    )


class PBFImageDescriberOutput(BaseModel):
    scene_description: SceneDescription = Field(
        description="Scene, composition, and objects visible in the image.",
    )

    people_description: PeopleDescription = Field(
        description="Physical description of one or more people in the image.",
    )

    clothing_description: ClothingDescription = Field(
        description="Clothing and accessory description of the people in the image.",
    )


agent = Agent(
    name="pbf-image-describer",
    model="gpt-5.6-sol",
    model_settings=OpenAIChatModelSettings(
        max_tokens=512,
        openai_reasoning_effort="none",
    ),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    output_type=ToolOutput(PBFImageDescriberOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class PBFImageDescriber(LLMAgent[None, PBFImageDescriberOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
