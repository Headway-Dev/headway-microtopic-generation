import os
import dotenv

dotenv.load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_MODEL = 'gpt-4o-mini'

TOPIC_TO_CLASS_EN_FILE = 'data/tpk_to_class_en.json'
TOPIC_TO_CLASS_ES_FILE = 'data/tpk_to_class_es.json'

BOOK_TOPICS_CACHE_FILE = 'data/cache_book_to_class.json'
