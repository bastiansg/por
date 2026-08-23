import os
from io import BytesIO
from typing import Literal

from hailo_apps.meta.interfaces import ImageSize, RotatorParams
from hailo_apps.servos import ServoAngles
from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    StrictBool,
    StrictInt,
    StrictStr,
    field_validator,
)
from pydantic_extra_types.language_code import LanguageName
from sensehat_dsp.display import Color

from por.llm_agents.schema import PBFImageDescriberOutput
from por.meta.schema import (
    AstrologyPlacements,
    PsychologicalProfile,
    Song,
    TextChunk,
)


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
    capture_size: ImageSize
    final_capture_y_angle_offset: StrictInt
    history_length: NonNegativeInt
    face_detector_min_score: NonNegativeFloat
    images_path: StrictStr
    input_image_extension: StrictStr
    generated_image_extension: StrictStr
    caption_header: StrictStr
    replicate_model: StrictStr
    replicate_timeout: PositiveFloat
    idle_angles: ServoAngles
    dc_poems: list[DCPoem]
    fc_messages: list[FCMessage]
    printer: Printer
    test_mode: StrictBool

    @field_validator("images_path", mode="after")
    def images_path_validator(cls, v: str) -> str:
        os.makedirs(v, exist_ok=True)
        return v


class SelectedSong(BaseModel):
    title: StrictStr
    artist: StrictStr
    lyrics: StrictStr


class StateSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    invoked_at: StrictStr | None = None
    button_is_active: StrictBool = False
    image_id: StrictStr
    audio_buffer: BytesIO | None = None
    image_path: StrictStr | None = None
    recorder_ok: StrictBool = False
    audio_transcription: StrictStr | None = None
    detected_language: LanguageName | None = None
    astrology_placements: AstrologyPlacements | None = None
    message_accepted: StrictBool | None = None
    rejection_reason: StrictStr | None = None
    image_description: PBFImageDescriberOutput | None = None
    psychological_profile: PsychologicalProfile | None = None
    nietzsche_advise: StrictStr | None = None
    nietzsche_text_chunks: list[TextChunk] = []
    astrology_advice: StrictStr | None = None
    astrology_text_chunks: list[TextChunk] = []
    satc_advice: StrictStr | None = None
    satc_text_chunks: list[TextChunk] = []
    song: Song | None = None
    lyrics_advise: StrictStr | None = None
    lyrics_text_chunks: list[TextChunk] = []
    selected_dc_poem: StrictStr | None = None
    selected_fc_message: StrictStr | None = None
    image_generation_prompt: StrictStr | None = None
    gen_image_path: StrictStr | None = None
    lucky_number: PositiveInt | None = None
    print_status: Literal["ok", "failed"] | None = None
