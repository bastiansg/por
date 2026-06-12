import asyncio

from pathlib import Path
from itertools import groupby

from tqdm import tqdm
from rich.console import Console

from rage.retriever import Retriever
from rage.meta.interfaces import Document, TextChunk
from rage.utils.embeddings import get_openai_embeddings

from rage.splitters import MarkdownSplitter, TokenSplitter
from rage.loaders import PDFMarkdownLoader, MarkdownLoader, DocxLoader

from por.loaders import CMTVLoader

from .ancora_file_items import ancora_file_items


console = Console()


ANCORA_DOCUMENTS_PATH = Path("/resources/documents/ancora")
CMTV_URL = (
    "https://www.cmtv.com.ar/discos_letras/show.php"
    "?bnid=234&banda=Patricio_Rey_y_Sus_Redonditos_de_Ricota"
)

PAYLOAD_INDEX_FIELDS = (
    "metadata.chunk_id",
    "metadata.language",
    "metadata.file_name",
)

LOADER_MAP = {
    ".pdf": {
        "loader": PDFMarkdownLoader(),
        "splitter": MarkdownSplitter(),
    },
    ".docx": {
        "loader": DocxLoader(),
        "splitter": MarkdownSplitter(),
    },
    ".epub": {
        "loader": MarkdownLoader(),
        "splitter": MarkdownSplitter(),
    },
    ".rtf": {
        "loader": MarkdownLoader(),
        "splitter": TokenSplitter(),
    },
    ".txt": {
        "loader": MarkdownLoader(),
        "splitter": TokenSplitter(),
    },
    ".md": {
        "loader": MarkdownLoader(),
        "splitter": TokenSplitter(),
    },
}


async def get_file_text_chunks() -> list[TextChunk]:
    async def get_file_item_text_chunks(file_item) -> list[TextChunk]:
        extension = file_item.metadata.extension
        assert extension is not None

        source_path = ANCORA_DOCUMENTS_PATH / file_item.source

        loader = LOADER_MAP[extension]["loader"]
        docs = await loader.load(
            source_path=str(source_path),
            cached_load=True,
        )

        docs = [
            Document(
                text=doc.text,
                metadata=doc.metadata | file_item.metadata.model_dump(),
            )
            for doc in docs
        ]

        splitter = LOADER_MAP[extension]["splitter"]
        return splitter.split_documents(documents=docs)

    text_chunk_groups = [
        await get_file_item_text_chunks(file_item=file_item)
        for file_item in tqdm(ancora_file_items, ascii=True)
    ]

    return [
        text_chunk
        for text_chunks in text_chunk_groups
        for text_chunk in text_chunks
    ]


async def get_cmtv_text_chunks() -> list[TextChunk]:
    loader = CMTVLoader()
    documents = await loader.load(source_path=CMTV_URL)

    splitter = TokenSplitter(
        chunk_size=128,
        chunk_overlap=16,
    )
    text_chunks = splitter.split_documents(documents=documents)

    return text_chunks


async def main() -> None:
    file_text_chunks = await get_file_text_chunks()
    console.log(f"file_text_chunks: {len(file_text_chunks)}")

    cmtv_text_chunks = await get_cmtv_text_chunks()
    console.log(f"cmtv_text_chunks: {len(cmtv_text_chunks)}")

    text_chunks = file_text_chunks + cmtv_text_chunks

    console.log(f"text_chunks: {len(text_chunks)}")
    text_chunks = sorted(
        text_chunks,
        key=lambda tc: tc.metadata["collection"],
    )

    collection_groups = groupby(
        text_chunks,
        key=lambda tc: tc.metadata["collection"],
    )

    retriever = Retriever(dense_embeddings=get_openai_embeddings())
    for collection, text_chunks in collection_groups:
        await retriever.create_collection(collection_name=collection)
        for field_name in PAYLOAD_INDEX_FIELDS:
            await retriever.create_payload_index(
                collection_name=collection,
                field_name=field_name,
            )

        await retriever.insert_text_chunks(
            collection_name=collection,
            text_chunks=list(text_chunks),
        )


if __name__ == "__main__":
    asyncio.run(main())
