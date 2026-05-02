import asyncio
import httpx
import stamina

from tqdm import tqdm
from parsel import Selector

from rich.console import Console
from common.cache import cache, RedisCache

from rage.meta.interfaces import TextLoader, Document

from por.meta.schema import FileMetadata


console = Console()


@stamina.retry(on=httpx.HTTPError, wait_initial=10, wait_max=60, attempts=10)
async def _get_req(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

        return resp


async def get_req(url: str) -> httpx.Response | None:
    try:
        return await _get_req(url)
    except httpx.HTTPError:
        return None


class SATCLoader(TextLoader):
    def __init__(
        self,
        base_url: str = "https://subslikescript.com/series/Sex_and_the_City-159206",
        max_concurrency: int = 2,
    ):
        super().__init__()
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(max_concurrency)

    @staticmethod
    @cache(redis_cache=RedisCache())
    async def get_script_urls(base_url: str) -> list[str]:

        data_req = await get_req(url=base_url)
        assert data_req is not None

        selector = Selector(text=data_req.text)
        return [
            f"https://subslikescript.com{href}"
            for href in selector.css("div.season a::attr(href)").getall()
        ]

    @staticmethod
    @cache(redis_cache=RedisCache())
    async def get_script_(script_url: str) -> str:
        data_req = await get_req(url=script_url)
        assert data_req is not None

        selector = Selector(text=data_req.text)
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
                metadata=FileMetadata(
                    title="Sex and the City",
                    extension=None,
                    collection="satc",
                    language="English",  # type: ignore
                    author=None,
                ).model_dump(),
            )
            for script, script_url in zip(scripts, script_urls)
            if self.filter_script(script=script)
        ]

        console.log(f"scripts: {len(documents)}")
        console.log(f"invalid scripts: {len(scripts) - len(documents)}")

        return documents
