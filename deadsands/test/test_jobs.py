import pytest

from site_tools import jobs


@pytest.mark.parametrize('value, step, expected', [
    (0, 50, 50),
    (49, 50, 50),
    (51, 50, 50),
    (99, 50, 100),
    (100, 50, 100),
    (101, 50, 100),
    (124, 50, 100),
    (125, 50, 100),
    (126, 50, 150),
    (150, 50, 150),
    (151, 50, 150),
    (199, 50, 200)
])
def test_nearest(value, step, expected):
    assert jobs.nearest(value, step=step) == expected
