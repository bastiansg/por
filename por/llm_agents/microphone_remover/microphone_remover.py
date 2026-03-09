from pydantic_ai import ToolOutput

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import microphone_remover

from ..image_describer.image_describer import ImageDescriberOutput


class MicrophoneRemoverDeps(ImageDescriberOutput):
    pass


class MicrophoneRemover(LLMAgent[MicrophoneRemoverDeps, ImageDescriberOutput]):
    def __init__(
        self,
        conf_path=f"{microphone_remover.__path__[0]}/microphone-remover.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=MicrophoneRemoverDeps,
            output_type=ToolOutput(ImageDescriberOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
