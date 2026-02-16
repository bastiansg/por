from pydantic import BaseModel, StrictStr, Field


class ChunkMetadata(BaseModel):
    author: StrictStr = Field(description="")
    title: StrictStr = Field(description="")

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
