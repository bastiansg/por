from pathlib import Path

from pydantic import BaseModel, StrictStr, model_validator
from pydantic_extra_types.language_code import LanguageName


class FileMetadata(BaseModel):
    title: StrictStr
    author: StrictStr
    collection: StrictStr
    language: LanguageName
    extension: StrictStr | None = None


class FileItem(BaseModel):
    name: StrictStr
    metadata: FileMetadata

    @model_validator(mode="after")
    def set_extension(self):
        p = Path(self.name)
        self.metadata.extension = p.suffix

        return self


files = [
    #################### Matter ####################
    {
        "name": "a-bio-inspired-perspective-on-materials-sustainability.pdf",
        "metadata": {
            "title": "A Bio-Inspired Perspective on Materials Sustainability",
            "collection": "matter",
            "language": "English",
            "author": "Advanced Materials",
        },
    },
    {
        "name": "actualicing-material-capacities.pdf",
        "metadata": {
            "title": "Actualicing (Overlooked) Material Capacities",
            "collection": "matter",
            "language": "English",
            "author": "Branko Kolarevic",
        },
    },
    {
        "name": "al-bosque-lo-que-es-del-bosque.pdf",
        "metadata": {
            "title": "Al bosque lo que es del bosque (Phallus indusiatus)",
            "collection": "matter",
            "language": "Spanish",
            "author": "Marta Zatonyi",
        },
    },
    {
        "name": "amphibious-transport-of-fluids-and-solids-by-soft-magnetic-carpets.pdf",
        "metadata": {
            "title": "Amphibious Transport of Fluids and Solids by Soft Magnetic Carpets",
            "collection": "matter",
            "language": "English",
            "author": "Advanced Science",
        },
    },
    {
        "name": "animate-materials-report.pdf",
        "metadata": {
            "title": "Animate materials",
            "collection": "matter",
            "language": "English",
            "author": "The Royal Society",
        },
    },
    {
        "name": "arte-y-creacion.pdf",
        "metadata": {
            "title": "Arte y Creación",
            "collection": "matter",
            "language": "Spanish",
            "author": "Marta Zálon",
        },
    },
    {
        "name": "bringing-things-to-life.pdf",
        "metadata": {
            "title": "Bringing Things to Life: Creative Entanglements in a World of Materials",
            "collection": "matter",
            "language": "English",
            "author": "Tim Ingold",
        },
    },
    {
        "name": "designerly-ways-of-knowing.pdf",
        "metadata": {
            "title": "Designerly Ways of Knowing",
            "collection": "matter",
            "language": "English",
            "author": "Claudia Mareis",
        },
    },
    {
        "name": "heidi-jalkh-thesis-refes.txt",
        "metadata": {
            "title": "Heidi Jalkh Thesis Refes",
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "being-alive.pdf",
        "metadata": {
            "title": "Being Alive",
            "collection": "matter",
            "language": "English",
            "author": "Tim Ingold",
        },
    },
    {
        "name": "la-magna-auxetic.pdf",
        "metadata": {
            "title": "La Magna Auxetic",
            "collection": "matter",
            "language": "English",
            "author": "Roderic Lakes",
        },
    },
    {
        "name": "le-probleme-technique.pdf",
        "metadata": {
            "title": "Le Probleme Technique",
            "collection": "matter",
            "language": "French",
            "author": "Irlande Saurin",
        },
    },
    {
        "name": "making-matter-active-through-form.pdf",
        "metadata": {
            "title": "Making Matter Active Through Form",
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "material-intelligence.pdf",
        "metadata": {
            "title": "Material Intelligence",
            "collection": "matter",
            "language": "English",
            "author": "Glenn Adamson",
        },
    },
    {
        "name": "moa-chat-heidi-ai.rtf",
        "metadata": {
            "title": "Moa Chat Heidi Ai",
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "new-materialism.pdf",
        "metadata": {
            "title": "New Materialism",
            "collection": "matter",
            "language": "English",
            "author": "Rick Dolphijn & Iris van der Tuin",
        },
    },
    {
        "name": "no-cosas.epub",
        "metadata": {
            "title": "No Cosas",
            "collection": "matter",
            "language": "Spanish",
            "author": "Byung-Chul Han",
        },
    },
    {
        "name": "on-material-grammar.pdf",
        "metadata": {
            "title": "On Material Grammar",
            "collection": "matter",
            "language": "English",
            "author": "Lorenzo Guiducci & Heidi Jalkh",
        },
    },
    {
        "name": "parallel-minds.epub",
        "metadata": {
            "title": "Parallel Minds",
            "collection": "matter",
            "language": "English",
            "author": "Laura Tripaldi",
        },
    },
    {
        "name": "quotes-compilation.rtf",
        "metadata": {
            "title": "Quotes Compilation",
            "collection": "matter",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "name": "stuff-matters.pdf",
        "metadata": {
            "title": "Stuff Matters",
            "collection": "matter",
            "language": "English",
            "author": "Mark Miodownik",
        },
    },
    {
        "name": "survival-of-the-cheapest.pdf",
        "metadata": {
            "title": "Survival of the Cheapest",
            "collection": "matter",
            "language": "English",
            "author": "Julian F. V. Vincent",
        },
    },
    {
        "name": "the-limits-of-fabrication.pdf",
        "metadata": {
            "title": "The Limits of Fabrication",
            "collection": "matter",
            "language": "English",
            "author": "Nathan Brown",
        },
    },
    {
        "name": "the-new-materiality.pdf",
        "metadata": {
            "title": "The New Materiality",
            "collection": "matter",
            "language": "English",
            "author": "Manuel DeLanda",
        },
    },
    {
        "name": "the-positive-side-of-being-negative.pdf",
        "metadata": {
            "title": "The Positive Side of Being Negative",
            "collection": "matter",
            "language": "English",
            "author": "K. E. Evans & K. L. Alderson",
        },
    },
    {
        "name": "towarda-new-materialism.pdf",
        "metadata": {
            "title": "Toward a New Materialism",
            "collection": "matter",
            "language": "English",
            "author": "Rachel Tillman",
        },
    },
    {
        "name": "ultra-knowledge-and-gestaltung.pdf",
        "metadata": {
            "title": "Ultra Knowledge and Gestaltung",
            "collection": "matter",
            "language": "English",
            "author": "Nikola Doll, Horst Bredekamp & Wolfgang Schaffner",
        },
    },
    {
        "name": "vehlken-friedman-krauthausen-fratzl-essays.pdf",
        "metadata": {
            "title": "Vehlken Friedman Krauthausen Fratzl Essays",
            "collection": "matter",
            "language": "English",
            "author": "Michael Friedman & Karin Krauthausen",
        },
    },
    {
        "name": "vibrant-matter.epub",
        "metadata": {
            "title": "Vibrant Matter",
            "collection": "matter",
            "language": "English",
            "author": "Jane Bennett",
        },
    },
    {
        "name": "vincent-quotes.docx",
        "metadata": {
            "title": "Vincent Quotes",
            "collection": "matter",
            "language": "English",
            "author": "Julian F. V. Vincent",
        },
    },
    {
        "name": "wholeness-and-the-implicate-order.pdf",
        "metadata": {
            "title": "Wholeness and the Implicate Order",
            "collection": "matter",
            "language": "English",
            "author": "David Bohm",
        },
    },
]


file_items = [FileItem(**f) for f in files]
