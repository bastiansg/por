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


class FalLoraConfig(BaseModel):
    # path: StrictStr = "https://v3b.fal.media/files/b/0aabdb3f/mr5Rou2s8RktEeKvlIb9V_pytorch_lora_weights.safetensors"
    path: StrictStr = "https://v3b.fal.media/files/b/0aabdcf1/Sqy1p_b0foSsoCBR1k3ev_flux-lora.safetensors"
    scale: PositiveFloat = 2.0


class FalInputConfig(BaseModel):
    image_size: StrictStr = "portrait_16_9"
    num_images: PositiveInt = 1
    output_format: StrictStr = "jpeg"
    acceleration: StrictStr = "none"
    guidance_scale: PositiveFloat = 5
    num_inference_steps: PositiveInt = 50
    enable_safety_checker: StrictBool = False
    loras: list[FalLoraConfig] = Field(
        default_factory=lambda: [FalLoraConfig()],
    )


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

    fal_model: StrictStr = "fal-ai/flux-lora"
    fal_timeout: PositiveFloat = 120.0
    fal_input: FalInputConfig = Field(
        default_factory=FalInputConfig,
    )

    idle_angles: IdleAngles = Field(default_factory=IdleAngles)
    printer: Printer = Field(default_factory=Printer)
