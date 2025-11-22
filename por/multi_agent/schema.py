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


class ContextSchema(BaseModel):
    servo_angles: ServoAngles
    rotator_params: RotatorParams
    image_size: ImageSize
    history_length: NonNegativeInt
    face_detector_min_score: NonNegativeFloat
    images_path: StrictStr
    image_extension: StrictStr
    idle_angles: ServoAngles
    dc_poems: list[DCPoem]
    fc_messages: list[FCMessage]
    printer: Printer

    @field_validator("images_path", mode="after")
    def images_path_validator(cls, v: str) -> str:
        create_path(path=v)
        return v


class SelectedSong(BaseModel):
    title: StrictStr
    artist: StrictStr
    lyrics: StrictStr


class StateSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    image_id: StrictStr
    audio_buffer: BytesIO | None = None
    image_path: StrictStr | None = None
    audio_transcription: StrictStr | None = None
    detected_language: LanguageName | None = None
    message_accepted: StrictBool | None = None
    rejection_reason: StrictStr | None = None
    image_description: ImageDescriberOutput | None = None
    psychological_profile: PsychologicalDescriberOutput | None = None
    nietzsche_advise: StrictStr | None = None
    nietzsche_text_chunks: list[StrictStr] = []
    music_advice: StrictStr | None = None
    selected_song: SelectedSong | None = None
    selected_dc_poem: StrictStr | None = None
    selected_fc_message: StrictStr | None = None
    image_generation_prompt: StrictStr | None = None
    gen_image_path: StrictStr | None = None
    lucky_number: PositiveInt | None = None
    print_status: Literal["ok", "failed"] | None = None
