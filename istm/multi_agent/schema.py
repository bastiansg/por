from common.utils.path import create_path

from sensehat_dsp.display import Color

from hailo_apps.servos import ServoAngles
from hailo_apps.meta.interfaces import RotatorParams, ImageSize


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


class GolColors(BaseModel):
    p_color: Color
    s_color: Color


class ConfigSchema(BaseModel):
    servo_angles: ServoAngles
    rotator_params: RotatorParams
    image_size: ImageSize
    image_margin: NonNegativeInt
    description_guidelines: StrictStr
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
    dry_mode: StrictBool = False
    dry_mode_wait: NonNegativeInt = 5

    @field_validator("images_path", mode="after")
    def images_path_validator(cls, v: str) -> str:
        create_path(path=v)
        return v


class StateSchema(BaseModel):
    image_id: StrictStr
    image_path: FilePath | None = None
    image_description: StrictStr | None = None
    gen_image_path: FilePath | None = None
    concat_image_path: FilePath | None = None
    image_url: HttpUrl | None = None
    qr_image_path: FilePath | None = None
    printer_job_id: NonNegativeInt | None = None
