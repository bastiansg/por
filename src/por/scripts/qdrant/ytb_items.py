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
    {
        "source": "https://www.youtube.com/watch?v=88n7W3BKqEo",
        "metadata": {
            "title": "El método de Jung para integrar tu sombra",
            "collection": "philosophy",
            "language": "Spanish",
            "author": "Cachetada",
        },
    },
    {
        "source": "https://www.youtube.com/watch?v=PHjQ6SIHj28",
        "metadata": {
            "title": "Los 12 arquetipos de Jung",
            "collection": "philosophy",
            "language": "Spanish",
            "author": "Cachetada",
        },
    },
    {
        "source": "https://www.youtube.com/watch?v=1KJcrdaICMo",
        "metadata": {
            "title": "Jung: Los arquetipos de la humanidad",
            "collection": "philosophy",
            "language": "Spanish",
            "author": "Cachetada",
        },
    },
    {
        "source": "https://www.youtube.com/watch?v=WOAl4FQWqfk",
        "metadata": {
            "title": "Cómo criar monstruos marinos",
            "collection": "philosophy",
            "language": "Spanish",
            "author": "Diago Singer",
        },
    },
]

ytb_items = [YTBItem(**i) for i in ytb_items]
