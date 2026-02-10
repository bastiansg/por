from pydantic import BaseModel, StrictStr, Field


class ChunkMetadata(BaseModel):
    # artist: StrictStr | None = Field(
    #     description="The artist of the song if the text chunk contains lyrics.",
    #     default=None,
    # )

    # title: StrictStr | None = Field(
    #     description="The title of the song if the text chunk contains lyrics.",
    #     default=None,
    # )

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
    text: StrictStr = Field(
        description="The actual textual content of the chunk."
    )

    metadata: ChunkMetadata
