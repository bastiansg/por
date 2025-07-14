from pydantic import BaseModel, StrictStr, PositiveInt

from common.cache import RedisCache
from common.utils.json_data import load_json
from rage.meta.interfaces import TextLoader, Document


class Metadata(BaseModel):
    title: StrictStr
    tag: StrictStr
    artist: StrictStr
    year: PositiveInt


INVALID_LYRICS = {"[Instrumental]"}


class LyricsLoader(TextLoader):
    def __init__(
        self,
        invalid_lyrics: set[str] = INVALID_LYRICS,
        cache: RedisCache | None = None,
    ):
        super().__init__(cache=cache)
        self.invalid_lyrics = invalid_lyrics

    def _get_documents(self, source_path: str) -> list[Document]:
        return [
            Document(
                text=data_item["lyrics"],
                metadata=Metadata(**data_item).model_dump(),
            )
            for data_item in load_json(json_file_path=source_path)
            if data_item["lyrics"] not in self.invalid_lyrics
        ]
