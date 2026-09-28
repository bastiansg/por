import pytest

from por.llm_agents.schema import ClothingDescription, PeopleDescription


@pytest.mark.parametrize(
    "description",
    [
        pytest.param("None visible", id="capitalized"),
        pytest.param("Eyeglasses; none appear behind", id="embedded-lowercase"),
        pytest.param("NONE", id="uppercase"),
    ],
)
def test_optional_description_with_none_substring_is_normalized(
    description: str,
) -> None:
    people = PeopleDescription(
        general_description="One person",
        gender_presentation="Feminine presentation",
        pose_and_posture="Standing",
        body_proportions="Average build",
        silhouette_shape="Upright silhouette",
        visible_modifications=description,
    )
    clothing = ClothingDescription(
        main_garments="A loose shirt",
        accessories=description,
        footwear=description,
    )

    assert people.visible_modifications is None
    assert clothing.accessories is None
    assert clothing.footwear is None


def test_optional_description_without_none_substring_is_preserved() -> None:
    description = "Rounded eyeglasses and hoop earrings"
    clothing = ClothingDescription(
        main_garments="A loose shirt",
        accessories=description,
    )

    assert clothing.accessories == description
