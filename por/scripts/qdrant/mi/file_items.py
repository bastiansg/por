from pathlib import Path

from pydantic import BaseModel, StrictStr, model_validator
from pydantic_extra_types.language_code import LanguageName


class FileMetadata(BaseModel):
    title: StrictStr | None = None
    extension: StrictStr | None = None
    collection: StrictStr
    language: LanguageName
    author: StrictStr | None = None


class FileItem(BaseModel):
    name: StrictStr
    metadata: FileMetadata

    @model_validator(mode="after")
    def set_extension(self):
        p = Path(self.name)

        self.metadata.extension = p.suffix
        self.metadata.title = p.stem.replace("-", " ").title()

        return self


files = [
    #################### Matter ####################
    {
        "name": "a-bio-inspired-perspective-on-materials-sustainability.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Advanced Materials",
        },
    },
    {
        "name": "actualicing-material-capacities.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Branko Kolarevic",
        },
    },
    # NOTE: Broken?
    # {
    #     "name": "a-guide-to-the-new-materials-revolution.epub",
    #     "metadata": {
    #         "collection": "matter",
    #         "language": "English",
    #     },
    # },
    {
        "name": "al-bosque-lo-que-es-del-bosque.pdf",
        "metadata": {
            "collection": "matter",
            "language": "Spanish",
            "author": "??",
        },
    },
    {
        "name": "amphibious-transport-of-fluids-and-solids-by-soft-magnetic-carpets.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Advanced Science",
        },
    },
    {
        "name": "animate-materials-report.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "The Royal Society",
        },
    },
    {
        "name": "arte-y-creacion.pdf",
        "metadata": {
            "collection": "matter",
            "language": "Spanish",
            "author": "Marta Zálon",
        },
    },
    {
        "name": "bringing-things-to-life.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Tim Ingold",
        },
    },
    {
        "name": "designerly-ways-of-knowing.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Claudia Mareis",
        },
    },
    {
        "name": "heidi-jalkh-thesis-refes.txt",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "being-alive.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Tim Ingold",
        },
    },
    {
        "name": "la-magna-auxetic.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "??",
        },
    },
    {
        "name": "le-probleme-technique.pdf",
        "metadata": {
            "collection": "matter",
            "language": "French",
            "author": "Irlande Saurin",
        },
    },
    {
        "name": "making-matter-active-through-form.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "material-intelligence.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Glenn Adamson",
        },
    },
    {
        # NOTE: What does "moa" mean?
        "name": "moa-chat-heidi-ai.rtf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "new-materialism.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Rick Dolphijn & Iris van der Tuin",
        },
    },
    {
        "name": "no-cosas.epub",
        "metadata": {
            "collection": "matter",
            "language": "Spanish",
            "author": "Byung-Chul Han",
        },
    },
    {
        "name": "on-material-grammar.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Lorenzo Guiducci & Heidi Jalkh",
        },
    },
    {
        "name": "parallel-minds.epub",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Laura Tripaldi",
        },
    },
    {
        "name": "quotes-compilation.rtf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "stuff-matters.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Mark Miodownik",
        },
    },
    {
        "name": "survival-of-the-cheapest.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Julian F. V. Vincent",
        },
    },
    {
        "name": "the-limits-of-fabrication.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Nathan Brown",
        },
    },
    {
        "name": "the-new-materiality.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Manuel DeLanda",
        },
    },
    # NOTE: Duplicate
    # {
    #     "name": "the-new-materiality-corrected.pdf",
    #     "metadata": {
    #         "collection": "matter",
    #         "language": "English",
    #         "author": "Manuel DeLanda",
    #     },
    # },
    {
        "name": "the-positive-side-of-being-negative.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "K. E. Evans & K. L. Alderson",
        },
    },
    {
        "name": "towarda-new-materialism.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Rachel Tillman",
        },
    },
    {
        "name": "ultra-knowledge-and-gestaltung.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "??",
        },
    },
    {
        "name": "vehlken-friedman-krauthausen-fratzl-essays.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "??",
        },
    },
    {
        "name": "vibrant-matter.epub",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "Jane Bennett",
        },
    },
    {
        "name": "vincent-quotes.docx",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "??",
        },
    },
    {
        "name": "wholeness-and-the-implicate-order.pdf",
        "metadata": {
            "collection": "matter",
            "language": "English",
            "author": "David Bohm",
        },
    },
    #################### Borges ####################
    {
        "name": "el-hacedor.epub",
        "metadata": {
            "collection": "borges",
            "language": "Spanish",
            "author": "Jorge Luis Borges",
        },
    },
    {
        "name": "el-libro-de-arena.epub",
        "metadata": {
            "collection": "borges",
            "language": "Spanish",
            "author": "Jorge Luis Borges",
        },
    },
    {
        "name": "ficciones.epub",
        "metadata": {
            "collection": "borges",
            "language": "Spanish",
            "author": "Jorge Luis Borges",
        },
    },
    {
        "name": "el-aleph.epub",
        "metadata": {
            "collection": "borges",
            "language": "Spanish",
            "author": "Jorge Luis Borges",
        },
    },
]


file_items = [FileItem(**f) for f in files]
