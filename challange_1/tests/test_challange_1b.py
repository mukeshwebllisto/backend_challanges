import pytest

from challange_1.challange_1b import identify_router


@pytest.fixture
def example_scenarios():
    return [
        {
            "edges": [(1, 2), (2, 3), (3, 5), (5, 2), (2, 1)],
            "expected_result": [2],
        },
        {
            "edges": [(1, 3), (3, 5), (5, 6), (6, 4), (4, 5), (5, 2), (2, 6)],
            "expected_result": [5],
        },
        {
            "edges": [(2, 4), (4, 6), (6, 2), (2, 5), (5, 6)],
            "expected_result": [2, 6],
        },
    ]


def test_identify_routers(example_scenarios):
    for test_scenario in example_scenarios:
        assert (
            identify_router(test_scenario["edges"])
            == test_scenario["expected_result"]
        )
