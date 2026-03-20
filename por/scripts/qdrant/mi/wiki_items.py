from pydantic import BaseModel, StrictStr


class WikiMetadata(BaseModel):
    title: StrictStr
    author: StrictStr
    collection: StrictStr


class WikiItem(BaseModel):
    source: StrictStr
    metadata: WikiMetadata


wiki_items = [
    #################### Matter ####################
    {
        "source": "https://es.wikipedia.org/wiki/Crassostrea_gigas",
        "metadata": {
            "title": "Crassostrea gigas",
            "collection": "matter",
            "author": "Wikipedia",
        },
    },
    {
        "source": "https://es.wikipedia.org/wiki/Mytilidae",
        "metadata": {
            "title": "Mytilidae",
            "collection": "matter",
            "author": "Wikipedia",
        },
    },
    {
        "source": "https://en.wikipedia.org/wiki/Cross-link",
        "metadata": {
            "title": "Cross-link",
            "collection": "matter",
            "author": "Wikipedia",
        },
    },
]

wiki_items = [WikiItem(**i) for i in wiki_items]
