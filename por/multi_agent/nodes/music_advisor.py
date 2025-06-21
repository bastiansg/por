from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import MusicAdvisor, MusicAdvisorInput, Song
from por.multi_agent.schema import StateSchema, ConfigSchema


from .utils import get_retriever


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing music_advisor...")
    conf = config["configurable"]

    retriever = get_retriever()
    question = state.audio_transcription

    retriever_items = await retriever.dense_search(
        collection_name="lyrics",
        query=question,
        k=1,
    )

    selected_song = Song(
        title=retriever_items[0].metadata["title"],
        artist=retriever_items[0].metadata["artist"],
        lyrics=retriever_items[0].text,
    )

    music_advisor = MusicAdvisor()
    music_advisor_output = await music_advisor.generate(
        agent_input=MusicAdvisorInput(
            question=question,
            psychological_profile=state.psychological_profile,
            song=selected_song,
            output_language=conf["output_language"],
        )
    )

    return {
        "selected_song": selected_song,
        "music_advice": music_advisor_output.music_advice,
    }


music_advisor = Node(
    name="music_advisor",
    run=run,
)
