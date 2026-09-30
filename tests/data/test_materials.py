from por.data.materials import material_map, materials


def test_biodesign_codes() -> None:
    assert {material.code for material in materials} == {
        "bioinspirado",
        "biobasado",
        "biofabricado",
    }
    assert set(material_map) == {material.code for material in materials}
