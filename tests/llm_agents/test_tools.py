from datetime import datetime, timedelta

import pytest

from por.llm_agents.tools import _localize_datetime, compute_sun_placement


SANTIAGO_LATITUDE = -33.4489
SANTIAGO_LONGITUDE = -70.6693


@pytest.mark.parametrize(
    ("birth_datetime", "expected_offset"),
    [
        pytest.param(
            datetime(1989, 1, 15, 12),
            timedelta(hours=-3),
            id="1989-summer",
        ),
        pytest.param(
            datetime(1989, 7, 15, 12),
            timedelta(hours=-4),
            id="1989-winter",
        ),
        pytest.param(
            datetime(1950, 1, 15, 12),
            timedelta(hours=-4),
            id="1950-summer",
        ),
        pytest.param(
            datetime(1950, 7, 15, 12),
            timedelta(hours=-4),
            id="1950-winter",
        ),
    ],
)
def test_localize_datetime_uses_historical_santiago_offset(
    birth_datetime: datetime,
    expected_offset: timedelta,
) -> None:
    localized_datetime, timezone_name = _localize_datetime(
        birth_datetime,
        SANTIAGO_LATITUDE,
        SANTIAGO_LONGITUDE,
    )

    assert localized_datetime.utcoffset() == expected_offset
    assert timezone_name == "America/Santiago"


@pytest.mark.parametrize(
    ("year", "month", "day", "expected_sign"),
    [
        pytest.param(1990, 1, 1, "Capricorn", id="capricorn"),
        pytest.param(2000, 8, 1, "Leo", id="leo"),
    ],
)
def test_compute_sun_placement(
    year: int,
    month: int,
    day: int,
    expected_sign: str,
) -> None:
    placement = compute_sun_placement(year, month, day)

    assert placement["sign"] == expected_sign
