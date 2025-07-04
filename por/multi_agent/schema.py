from io import BytesIO
from typing import Literal
from sensehat_dsp.display import Color
from common.utils.path import create_path

from hailo_apps.servos import ServoAngles
from hailo_apps.meta.interfaces import RotatorParams, ImageSize

from pydantic_extra_types.language_code import LanguageName
from pydantic import (
    BaseModel,
    ConfigDict,
    StrictStr,
    StrictBool,
    NonNegativeInt,
    NonNegativeFloat,
    PositiveInt,
    field_validator,
)

from por.loaders import ImageCaptionItem
from por.llm_agents.music_advisor import Song
from por.llm_agents.image_describer import ImageDescriberOutput


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


class ConfigSchema(BaseModel):
    servo_angles: ServoAngles
    rotator_params: RotatorParams
    image_size: ImageSize
    image_margin: NonNegativeInt
    image_description_guidelines: StrictStr
    history_length: NonNegativeInt
    face_detector_min_score: NonNegativeFloat
    images_path: StrictStr
    image_extension: StrictStr
    image_generation_model: StrictStr
    printer_name: StrictStr
    imagekit_url: StrictStr
    idle_angles: ServoAngles
    output_language: LanguageName
    dc_poems: list[DCPoem]
    fc_messages: list[FCMessage]
    printer: Printer
    train_image_captions: list[ImageCaptionItem]

    @field_validator("images_path", mode="after")
    def images_path_validator(cls, v: str) -> str:
        create_path(path=v)
        return v


class ImageGenerationPrompt(BaseModel):
    prompt: StrictStr
    num_tokens: PositiveInt


class StateSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    image_id: StrictStr
    audio_buffer: BytesIO | None = None
    image_path: StrictStr | None = None
    audio_transcription: StrictStr | None = None
    message_accepted: StrictBool | None = None
    rejection_reason: StrictStr | None = None
    image_description: ImageDescriberOutput | None = None
    psychological_profile: StrictStr | None = None
    nietzsche_text_chunks: list[StrictStr] = []
    nietzsche_advise: StrictStr | None = None
    selected_song: Song | None = None
    music_advice: StrictStr | None = None
    creative_capsule: StrictStr | None = None
    creative_advice: StrictStr | None = None
    selected_dc_poem: StrictStr | None = None
    selected_fc_message: StrictStr | None = None
    image_generation_prompt: ImageGenerationPrompt | None = None
    gen_image_path: StrictStr | None = None
    image_url: StrictStr | None = None
    ascii_image: list[StrictStr] = []
    lucky_number: PositiveInt | None = None
    print_status: Literal["ok", "failed"] | None = None
