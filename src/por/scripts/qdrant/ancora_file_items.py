from .file_items import FileItem


files = [
    {
        "source": "aceleracionismo-y-extrema-derecha.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Aceleracionismo y extrema derecha",
            "language": "Spanish",
            "author": "Enrique Arias Gil",
        },
    },
    {
        "source": "ancla-una-forma-de-hacer-politica-a-traves-de-la-escritura.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "ANCLA: una forma de hacer política a través de la escritura",
            "language": "Spanish",
            "author": "Revista Haroldo",
        },
    },
    {
        "source": "ciencia-ficcion-capitalista-como-los-multimillonarios-nos-salvaran-del-mundo.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Ciencia ficción capitalista: como los multimillonarios nos salvarán del mundo",
            "language": "Spanish",
            "author": "Francisco Mondaca",
        },
    },
    {
        "source": "codigo-stiuso.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Código Stiuso",
            "language": "Spanish",
            "author": "Gerardo Young",
        },
    },
    {
        "source": "esta-entre-nosotros.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Está entre nosotros",
            "language": "Spanish",
            "author": "Pablo Semán",
        },
    },
    {
        "source": "estados-nerviosos.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Estados nerviosos",
            "language": "Spanish",
            "author": "William Davies",
        },
    },
    {
        "source": "extrema-derecha-que-es-y-como-combatirla.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Extrema derecha: qué es y cómo combatirla",
            "language": "Spanish",
            "author": "Enzo Traverso",
        },
    },
    {
        "source": "la-democracia-en-peligro.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "La democracia en peligro",
            "language": "Spanish",
            "author": "Steven Levitsky y Daniel Ziblatt",
        },
    },
    {
        "source": "la-era-del-capitalismo-de-vigilancia.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "La era del capitalismo de la vigilancia",
            "language": "Spanish",
            "author": "Shoshana Zuboff",
        },
    },
    {
        "source": "la-rebelion-del-publico.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "La rebelión del público",
            "language": "Spanish",
            "author": "Martin Gurri",
        },
    },
    {
        "source": "los-ingenieros-del-caos.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Los ingenieros del caos",
            "language": "Spanish",
            "author": "Giuliano da Empoli",
        },
    },
    {
        "source": "nuevas-derechas-y-propaganda-final-que-dicen-de-feminismos-en-youtube-y-tiktok.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Nuevas derechas y propaganda: qué dicen de feminismos en YouTube y TikTok",
            "language": "Spanish",
            "author": "Sandra Chaher",
        },
    },
    {
        "source": "operacion-masacre.pdf",
        "metadata": {
            "collection": "rodolfo-walsh",
            "title": "Operación masacre",
            "language": "Spanish",
            "author": "Rodolfo Walsh",
        },
    },
    {
        "source": "quien-mato-a-rosendo.pdf",
        "metadata": {
            "collection": "rodolfo-walsh",
            "title": "¿Quién mató a Rosendo?",
            "language": "Spanish",
            "author": "Rodolfo Walsh",
        },
    },
    {
        "source": "realismo-capitalista.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Realismo capitalista",
            "language": "Spanish",
            "author": "Mark Fisher",
        },
    },
    {
        "source": "recorridos-de-la-investigacion-politica-en-argentina.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Recorridos de la investigación política en Argentina",
            "language": "Spanish",
            "author": "Diego Sztulwark",
        },
    },
    {
        "source": "sobre-la-violencia.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Sobre la violencia",
            "language": "Spanish",
            "author": "Slavoj Zizek",
        },
    },
    {
        "source": "the-stack.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "The Stack",
            "language": "English",
            "author": "Benjamin H. Bratton",
        },
    },
    {
        "source": "tres-catastrofes.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Tres catástrofes",
            "language": "Spanish",
            "author": "Étienne Balibar",
        },
    },
    {
        "source": "vida-de-perro-notas-sobre-metodo-de-investigacion-politica.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Vida de perro: notas sobre método de investigación política",
            "language": "Spanish",
            "author": "Marcela Pelerman",
        },
    },
    {
        "source": "vigilar-y-castigar.pdf",
        "metadata": {
            "collection": "ancora",
            "title": "Vigilar y castigar",
            "language": "Spanish",
            "author": "Michel Foucault",
        },
    },
]


ancora_file_items = [FileItem(**f) for f in files]
