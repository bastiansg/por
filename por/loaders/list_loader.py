from common.cache import RedisCache
from common.utils.json_data import load_json
from rage.meta.interfaces import TextLoader, Document


class ListLoader(TextLoader):
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(cache=cache)

    async def _load(self, source_path: str) -> list[Document]:
        return [
            Document(text=text)
            for text in load_json(json_file_path=source_path)
        ]
