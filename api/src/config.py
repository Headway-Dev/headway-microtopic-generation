import os
import dotenv

dotenv.load_dotenv()

TEST_ACCESS_TOKEN = '8b0d0a8feae7be390b04112d1'

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_MODEL = 'gpt-4o-mini'


DEFAULT_DATA_DIR = 'default_data/'
DATA_DIR = os.environ['API_DATA_DIR']
TOPIC_TO_CLASS_EN_FILENAME = 'tpk_to_class_en.json'
TOPIC_TO_CLASS_ES_FILENAME = 'tpk_to_class_es.json'

DEFAULT_TOPIC_TO_CLASS_EN_FILE = os.path.join(DEFAULT_DATA_DIR, TOPIC_TO_CLASS_EN_FILENAME)
TOPIC_TO_CLASS_EN_FILE = os.path.join(DATA_DIR, TOPIC_TO_CLASS_EN_FILENAME)
DEFAULT_TOPIC_TO_CLASS_ES_FILE = os.path.join(DEFAULT_DATA_DIR, TOPIC_TO_CLASS_ES_FILENAME)
TOPIC_TO_CLASS_ES_FILE = os.path.join(DATA_DIR, TOPIC_TO_CLASS_ES_FILENAME)

PREPOPULATED_BOOK_TOPICS_CACHE_FILE = os.path.join(DEFAULT_DATA_DIR, 'book_to_classes.json')
BOOK_TOPICS_CACHE_FILE = os.path.join(DATA_DIR, 'cache_book_to_class.json')
