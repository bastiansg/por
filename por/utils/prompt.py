def get_drhdr_prompt(
    physical_description: str,
    clothing_description: str,
) -> str:
    return (
        "In the style of DRHDR, an illustration of:"
        f"Physical description: {physical_description}\n"
        f"Clothing description: {clothing_description}\n"
        "The illustration contains no artist signatures, marks, or initials in the corners or elsewhere."
    )
