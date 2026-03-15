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
    source: StrictStr
    metadata: FileMetadata

    @model_validator(mode="after")
    def set_extension(self):
        p = Path(self.source)
        self.metadata.extension = p.suffix

        return self


files = [
    #################### Matter ####################
    {
        "source": "a-bio-inspired-perspective-on-materials-sustainability.pdf",
        "metadata": {
            "collection": "matter",
            "title": "A Bio-Inspired Perspective on Materials Sustainability",
            "language": "English",
            "author": "Advanced Materials",
        },
    },
    {
        "source": "actualicing-material-capacities.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Actualicing (Overlooked) Material Capacities",
            "language": "English",
            "author": "Branko Kolarevic",
        },
    },
    {
        "source": "al-bosque-lo-que-es-del-bosque.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Al bosque lo que es del bosque (Phallus indusiatus)",
            "language": "Spanish",
            "author": "Marta Zatonyi",
        },
    },
    {
        "source": "amphibious-transport-of-fluids-and-solids-by-soft-magnetic-carpets.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Amphibious Transport of Fluids and Solids by Soft Magnetic Carpets",
            "language": "English",
            "author": "Advanced Science",
        },
    },
    {
        "source": "animate-materials-report.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Animate materials",
            "language": "English",
            "author": "The Royal Society",
        },
    },
    {
        "source": "arte-y-creacion.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Arte y Creación",
            "language": "Spanish",
            "author": "Marta Zálon",
        },
    },
    {
        "source": "bringing-things-to-life.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Bringing Things to Life: Creative Entanglements in a World of Materials",
            "language": "English",
            "author": "Tim Ingold",
        },
    },
    {
        "source": "designerly-ways-of-knowing.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Designerly Ways of Knowing",
            "language": "English",
            "author": "Claudia Mareis",
        },
    },
    {
        "source": "heidi-jalkh-thesis-refes.txt",
        "metadata": {
            "collection": "matter",
            "title": "Heidi Jalkh Thesis Refes",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "source": "being-alive.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Being Alive",
            "language": "English",
            "author": "Tim Ingold",
        },
    },
    {
        "source": "la-magna-auxetic.pdf",
        "metadata": {
            "collection": "matter",
            "title": "La Magna Auxetic",
            "language": "English",
            "author": "Roderic Lakes",
        },
    },
    {
        "source": "le-probleme-technique.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Le Probleme Technique",
            "language": "French",
            "author": "Irlande Saurin",
        },
    },
    {
        "source": "making-matter-active-through-form.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Making Matter Active Through Form",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "source": "material-intelligence.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Material Intelligence",
            "language": "English",
            "author": "Glenn Adamson",
        },
    },
    {
        "source": "moa-chat-heidi-ai.rtf",
        "metadata": {
            "collection": "matter",
            "title": "Moa Chat Heidi Ai",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "source": "new-materialism.pdf",
        "metadata": {
            "collection": "matter",
            "title": "New Materialism",
            "language": "English",
            "author": "Rick Dolphijn & Iris van der Tuin",
        },
    },
    {
        "source": "no-cosas.epub",
        "metadata": {
            "collection": "matter",
            "title": "No Cosas",
            "language": "Spanish",
            "author": "Byung-Chul Han",
        },
    },
    {
        "source": "on-material-grammar.pdf",
        "metadata": {
            "collection": "matter",
            "title": "On Material Grammar",
            "language": "English",
            "author": "Lorenzo Guiducci & Heidi Jalkh",
        },
    },
    {
        "source": "parallel-minds.epub",
        "metadata": {
            "collection": "matter",
            "title": "Parallel Minds",
            "language": "English",
            "author": "Laura Tripaldi",
        },
    },
    {
        "source": "quotes-compilation.rtf",
        "metadata": {
            "collection": "matter",
            "title": "Quotes Compilation",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "source": "stuff-matters.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Stuff Matters",
            "language": "English",
            "author": "Mark Miodownik",
        },
    },
    {
        "source": "survival-of-the-cheapest.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Survival of the Cheapest",
            "language": "English",
            "author": "Julian F. V. Vincent",
        },
    },
    {
        "source": "the-limits-of-fabrication.pdf",
        "metadata": {
            "collection": "matter",
            "title": "The Limits of Fabrication",
            "language": "English",
            "author": "Nathan Brown",
        },
    },
    {
        "source": "the-new-materiality.pdf",
        "metadata": {
            "collection": "matter",
            "title": "The New Materiality",
            "language": "English",
            "author": "Manuel DeLanda",
        },
    },
    {
        "source": "the-positive-side-of-being-negative.pdf",
        "metadata": {
            "collection": "matter",
            "title": "The Positive Side of Being Negative",
            "language": "English",
            "author": "K. E. Evans & K. L. Alderson",
        },
    },
    {
        "source": "towarda-new-materialism.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Toward a New Materialism",
            "language": "English",
            "author": "Rachel Tillman",
        },
    },
    {
        "source": "ultra-knowledge-and-gestaltung.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Ultra Knowledge and Gestaltung",
            "language": "English",
            "author": "Nikola Doll, Horst Bredekamp & Wolfgang Schaffner",
        },
    },
    {
        "source": "vehlken-friedman-krauthausen-fratzl-essays.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Vehlken Friedman Krauthausen Fratzl Essays",
            "language": "English",
            "author": "Michael Friedman & Karin Krauthausen",
        },
    },
    {
        "source": "vibrant-matter.epub",
        "metadata": {
            "collection": "matter",
            "title": "Vibrant Matter",
            "language": "English",
            "author": "Jane Bennett",
        },
    },
    {
        "source": "vincent-quotes.docx",
        "metadata": {
            "collection": "matter",
            "title": "Vincent Quotes",
            "language": "English",
            "author": "Julian F. V. Vincent",
        },
    },
    {
        "source": "wholeness-and-the-implicate-order.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Wholeness and the Implicate Order",
            "language": "English",
            "author": "David Bohm",
        },
    },
    {
        "source": "things-fall-together.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Things Fall Together",
            "language": "English",
            "author": "Skylar Tibbits",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-01.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-02.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-03.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-04.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-05.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-06.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-07.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-08.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-09.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "trazos-edicion-biomateriales-10.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trazos edición biomateriales. Sistemas Materiales.",
            "language": "Spanish",
            "author": "Pozzetti, G., Jalkh, H.",
        },
    },
    {
        "source": "shells-from-aquaculture.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Shells from aquaculture: a valuable biomaterial, not a nuisance waste product",
            "language": "English",
            "author": "James P. Morris, Thierry Backeljau, Gauthier Chapelle",
        },
    },
    {
        "source": "mdpi.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Trends and Opportunities of Bivalve Shells' Waste Valorization in a Prospect of Circular Blue Bioeconomy",
            "language": "English",
            "author": "Daniela Summa, Mattia Lanzoni, Giuseppe Castaldelli, Elisa Anna Fano, Elena Tamburini",
        },
    },
    {
        "source": "marine-biobased-materials-and-networks.pdf",
        "metadata": {
            "collection": "matter",
            "title": "Crosslinked. Marine biobased materials and networks.",
            "language": "English",
            "author": "Heidi Jalkh",
        },
    },
    {
        "source": "material-interactions-press.epub",
        "metadata": {
            "collection": "matter",
            "title": "Material Interactions 一 A New Species of Design",
            "language": "English",
            "author": "Heidi Jalkh and Nadya Suvorova",
        },
    },
]


file_items = [FileItem(**f) for f in files]
