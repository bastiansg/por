from pydantic_ai import NativeOutput

from llm_agents.meta.interfaces import LLMAgent

from por.meta.schema import AstrologyPlacements
from por.llm_agents import astrology_placements_extractor


class AstrologyPlacementsExtractor(LLMAgent[None, AstrologyPlacements]):
    def __init__(
        self,
        conf_path=(
            f"{astrology_placements_extractor.__path__[0]}/"
            "astrology-placements-extractor.yml"
        ),
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=NativeOutput(AstrologyPlacements),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
