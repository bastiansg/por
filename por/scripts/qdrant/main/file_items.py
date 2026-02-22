from por.meta.schema import FileItem


files = [
    #################### Nietzsche ####################
    {
        "name": "asi-hablo-zaratustra.pdf",
        "metadata": {
            "title": "Así habló Zaratustra",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "aurora.pdf",
        "metadata": {
            "title": "Aurora",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "como-se-filosofa-a-martillazos.pdf",
        "metadata": {
            "title": "Como se filosofa a martillazos",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "ecce-homo-sp.pdf",
        "metadata": {
            "title": "Ecce homo",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "el-anticristo.pdf",
        "metadata": {
            "title": "El Anticristo",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "el-caminante-y-su-sombra.pdf",
        "metadata": {
            "title": "El caminante y su sombra",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "el-nacimiento-de-la-tragedia-en-el-espiritu-de-la-musica.pdf",
        "metadata": {
            "title": "El nacimiento de la tragedia desde el espíritu de la música",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "el-ocaso-de-los-idolos.pdf",
        "metadata": {
            "title": "El ocaso de los ídolos",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "la-gaya-ciencia.pdf",
        "metadata": {
            "title": "La gaya ciencia",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "la-genealogia-de-la-moral.pdf",
        "metadata": {
            "title": "La genealogía de la moral",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "mas-alla-del-bien-y-del-mal.pdf",
        "metadata": {
            "title": "Más allá del bien y del mal",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    {
        "name": "sobre-verdad-y-mentira-en-sentido-extramoral.pdf",
        "metadata": {
            "title": "Sobre verdad y mentira en sentido extramoral",
            "collection": "nietzsche",
            "language": "Spanish",
            "author": "Friedrich Nietzsche",
        },
    },
    #################### Machiavelli ####################
    {
        "name": "del-arte-de-la-guerra.pdf",
        "metadata": {
            "title": "Del arte de la guerra",
            "collection": "machiavelli",
            "language": "Spanish",
            "author": "Niccolo Machiavelli",
        },
    },
    {
        "name": "discurso-sobre-la-primera-decada-de-tito-livio.pdf",
        "metadata": {
            "title": "Discursos sobre la primera década de Tito Livio",
            "collection": "machiavelli",
            "language": "Spanish",
            "author": "Niccolo Machiavelli",
        },
    },
    {
        "name": "el-principe.pdf",
        "metadata": {
            "title": "El príncipe",
            "collection": "machiavelli",
            "language": "Spanish",
            "author": "Niccolo Machiavelli",
        },
    },
    {
        "name": "la-mandragora.pdf",
        "metadata": {
            "title": "La mandrágora",
            "collection": "machiavelli",
            "language": "Spanish",
            "author": "Niccolo Machiavelli",
        },
    },
]


file_items = [FileItem(**f) for f in files]
