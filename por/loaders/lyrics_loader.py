import asyncio

from pydantic import BaseModel, StrictStr, PositiveInt

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
    ):
        super().__init__()
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

    async def get_documents(self, source_path: str) -> list[Document]:
        return await asyncio.to_thread(
            self._get_documents,
            source_path=source_path,
        )
