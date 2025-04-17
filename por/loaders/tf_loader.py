from tqdm import tqdm

from common.cache import RedisCache
from rage.meta.interfaces import TextLoader, Document

from unstructured.partition.docx import partition_docx


class TFLoader(TextLoader):
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(cache=cache)

    def _load(self, source_path: str) -> list[Document]:
        text_elements = (
            elem.to_dict() for elem in partition_docx(filename=source_path)
        )

        documents = []
        text_lines = []
        for te in text_elements:
            if te["type"] == "Title":
                if not len(text_lines):
                    continue

                documents.append(Document(text=" ".join(text_lines)))
                text_lines = []
                continue

            text_lines.append(te["text"])

        return documents
