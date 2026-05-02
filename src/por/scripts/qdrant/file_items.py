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
    ########## Friedrich Nietzsche ##########
    {
        "source": "asi-hablo-zaratustra.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "Así habló Zaratustra",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "aurora.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "Aurora",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "como-se-filosofa-a-martillazos.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "Como se filosofa a martillazos",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "ecce-homo-sp.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "Ecce homo",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "el-anticristo.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "El Anticristo",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "el-caminante-y-su-sombra.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "El caminante y su sombra",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "el-nacimiento-de-la-tragedia-en-el-espiritu-de-la-musica.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "El nacimiento de la tragedia desde el espíritu de la música",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "el-ocaso-de-los-idolos.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "El ocaso de los ídolos",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "la-gaya-ciencia.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "La gaya ciencia",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "la-genealogia-de-la-moral.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "La genealogía de la moral",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "mas-alla-del-bien-y-del-mal.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "Más allá del bien y del mal",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "source": "sobre-verdad-y-mentira-en-sentido-extramoral.pdf",
        "metadata": {
            "collection": "philosophy",
            "title": "Sobre verdad y mentira en sentido extramoral",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    ########## Astrology ##########
    {
        "source": "sun-signs.epub",
        "metadata": {
            "collection": "astrology",
            "title": "Sun Signs",
            "language": "English",
            "author": "Linda Goodman",
        },
    },
    {
        "source": "love-signs.epub",
        "metadata": {
            "collection": "astrology",
            "title": "Love Signs",
            "language": "English",
            "author": "Linda Goodman",
        },
    },
    {
        "source": "ascendentes.pdf",
        "metadata": {
            "collection": "astrology",
            "title": "Ascendentes",
            "language": "Spanish",
            "author": "Eugenio Carutti",
        },
    },
    {
        "source": "lunas.pdf",
        "metadata": {
            "collection": "astrology",
            "title": "Lunas",
            "language": "Spanish",
            "author": "Eugenio Carutti",
        },
    },
]


file_items = [FileItem(**f) for f in files]
