import asyncio
import aiohttp

from tqdm import tqdm
from parsel import Selector
from pydantic import BaseModel, StrictStr, PositiveInt

from common.logger import get_logger
from common.cache import cache, RedisCache

from rage.meta.interfaces import TextLoader, Document


logger = get_logger(__name__)


class Metadata(BaseModel):
    title: StrictStr
    tag: StrictStr
    artist: StrictStr
    year: PositiveInt


class SATCLoader(TextLoader):
    def __init__(
        self,
        base_url: str = "https://subslikescript.com/series/Sex_and_the_City-159206",
        max_concurrency: int = 5,
    ):
        super().__init__()
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(max_concurrency)

    @staticmethod
    @cache(redis_cache=RedisCache())
    async def get_script_urls(base_url: str) -> list[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url) as resp:
                resp.raise_for_status()
                html = await resp.text()

        selector = Selector(text=html)
        return [
            f"https://subslikescript.com{href}"
            for href in selector.css("div.season a::attr(href)").getall()
        ]

    @staticmethod
    @cache(redis_cache=RedisCache())
    async def get_script_(script_url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(script_url) as resp:
                resp.raise_for_status()
                html = await resp.text()

        selector = Selector(text=html)
        parts = selector.css("div.full-script ::text").getall()

        return " ".join(parts).strip()

    async def get_script(self, script_url: str, pbar: tqdm | None) -> str:
        async with self.semaphore:
            script = await self.get_script_(script_url=script_url)
            if pbar is not None:
                pbar.update(1)

            return script

    @staticmethod
    def filter_script(script: str) -> bool:
        qm_count = script.count("?")
        if qm_count > 1000:
            return False

        return True

    async def get_documents(
        self,
        source_path: str | None = None,
    ) -> list[Document]:
        script_urls = await self.get_script_urls(base_url=self.base_url)
        with tqdm(  # type: ignore
            total=len(script_urls),
            ascii=" ##",
            colour="#808080",
        ) as pbar:
            async with asyncio.TaskGroup() as tg:
                tasks = [
                    tg.create_task(
                        self.get_script(
                            script_url=script_url,
                            pbar=pbar,
                        )
                    )
                    for script_url in script_urls
                ]

            scripts = [t.result() for t in tasks]

        documents = [
            Document(
                text=script,
                metadata={"url": script_url},
            )
            for script, script_url in zip(scripts, script_urls)
            if self.filter_script(script=script)
        ]

        logger.info(f"scripts: {len(documents)}")
        logger.info(f"invalid scripts: {len(scripts) - len(documents)}")

        return documents
