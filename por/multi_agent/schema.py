from typing import Literal
from sensehat_dsp.display import Color
from common.utils.path import create_path

from hailo_apps.servos import ServoAngles
from hailo_apps.meta.interfaces import RotatorParams, ImageSize

from pydantic_extra_types.language_code import LanguageName
from pydantic import (
    BaseModel,
    StrictStr,
    NonNegativeInt,
    NonNegativeFloat,
    PositiveFloat,
    PositiveInt,
    field_validator,
)

from por.loaders import ImageCaptionItem
from por.llm_agents.image_describer import ImageDescriberOutput
from por.llm_agents.psychological_describer import PsychologicalDescriberOutput


class GolColors(BaseModel):
    p_color: Color
    s_color: Color


class DCPoem(BaseModel):
    poem_id: NonNegativeInt
    poem: StrictStr


class FCMessage(BaseModel):
    message_id: NonNegativeInt
    message: StrictStr


class Printer(BaseModel):
    por_logo_path: StrictStr
    max_text_len: PositiveInt


class NumberArchetype(BaseModel):
    number: NonNegativeInt
    archetype_name: StrictStr
    traits: list[StrictStr]


class ConfigSchema(BaseModel):
    servo_angles: ServoAngles
    rotator_params: RotatorParams
    min_delta_avg: PositiveFloat
    image_size: ImageSize
    image_margin: NonNegativeInt
    image_description_guidelines: StrictStr
    history_length: NonNegativeInt
    face_detector_min_score: NonNegativeFloat
    images_path: StrictStr
    image_extension: StrictStr
    model: StrictStr
    generation_prompt_header: StrictStr
    generation_prompt_footer: StrictStr
    printer_name: StrictStr
    imagekit_url: StrictStr
    idle_angles: ServoAngles
    recovery_time: NonNegativeFloat
    output_language: LanguageName
    dc_poems: list[DCPoem]
    fc_messages: list[FCMessage]
    printer: Printer
    number_archetypes: list[NumberArchetype]
    train_image_captions: list[ImageCaptionItem]

    @field_validator("images_path", mode="after")
    def images_path_validator(cls, v: str) -> str:
        create_path(path=v)
        return v


class ImageGenerationPrompt(BaseModel):
    prompt: StrictStr
    num_tokens: PositiveInt


class StateSchema(BaseModel):
    image_id: StrictStr
    image_path: StrictStr | None = None
    image_description: ImageDescriberOutput | None = None
    psychological_description: PsychologicalDescriberOutput | None = None
    nietzsche_text_chunks: list[StrictStr] = []
    nietzsche_advise: StrictStr | None = None
    ts_text_chunks: list[StrictStr] = []
    taylor_swift_advise: StrictStr | None = None
    creativity_text_chunks: list[StrictStr] = []
    creativity_advice: StrictStr | None = None
    selected_dc_poem: StrictStr | None = None
    selected_fc_message: StrictStr | None = None
    image_generation_prompt: ImageGenerationPrompt | None = None
    gen_image_path: StrictStr | None = None
    image_url: StrictStr | None = None
    lucky_number: NonNegativeInt | None = None
    print_status: Literal["ok", "failed"] | None = None
