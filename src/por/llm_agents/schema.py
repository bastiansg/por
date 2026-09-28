from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, BeforeValidator, Field, StrictStr


def _none_substring_to_none(value: object) -> object:
    if isinstance(value, str) and "none" in value.casefold():
        return None

    return value


_OptionalDescription = Annotated[
    StrictStr | None,
    BeforeValidator(_none_substring_to_none),
]


class PeopleDescription(BaseModel):
    general_description: StrictStr = Field(
        description="Very brief general description of the people in the image.",
        min_length=1,
    )

    gender_presentation: StrictStr = Field(
        description="Visible gender presentation.",
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

    facial_expression: _OptionalDescription = Field(
        description=(
            "Visible facial expressions and facial characteristics. "
            "Must be None if not visible."
        ),
        default=None,
    )

    hair_style: _OptionalDescription = Field(
        description=(
            "Visible hair lengths, textures, and styling. Must be None if not visible."
        ),
        default=None,
    )

    visible_modifications: _OptionalDescription = Field(
        description=(
            "Visible tattoos, piercings, makeup, or cosmetic enhancements. "
            "Must be None if not visible."
        ),
        default=None,
    )


class ClothingDescription(BaseModel):
    main_garments: StrictStr = Field(
        description="Primary garments, including type, fit, silhouette, and design details.",
        min_length=1,
    )

    layering: _OptionalDescription = Field(
        description=(
            "Visible garment layers and how they overlap. Must be None if not visible."
        ),
        default=None,
    )

    fabric_and_texture: _OptionalDescription = Field(
        description=(
            "Visible fabric texture, material impression, weight, and structure. "
            "Must be None if not visible."
        ),
        default=None,
    )

    patterns_and_details: _OptionalDescription = Field(
        description=(
            "Visible patterns, trims, collars, fastenings, stitching, and motifs. "
            "Must be None if not visible."
        ),
        default=None,
    )

    accessories: _OptionalDescription = Field(
        description=(
            "Visible jewelry, hats, eyewear, belts, bags, and other wearable accessories. "
            "Must be None if not visible."
        ),
        default=None,
    )

    footwear: _OptionalDescription = Field(
        description=(
            "Visible footwear type, style, silhouette, and notable details. "
            "Must be None if not visible."
        ),
        default=None,
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


SceneDescriptionT = TypeVar("SceneDescriptionT", bound=SceneDescription)


class ImageDescriptionOutput(BaseModel, Generic[SceneDescriptionT]):
    scene_description: SceneDescriptionT = Field(
        description="Scene, composition, and objects visible in the image.",
    )

    people_description: PeopleDescription = Field(
        description="Physical description of one or more people in the image.",
    )

    clothing_description: ClothingDescription = Field(
        description="Clothing and accessory description of the people in the image.",
    )
