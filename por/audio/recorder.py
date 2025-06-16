import torch
import torchaudio

import numpy as np
import sounddevice as sd

from IPython.display import Audio

from common.logger import get_logger
from common.utils.threading import threaded


logger = get_logger(__name__)


# TODO: Move this module to the common package.
class AudioRecorder:
    def __init__(self, sample_rate: int = 16_000):
        self.sample_rate = sample_rate
        self.frames = []
        self.recording = False

    def stream_callback(self, indata, *_):
        self.frames.append(indata.copy())

    @threaded
    def start(self) -> None:
        self.frames = []
        self.recording = True
        logger.info("start recording.")
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self.stream_callback,
        ):
            while self.recording:
                pass

    def stop(self) -> None:
        self.recording = False
        logger.info("stop recording.")

    def playback(self) -> Audio | None:
        if not len(self.frames):
            logger.warning("no audio recorded.")
            return

        audio_np = np.concatenate(self.frames, axis=0)
        return Audio(
            audio_np.flatten(),
            rate=self.sample_rate,
        )

    def save_to_file(self, file_path: str) -> None:
        if not self.frames:
            logger.warning("no audio to save.")
            return

        audio_np = np.concatenate(self.frames, axis=0).flatten()
        waveform = torch.from_numpy(audio_np).unsqueeze(0)

        torchaudio.save(file_path, waveform, self.sample_rate)
        logger.info(f"saved audio to => {file_path}")
