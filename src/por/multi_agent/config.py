from pydantic_settings import BaseSettings
from pydantic import (
    BaseModel,
    NonNegativeInt,
    NonNegativeFloat,
    StrictStr,
    Field,
)


class ServoAngles(BaseModel):
    x: NonNegativeInt = 90
    y: NonNegativeInt = 50


class RotatorParams(BaseModel):
    update_angle: NonNegativeInt = 5
    min_delta_x_angle: NonNegativeInt = 100
    min_delta_y_angle: NonNegativeInt = 120
    min_x_angle: NonNegativeInt = 20
    max_x_angle: NonNegativeInt = 160
    min_y_angle: NonNegativeInt = 30
    max_y_angle: NonNegativeInt = 150


class ImageSize(BaseModel):
    width: NonNegativeInt = 1024
    height: NonNegativeInt = 1024


class IdleAngles(BaseModel):
    x: NonNegativeInt = 90
    y: NonNegativeInt = 0


class Printer(BaseModel):
    por_logo_path: StrictStr = "/resources/ticket-images/por-logo.jpeg"
    max_text_len: NonNegativeInt = 48


class MultiAgentConfig(BaseSettings):
    servo_angles: ServoAngles = Field(default_factory=ServoAngles)
    rotator_params: RotatorParams = Field(default_factory=RotatorParams)
    image_size: ImageSize = Field(default_factory=ImageSize)
    history_length: NonNegativeInt = 90
    face_detector_min_score: NonNegativeFloat = 0.0
    images_path: StrictStr = "/resources/generated-images"
    image_extension: StrictStr = "jpg"
    idle_angles: IdleAngles = Field(default_factory=IdleAngles)
    printer: Printer = Field(default_factory=Printer)
