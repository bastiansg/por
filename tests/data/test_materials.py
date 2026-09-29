from por.data.materials import material_map, materials


def test_material_codes_match_ticket_assets() -> None:
    assert {material.code for material in materials} == {
        "BM.01",
        "GM.02",
        "MC.03",
        "AS.04",
        "MF.05",
    }
    assert set(material_map) == {material.code for material in materials}
