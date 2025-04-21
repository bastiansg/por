import tiktoken

from sensehat_dsp.display import Color
from common.utils.path import create_path

from hailo_apps.servos import ServoAngles
from hailo_apps.meta.interfaces import RotatorParams, ImageSize

from pydantic_extra_types.language_code import LanguageName
from pydantic import (
    BaseModel,
    StrictStr,
    FilePath,
    NonNegativeInt,
    NonNegativeFloat,
    StrictBool,
    HttpUrl,
    field_validator,
)


tiktoken_encoder = tiktoken.encoding_for_model("gpt-4o")


class GolColors(BaseModel):
    p_color: Color
    s_color: Color


class DCPoem(BaseModel):
    poem_id: NonNegativeInt
    poem: StrictStr


class FCMessage(BaseModel):
    message_id: NonNegativeInt
    message: StrictStr


class ConfigSchema(BaseModel):
    servo_angles: ServoAngles
    rotator_params: RotatorParams
    image_size: ImageSize
    image_margin: NonNegativeInt
    image_description_guidelines: StrictStr
    person_description_guidelines: StrictStr
    history_length: NonNegativeInt
    min_score: NonNegativeFloat
    images_path: StrictStr
    image_extension: StrictStr
    model: StrictStr
    generation_prompt_header: StrictStr
    generation_prompt_footer: StrictStr
    printer_name: StrictStr
    imagekit_url_endpoint: StrictStr
    idle_angles: ServoAngles
    gol_colors: GolColors
    recovery_time: NonNegativeFloat
    output_language: LanguageName
    dc_poems: list[DCPoem]
    fc_messages: list[FCMessage]
    print_wait_time: NonNegativeInt
    dry_mode: StrictBool = False
    dry_mode_wait: NonNegativeInt = 5

    @field_validator("images_path", mode="after")
    def images_path_validator(cls, v: str) -> str:
        create_path(path=v)
        return v


class ConcatImage(BaseModel):
    image_path: FilePath
    width: NonNegativeInt
    height: NonNegativeInt


class PersonDescription(BaseModel):
    fears: StrictStr
    dreams_and_desires: StrictStr
    love_status: StrictStr
    lucky_number: StrictStr


class StateSchema(BaseModel):
    image_id: StrictStr
    image_path: FilePath | None = None
    image_description: StrictStr | None = None
    person_description: PersonDescription | None = None
    nietzsche_text_chunks: list[StrictStr] = []
    nietzsche_advise: StrictStr | None = None
    ts_text_chunks: list[StrictStr] = []
    taylor_swift_advise: StrictStr | None = None
    jung_text_chunks: list[StrictStr] = []
    jung_advise: StrictStr | None = None
    selected_dc_poem: StrictStr | None = None
    selected_fc_message: StrictStr | None = None
    image_generation_prompt: StrictStr | None = None
    gen_image_path: FilePath | None = None
    concat_image: ConcatImage | None = None
    image_url: HttpUrl | None = None
    qr_image_path: FilePath | None = None
    printer_job_id: NonNegativeInt | None = None

    @field_validator("image_generation_prompt", mode="after")
    def image_prompt_validator(cls, v: str) -> str:
        if len(tiktoken_encoder.encode(v)) > 512:
            raise ValueError(
                "The image generation prompt exceeds the 512-token limit."
            )
