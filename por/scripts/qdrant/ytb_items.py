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
    {
        "source": "https://www.youtube.com/watch?v=YrF0wesN7T0",
        "metadata": {
            "title": "La noción del gasto",
            "collection": "philosophy",
            "language": "Spanish",
            "author": "Georges Bataille",
        },
    },
]

ytb_items = [YTBItem(**i) for i in ytb_items]
