from rage.meta.interfaces import Document, TextLoader
from langchain_community.document_loaders import YoutubeLoader


class YTBLoader(TextLoader):
    def __init__(
        self,
        language: list[str] | None = None,
        metadata: dict = {},
    ):
        super().__init__()
        self.language = language or ["en"]
        self.metadata = metadata

    async def get_documents(
        self,
        source_path: str | None = None,
    ) -> list[Document]:
        assert source_path is not None
        loader = YoutubeLoader.from_youtube_url(
            youtube_url=source_path,
            language=self.language,
        )

        documents = await loader.aload()
        return [
            Document(
                text=document.page_content,
                metadata={"source_path": source_path} | self.metadata,
            )
            for document in documents
        ]
