import spotipy

from tqdm import tqdm
from datetime import datetime
from functools import lru_cache
from more_itertools import flatten

from pydantic import BaseModel, StrictStr, PositiveInt
from spotipy.oauth2 import SpotifyClientCredentials

from common.logger import get_logger
from common.cache import cache, RedisCache

from por.llm_agents import ArtistActivityChecker, ArtistActivityCheckerDeps


logger = get_logger(__name__)


@lru_cache()
def get_redis_cache() -> RedisCache:
    return RedisCache()


class Artist(BaseModel):
    id: StrictStr
    name: StrictStr
    last_year_active: PositiveInt


class Album(BaseModel):
    id: StrictStr
    name: StrictStr
    artist: StrictStr
    release_year: PositiveInt


class Track(BaseModel):
    id: StrictStr
    name: StrictStr
    album: StrictStr
    artist: StrictStr
    release_year: PositiveInt
    url: StrictStr


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.aac = ArtistActivityChecker(cache=get_redis_cache())

    @cache(redis_cache=get_redis_cache())
    async def serch_artist(self, artist: str) -> Artist | None:
        results = self.sp.search(
            q=f"artist:{artist}",
            type="artist",
        )

        if results is None:
            return

        artist_items = results["artists"]["items"]
        if not artist_items:
            return

        for artist_item in artist_items:
            if artist_item["name"] == artist:
                aac_output = await self.aac.generate(
                    user_prompt="Verified the last active year of the provided artist or band.",
                    agent_deps=ArtistActivityCheckerDeps(
                        artist=artist,
                        current_year=datetime.now().year,
                    ),
                )

                return Artist(
                    name=artist_item["name"],
                    id=artist_item["id"],
                    last_year_active=aac_output.last_year_active,
                )

    def parse_album_item(
        self,
        album_item: dict,
        artist: str,
        last_year_active: int,
    ) -> None | Album:
        release_year = int(album_item["release_date"][:4])
        if release_year > last_year_active:
            return

        return Album(
            **album_item,
            artist=artist,
            release_year=release_year,
        )

    def parse_album_items(
        self,
        album_items: list[dict],
        artist: str,
        last_year_active: int,
    ) -> list[Album]:
        albums = (
            self.parse_album_item(
                album_item=ai,
                artist=artist,
                last_year_active=last_year_active,
            )
            for ai in album_items
        )

        return [a for a in albums if a is not None]

    @cache(redis_cache=get_redis_cache())
    def get_artist_albums(self, artist: Artist, limit: int = 50) -> list[dict]:
        offset = 0
        album_items = []

        while True:
            results = self.sp.artist_albums(
                artist_id=artist.id,
                album_type="album",
                include_groups="album",
                limit=limit,
                offset=offset,
            )

            if results is None:
                break

            album_items_ = results["items"]
            if len(album_items) < limit:
                album_items.extend(
                    self.parse_album_items(
                        album_items=album_items_,
                        artist=artist.name,
                        last_year_active=artist.last_year_active,
                    )
                )

                break

            album_items.extend(
                self.parse_album_items(
                    album_items=album_items_,
                    artist=artist.name,
                    last_year_active=artist.last_year_active,
                )
            )

            offset = offset + limit

        return album_items

    def get_album_tracks(self, album: Album) -> list[Track]:
        tracks = self.sp.album_tracks(album_id=album.id, limit=50)
        if tracks is None:
            return []

        return [
            Track(
                id=ti["id"],
                name=ti["name"],
                album=album.name,
                artist=album.artist,
                release_year=album.release_year,
                url=ti["external_urls"]["spotify"],
            )
            for ti in tracks["items"]
        ]

    def get_albums_tracks(self, albums: list[Album]) -> list[Track]:
        album_tracks = map(self.get_album_tracks, tqdm(albums))
        return [at for at in flatten(album_tracks)]
