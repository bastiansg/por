from gpiozero import Button
from escpos.printer import Usb
from functools import lru_cache

from sensehat_dsp.display import Image
from sensehat_dsp.display import Display

from por.dsp_images import dsp_images
from por.db.qdrant import _get_text_chunks
from por.meta.schema import TextChunk, ChunkMetadata
from por.multi_agent.console import render_node_detail


@lru_cache(maxsize=1)
def get_sensehat_dsp() -> Display:
    return Display()


@lru_cache(maxsize=1)
def get_button() -> Button:
    return Button(
        pin=16,
        hold_time=0.001,  # type: ignore
        bounce_time=0.001,
    )


@lru_cache(maxsize=1)
def get_dsp_images():
    return {dsp_image["name"]: Image(**dsp_image) for dsp_image in dsp_images}


def get_printer(profile: str = "TM-T20II") -> Usb:
    return Usb(
        0x04B8,
        0x0E27,
        0,  # type: ignore
        profile=profile,
    )


async def get_relevant_text_chunks(
    relevant_chunk_ids: list[str],
    collection_name: str,
) -> list[TextChunk]:
    render_node_detail("relevant_chunk_ids", len(relevant_chunk_ids))
    chunk_records = await _get_text_chunks(
        collection_name=collection_name,
        key="chunk_id",
        values=relevant_chunk_ids,
    )

    return [
        TextChunk(
            text=chunk_record.payload["page_content"],
            metadata=ChunkMetadata(**chunk_record.payload["metadata"]),
        )
        for chunk_record in chunk_records
        if chunk_record is not None and chunk_record.payload is not None
    ]
