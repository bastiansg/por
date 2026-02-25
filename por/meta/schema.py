from pathlib import Path

from pydantic_extra_types.language_code import LanguageName
from pydantic import (
    BaseModel,
    StrictStr,
    Field,
    NonNegativeInt,
    model_validator,
)


class ChunkMetadata(BaseModel):
    title: StrictStr = Field(description="")
    artist: StrictStr | None = Field(
        description="",
        default=None,
    )

    author: StrictStr | None = Field(
        description="",
        default=None,
    )

    chunk_id: StrictStr = Field(
        description="A unique identifier for this text chunk within the collection."
    )

    previous_chunk_id: StrictStr | None = Field(
        description="The chunk_id of the preceding text chunk within the same collection.",
        default=None,
    )

    next_chunk_id: StrictStr | None = Field(
        description="The chunk_id of the following text chunk within the same collection.",
        default=None,
    )


class TextChunk(BaseModel):
    text: StrictStr = Field(description="The textual content of the chunk.")
    metadata: ChunkMetadata


class FileMetadata(BaseModel):
    title: StrictStr | None = None
    extension: StrictStr | None = None
    collection: StrictStr
    language: LanguageName | None = None
    author: StrictStr | None = None


class FileItem(BaseModel):
    name: StrictStr
    metadata: FileMetadata

    @model_validator(mode="after")
    def set_extension(self):
        p = Path(self.name)
        self.metadata.extension = p.suffix

        return self


class Song(BaseModel):
    title: StrictStr = Field(
        description="Recommended song title.",
        min_length=1,
    )

    artist: StrictStr = Field(
        description="Artist of the recommended song.",
        min_length=1,
    )

    year: NonNegativeInt = Field(
        description="Release year of the recommended song.",
    )
