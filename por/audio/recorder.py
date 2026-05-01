import time
import torch

import numpy as np
import soundfile as sf
import sounddevice as sd

from io import BytesIO
from IPython.display import Audio

from rich.console import Console
from por.utils.threading import threaded


console = Console()


# TODO: Move this module to the common package.
class AudioRecorder:
    def __init__(self, sample_rate: int = 16_000):
        self.sample_rate = sample_rate
        self.frames = []
        self.is_recording = False

    def stream_callback(self, indata, *_) -> None:
        self.frames.append(indata.copy())

    @threaded
    def start(self) -> None:
        self.frames = []
        self.is_recording = True
        console.log("start recording.")
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self.stream_callback,
        ):
            while self.is_recording:
                time.sleep(0.01)

    def stop(self) -> None:
        self.is_recording = False
        console.log("stop recording.")

    def playback(self) -> Audio | None:
        if not len(self.frames):
            console.log("no audio recorded.")
            return

        audio_np = np.concatenate(self.frames, axis=0)
        return Audio(
            audio_np.flatten(),
            rate=self.sample_rate,
        )

    def save_to_file(self, file: str | BytesIO) -> None:
        if not self.frames:
            console.log("no audio to save.")
            return

        audio_np = np.concatenate(self.frames, axis=0).flatten()
        waveform = torch.from_numpy(audio_np).clamp(-1.0, 1.0)

        sf.write(
            file,
            waveform.numpy(),
            self.sample_rate,
            format="WAV",
            subtype="PCM_16",
        )
