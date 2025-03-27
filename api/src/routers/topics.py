import json
from pathlib import Path

from fastapi import APIRouter, Query

from src import config
from src.models.book import LocalizedTopicsList, Localization
from src.openai_topics import OpenAITopicsPredictor
from src.book_topics_cache import BookTopicsCache


TOPIC_TO_CLASS_EN = json.loads(Path(config.TOPIC_TO_CLASS_EN_FILE).read_text())
CLASS_TO_TOPIC_EN = {v:k for k,v in TOPIC_TO_CLASS_EN.items()}
TOPIC_TO_CLASS_ES = json.loads(Path(config.TOPIC_TO_CLASS_ES_FILE).read_text())
CLASS_TO_TOPIC_ES = {v:k for k,v in TOPIC_TO_CLASS_ES.items()}


topics_predictor = OpenAITopicsPredictor(
    openai_key=config.OPENAI_API_KEY,
    model=config.OPENAI_MODEL,
    en_topic_to_class=TOPIC_TO_CLASS_EN,
)

topics_cache = BookTopicsCache(
    p_file=Path(config.BOOK_TOPICS_CACHE_FILE)
)

router = APIRouter(prefix='/topics')


@router.get('/book', response_model=list[LocalizedTopicsList])
async def get_book_topics(
        identifier: str = Query(description='Book summary identifier'),
        title: str = Query(description='Summary title'),
        book_overview: str | None = Query(description='Book overview for more context.', default=None)
) -> list[LocalizedTopicsList]:
    topic_ids = topics_cache.get(identifier)
    if topic_ids is None:
        topic_ids = topics_predictor.predict(
            book_title=title,
            book_overview=book_overview
        )
        topics_cache.set(identifier, topic_ids)

    return [
        LocalizedTopicsList(
            localization=Localization.EN,
            topics=[CLASS_TO_TOPIC_EN[c] for c in topic_ids]
        ),
        LocalizedTopicsList(
            localization=Localization.ES,
            topics=[CLASS_TO_TOPIC_ES[c] for c in topic_ids]
        )
    ]