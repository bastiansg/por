from pydantic_ai import NativeOutput
from pydantic import BaseModel, StrictStr, Field

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import image_describer


class FacialFeatures(BaseModel):
    face_shape: StrictStr = Field(
        description="Visible face shape.",
        min_length=1,
    )

    eyes: StrictStr = Field(
        description="Visible eye characteristics only, excluding gaze direction.",
        min_length=1,
    )

    jawline: StrictStr = Field(
        description="Visible jawline characteristics.",
        min_length=1,
    )

    nose: StrictStr = Field(
        description="Visible nose characteristics.",
        min_length=1,
    )

    lips: StrictStr = Field(
        description="Visible lip characteristics.",
        min_length=1,
    )

    beard: StrictStr | None = Field(
        description="Visible beard characteristics.",
        min_length=1,
    )

    mustache: StrictStr | None = Field(
        description="Visible mustache characteristics.",
        min_length=1,
    )

    brows: StrictStr = Field(
        description="Visible eyebrow characteristics.",
        min_length=1,
    )

    cheekbones: StrictStr = Field(
        description="Visible cheekbone characteristics.",
        min_length=1,
    )

    chin: StrictStr = Field(
        description="Visible chin characteristics.",
        min_length=1,
    )


class Hairstyle(BaseModel):
    length: StrictStr = Field(
        description="Visible hair length.",
        min_length=1,
    )

    texture: StrictStr = Field(
        description="Visible hair texture.",
        min_length=1,
    )

    styling: StrictStr = Field(
        description="Visible hair styling.",
        min_length=1,
    )

    color: StrictStr = Field(
        description="Visible hair color.",
        min_length=1,
    )


class PhysicalDescription(BaseModel):
    gender_presentation: StrictStr = Field(
        description="Apparent gender presentation based only on visible style cues.",
        min_length=1,
    )

    body_proportions: StrictStr = Field(
        description=(
            "Visible overall body proportions or build ("
            "e.g., slim, lean, average, broad, broad-framed, narrow-framed, petite, "
            "curvy, athletic, muscular, plus-size, stocky"
            ")."
        ),
        min_length=1,
    )

    silhouette_shape: StrictStr = Field(
        description="Overall silhouette impression from body and clothing (e.g., boxy, A-line, column, triangular, elongated).",
        min_length=1,
    )

    hairstyle: Hairstyle
    facial_features: FacialFeatures
    visible_modifications: StrictStr = Field(
        description="Visible body modifications such as tattoos, piercings, makeup, or cosmetic enhancements.",
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
        description="Fashion accessories: jewelry, hats, eyewear, belts, bags.",
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
        conf_path=f"{image_describer.__path__[0]}/image-describer.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=NativeOutput(ImageDescriberOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
