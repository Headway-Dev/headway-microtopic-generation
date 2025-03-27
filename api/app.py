import shutil
from pathlib import Path

from fastapi import FastAPI

from src import config


def populate_data():
    default2dest = {
        config.DEFAULT_TOPIC_TO_CLASS_EN_FILE: config.TOPIC_TO_CLASS_EN_FILE,
        config.DEFAULT_TOPIC_TO_CLASS_ES_FILE: config.TOPIC_TO_CLASS_ES_FILE,
        config.PREPOPULATED_BOOK_TOPICS_CACHE_FILE: config.BOOK_TOPICS_CACHE_FILE,
    }
    for default, dest in default2dest.items():
        if Path(dest).exists():
            print(f'{dest} already exists')
            continue
        if not Path(default).exists():
            print(f'Cannot populate {dest} because {default} does not exist')
        print(f'Populating {dest} with {default}')
        Path(dest).parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(default, dest)

populate_data()

from src import routers

app = FastAPI()
app.include_router(routers.topics.router)