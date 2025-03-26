import enum
from pydantic import BaseModel


class Localization(enum.Enum):
    EN = 'en'
    ES = 'es'


class LocalizedTopicsList(BaseModel):
    localization: Localization
    topics: list[str]
