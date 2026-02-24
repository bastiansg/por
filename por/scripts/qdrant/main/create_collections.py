import os
import asyncio

from glob import glob
from tqdm import tqdm
from itertools import groupby

from common.cache import RedisCache
from common.logger import get_logger

from rage.retriever import Retriever
from rage.meta.interfaces import Document
from rage.splitters import MarkdownSplitter, TokenSplitter
from rage.utils.embeddings import get_openai_embeddings
from rage.loaders import PDFMarkdownLoader

from por.loaders import SATCLoader, LyricsLoader

from .file_items import file_items


logger = get_logger(__name__)


redis_cache = RedisCache()
LOADER_MAP = {".pdf": PDFMarkdownLoader(cache=redis_cache)}


async def main() -> None:
    file_paths = glob("/resources/documents/main/**/*")
    file_map = {fi.name: fi for fi in file_items}

    documents = []
    for fp in tqdm(file_paths, ascii=True):
        file_name = os.path.basename(fp)
        file_item = file_map[file_name]

        extension = file_item.metadata.extension
        assert extension is not None

        loader = LOADER_MAP[extension]
        docs = await loader.load(source_path=fp)
        docs = [
            Document(
                text=doc.text,
                metadata=doc.metadata | file_item.metadata.model_dump(),
            )
            for doc in docs
        ]

        documents.extend(docs)

    logger.info(f"documents: {len(documents)}")

    satc_loader = SATCLoader()
    satc_docs = await satc_loader.load()
    logger.info(f"satc documents: {len(satc_docs)}")

    ly_loader = LyricsLoader()
    ly_documents = await ly_loader.load(
        source_path="/resources/documents/lyrics/lyrics.json"
    )

    logger.info(f"lyrics documents: {len(ly_documents)}")

    md_splitter = MarkdownSplitter()
    tk_splitter = TokenSplitter()
    tk_splitter_128 = TokenSplitter(
        chunk_size=128,
        chunk_overlap=16,
    )

    text_chunks = md_splitter.split_documents(documents=documents)
    satc_text_chunks = tk_splitter.split_documents(documents=satc_docs)
    ly_text_chunks = tk_splitter_128.split_documents(documents=ly_documents)

    text_chunks = text_chunks + satc_text_chunks + ly_text_chunks
    logger.info(f"text_chunks: {len(text_chunks)}")

    text_chunks = sorted(
        text_chunks,
        key=lambda tc: tc.metadata["collection"],
    )

    collection_gropus = groupby(
        text_chunks,
        key=lambda tc: tc.metadata["collection"],
    )

    retriever = Retriever(dense_embeddings=get_openai_embeddings())
    for collection, text_chunks in collection_gropus:
        await retriever.create_collection(collection_name=collection)
        await retriever.insert_text_chunks(
            collection_name=collection,
            text_chunks=list(text_chunks),
        )


if __name__ == "__main__":
    asyncio.run(main())
