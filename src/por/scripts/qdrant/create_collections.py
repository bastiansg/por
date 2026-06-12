import os
import asyncio
import pycountry

from glob import glob
from tqdm import tqdm
from itertools import groupby

from rich.console import Console

from rage.retriever import Retriever
from rage.meta.interfaces import Document, TextChunk
from rage.utils.embeddings import get_openai_embeddings

from rage.splitters import MarkdownSplitter, TokenSplitter
from rage.loaders import PDFMarkdownLoader, MarkdownLoader, DocxLoader

from por.loaders import LyricsLoader, SATCLoader, YTBLoader

from .file_items import file_items
from .ytb_items import ytb_items


console = Console()


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
    file_paths = [
        fp
        for fp in glob(
            "/resources/documents/main/**/*",
            recursive=True,
        )
        if os.path.isfile(fp)
    ]

    file_map = {fi.source: fi for fi in file_items}
    text_chunks = []

    for fp in tqdm(file_paths, ascii=True):
        file_name = os.path.basename(fp)
        file_item = file_map[file_name]

        extension = file_item.metadata.extension
        assert extension is not None

        loader = LOADER_MAP[extension]["loader"]
        docs = await loader.load(
            source_path=fp,
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
        tcs = splitter.split_documents(documents=docs)
        text_chunks.extend(tcs)

    return text_chunks


async def get_ytb_text_chunks() -> list[TextChunk]:
    splitter = TokenSplitter()

    text_chunks = []
    for ytb_item in ytb_items:
        language = pycountry.languages.lookup(
            ytb_item.metadata.language
        ).alpha_2

        loader = YTBLoader(
            language=[language],
            metadata=ytb_item.metadata.model_dump(),
        )

        documents = await loader.load(source_path=ytb_item.source)
        tcs = splitter.split_documents(documents=documents)
        text_chunks.extend(tcs)

    return text_chunks


async def get_satc_text_chunks() -> list[TextChunk]:
    loader = SATCLoader()
    documents = await loader.load()

    splitter = TokenSplitter()
    text_chunks = splitter.split_documents(documents=documents)

    return text_chunks


async def get_lyrics_text_chunks() -> list[TextChunk]:
    loader = LyricsLoader()
    documents = await loader.load(
        source_path="/resources/documents/lyrics/lyrics.json"
    )

    splitter = TokenSplitter(
        chunk_size=128,
        chunk_overlap=16,
    )
    text_chunks = splitter.split_documents(documents=documents)

    return text_chunks


async def main() -> None:
    file_text_chunks = await get_file_text_chunks()
    console.log(f"file_text_chunks: {len(file_text_chunks)}")

    ytb_text_chunks = await get_ytb_text_chunks()
    console.log(f"ytb_text_chunks: {len(ytb_text_chunks)}")

    satc_text_chunks = await get_satc_text_chunks()
    console.log(f"satc_text_chunks: {len(satc_text_chunks)}")

    lyrics_text_chunks = await get_lyrics_text_chunks()
    console.log(f"lyrics_text_chunks: {len(lyrics_text_chunks)}")

    text_chunks = (
        file_text_chunks
        + ytb_text_chunks
        + satc_text_chunks
        + lyrics_text_chunks
    )

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
