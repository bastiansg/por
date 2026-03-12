from pydantic import BaseModel, StrictStr
from pydantic_extra_types.language_code import LanguageName


class YTBMetadata(BaseModel):
    title: StrictStr
    author: StrictStr
    collection: StrictStr
    language: LanguageName


class YTBItem(BaseModel):
    source: StrictStr
    metadata: YTBMetadata


ytb_items = [
    #################### Matter ####################
    {
        "source": "https://www.youtube.com/watch?v=JGXi_9A__Vc",
        "metadata": {
            "title": "Everything You Need to Know About Planet Earth",
            "collection": "matter",
            "language": "English",
            "author": "@kurzgesagt",
        },
    },
    {
        "source": "https://www.youtube.com/watch?v=JQVmkDUkZT4",
        "metadata": {
            "title": "What Are You?",
            "collection": "matter",
            "language": "English",
            "author": "@kurzgesagt",
        },
    },
    {
        "source": "https://www.youtube.com/watch?v=QAa2O_8wBUQ",
        "metadata": {
            "title": "What is Dark Matter and Dark Energy?",
            "collection": "matter",
            "language": "English",
            "author": "@kurzgesagt",
        },
    },
]

ytb_items = [YTBItem(**i) for i in ytb_items]
