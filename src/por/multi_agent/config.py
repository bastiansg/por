from pydantic import (
    BaseModel,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    StrictBool,
    StrictInt,
    StrictStr,
)
from pydantic_settings import BaseSettings


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
    width: NonNegativeInt = 640
    height: NonNegativeInt = 640


class CaptureSize(BaseModel):
    width: NonNegativeInt = 2048
    height: NonNegativeInt = 2048


class IdleAngles(BaseModel):
    x: NonNegativeInt = 90
    y: NonNegativeInt = 0


class Printer(BaseModel):
    por_logo_path: StrictStr = "/resources/ticket-images/por-logo.jpeg"
    max_text_len: NonNegativeInt = 48


class ReplicateInputConfig(BaseModel):
    model: StrictStr = "dev"
    lora_scale: PositiveFloat = 1.3
    megapixels: StrictStr = "1"
    num_outputs: PositiveInt = 1
    aspect_ratio: StrictStr = "9:16"
    output_format: StrictStr = "jpg"
    guidance_scale: PositiveFloat = 5.0
    output_quality: PositiveInt = 100
    num_inference_steps: PositiveInt = 28
    disable_safety_checker: StrictBool = True


class MultiAgentConfig(BaseSettings):
    servo_angles: ServoAngles = Field(default_factory=ServoAngles)
    rotator_params: RotatorParams = Field(default_factory=RotatorParams)
    image_size: ImageSize = Field(default_factory=ImageSize)
    capture_size: CaptureSize = Field(default_factory=CaptureSize)
    final_capture_y_angle_offset: StrictInt = -15
    history_length: NonNegativeInt = 1
    face_detector_min_score: NonNegativeFloat = 0.0
    images_path: StrictStr = "/resources/generated-images"
    input_image_extension: StrictStr = "jpg"
    generated_image_extension: StrictStr = "jpg"
    caption_header: StrictStr = (
        "In the Style of PBFR, a raw monochrome ink sketch with bold, "
        "expressive linework of:"
    )

    replicate_model: StrictStr = (
        "bastiansg/pbfr-flux:"
        "35bbe647e733755ba300aa2ba1acf6ea211ce1615f7c6be53b1fa4c32cb5146d"
    )

    replicate_timeout: PositiveFloat = 120.0
    replicate_input: ReplicateInputConfig = Field(
        default_factory=ReplicateInputConfig,
    )

    idle_angles: IdleAngles = Field(default_factory=IdleAngles)
    printer: Printer = Field(default_factory=Printer)
