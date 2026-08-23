from collections.abc import Iterable

from por.llm_agents.schema import PBFImageDescriberOutput

__all__ = ["format_prompt"]


def _format_section(
    title: str,
    descriptions: Iterable[str | None],
) -> str:
    content = ". ".join(
        description.rstrip(".")
        for description in descriptions
        if description is not None
    )

    return f"{title}: {content}."


def format_prompt(
    description: PBFImageDescriberOutput,
    caption_header: str,
) -> str:
    scene = description.scene_description
    people = description.people_description
    clothing = description.clothing_description

    return "\n".join(
        (
            caption_header,
            _format_section(
                "Scene Description",
                (
                    scene.setting_and_background,
                    scene.composition,
                    scene.objects,
                ),
            ),
            _format_section(
                "People Description",
                (
                    people.general_description,
                    people.pose_and_posture,
                    people.body_proportions,
                    people.silhouette_shape,
                    people.facial_expression,
                    people.hair_style,
                    people.visible_modifications,
                ),
            ),
            _format_section(
                "Clothing Description",
                (
                    clothing.main_garments,
                    clothing.layering,
                    clothing.fabric_and_texture,
                    clothing.patterns_and_details,
                    clothing.accessories,
                    clothing.footwear,
                ),
            ),
        )
    )
