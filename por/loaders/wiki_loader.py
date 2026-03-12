from urllib.parse import unquote, urlparse
from langchain_community.document_loaders import WikipediaLoader

from rage.meta.interfaces import Document, TextLoader


class WikiLoader(TextLoader):
    def __init__(
        self,
        load_max_docs: int = 1,
        doc_content_chars_max: int = 100_000,
        metadata: dict = {},
    ):
        super().__init__()
        self.load_max_docs = load_max_docs
        self.doc_content_chars_max = doc_content_chars_max
        self.metadata = metadata

    @staticmethod
    def _get_query(source_path: str) -> str:
        parsed_url = urlparse(source_path)
        article_path = parsed_url.path.removeprefix("/wiki/")
        return unquote(article_path).replace("_", " ")

    @staticmethod
    def _get_language(source_path: str) -> str:
        hostname = urlparse(source_path).hostname or ""
        return hostname.split(".", maxsplit=1)[0]

    async def get_documents(
        self,
        source_path: str | None = None,
    ) -> list[Document]:
        assert source_path is not None
        query = self._get_query(source_path=source_path)
        language = self._get_language(source_path=source_path)

        wiki_laoder = WikipediaLoader(
            query=query,
            lang=language,
            load_max_docs=self.load_max_docs,
            doc_content_chars_max=self.doc_content_chars_max,
        )

        documents = await wiki_laoder.aload()
        return [
            Document(
                text=doc.page_content,
                metadata={
                    "language": language,
                }
                | self.metadata,
            )
            for doc in documents
        ]
