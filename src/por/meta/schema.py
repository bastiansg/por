from pathlib import Path

from typing import Literal
from pydantic_extra_types.language_code import LanguageName
from pydantic import (
    BaseModel,
    StrictStr,
    Field,
    NonNegativeInt,
    model_validator,
    NonNegativeFloat,
)


class ChunkMetadata(BaseModel):
    title: StrictStr = Field(description="")
    artist: StrictStr | None = Field(
        description="",
        default=None,
    )

    author: StrictStr | None = Field(
        description="",
        default=None,
    )

    chunk_id: StrictStr = Field(
        description="A unique identifier for this text chunk within the collection."
    )

    previous_chunk_id: StrictStr | None = Field(
        description="The chunk_id of the preceding text chunk within the same collection.",
        default=None,
    )

    next_chunk_id: StrictStr | None = Field(
        description="The chunk_id of the following text chunk within the same collection.",
        default=None,
    )


class TextChunk(BaseModel):
    text: StrictStr = Field(description="The textual content of the chunk.")
    metadata: ChunkMetadata
    score: NonNegativeFloat | None = Field(
        default=None,
        description="The similarity score for this chunk.",
    )


class Material(BaseModel):
    name: StrictStr
    interaction: StrictStr
    description: StrictStr
    code: StrictStr


class FileMetadata(BaseModel):
    title: StrictStr | None = None
    extension: StrictStr | None = None
    collection: StrictStr
    language: LanguageName | None = None
    author: StrictStr | None = None


class FileItem(BaseModel):
    name: StrictStr
    metadata: FileMetadata

    @model_validator(mode="after")
    def set_extension(self):
        p = Path(self.name)
        self.metadata.extension = p.suffix

        return self


class Song(BaseModel):
    title: StrictStr = Field(
        description="Recommended song title.",
        min_length=1,
    )

    artist: StrictStr = Field(
        description="Artist of the recommended song.",
        min_length=1,
    )

    year: NonNegativeInt = Field(
        description="Release year of the recommended song.",
    )


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


ZodiacSign = Literal[
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]


JungianArchetype = Literal[
    "innocent",
    "sage",
    "explorer",
    "outlaw",
    "magician",
    "hero",
    "lover",
    "jester",
    "everyman",
    "caregiver",
    "ruler",
    "creator",
]


PsychologicalPresentation = Literal[
    "open",
    "guarded",
    "tense",
    "relaxed",
    "withdrawn",
    "expansive",
    "composed",
    "alert",
]


class AstrologyPlacements(BaseModel):
    sun: ZodiacSign | None = Field(
        default=None,
        description="The user's sun sign.",
    )

    rising: ZodiacSign | None = Field(
        default=None,
        description="The user's rising sign.",
    )

    moon: ZodiacSign | None = Field(
        default=None,
        description="The user's moon sign.",
    )


class PsychologicalProfile(BaseModel):
    presentation: PsychologicalPresentation = Field(
        description="Overall visible psychological presentation inferred from posture, expression, and gaze.",
    )

    emotional_tone: Literal[
        "hopeful",
        "anxious",
        "conflicted",
        "determined",
        "melancholic",
        "resigned",
        "yearning",
        "defiant",
        "curious",
        "numb",
        "calm",
        "playful",
    ] = Field(description="Dominant felt emotional state.")

    composure: Literal[
        "settled",
        "guarded",
        "fragile",
        "controlled",
        "restless",
        "overwhelmed",
        "dissociated",
        "focused",
    ] = Field(description="Emotional self-regulation capacity in this moment.")

    question_theme: Literal[
        "direction",
        "conflict",
        "desire",
        "identity",
        "fear",
        "purpose",
        "change",
        "belonging",
        "loss",
        "worthiness",
        "trust",
    ] = Field(description="Core existential concern behind the question.")

    core_need: Literal[
        "clarity",
        "safety",
        "connection",
        "recognition",
        "freedom",
        "meaning",
        "renewal",
    ] = Field(description="Primary psychological need implied by the question.")

    inner_conflict: Literal[
        "security_vs_growth",
        "control_vs_surrender",
        "belonging_vs_independence",
        "hope_vs_resignation",
        "desire_vs_fear",
        "duty_vs_authenticity",
        "certainty_vs_possibility",
        "visibility_vs_protection",
    ] = Field(description="Central internal tension shaping the profile.")

    jungian_archetype: JungianArchetype = Field(
        description=(
            "Dominant Jungian archetype reflected by the person's emotional stance, "
            "question theme, and inner conflict."
        ),
    )
