from por.meta.schema import Material

materials = [
    Material(
        code="bioinspirado",
        interaction="Bioinspirado\nProceso: estrategia\nIntención: descubrir",
        name="Bioinspirado",
        description=(
            "Estudio de materiales, estructuras y procesos biológicos para extraer "
            "principios que puedan aplicarse al desarrollo de nuevos materiales y a "
            "otros campos."
        ),
    ),
    Material(
        code="biobasado",
        interaction="Biobasado\nProceso: composición\nIntención: regenerar",
        name="Biobasado",
        description=(
            "Se refiere a productos total o parcialmente derivados de biomasa, como "
            "plantas, árboles o animales (la biomasa puede haber sido sometida a un "
            "tratamiento físico, químico o biológico)."
        ),
    ),
    Material(
        code="biofabricado",
        interaction="Biofabricado\nProceso: metabolismo\nIntención: crecer",
        name="Biofabricado",
        description=(
            "Uso de organismos vivos y procesos biológicos para fabricar, cultivar, "
            "fermentar, crecer o elaborar nuevos materiales."
        ),
    ),
]

material_map = {material.code: material for material in materials}
