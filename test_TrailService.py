import pytest
from main import Trails

url = 'http://localhost:5026/api'
trail_service = Trails(url)


# Test to ensure the responses are correct
def test_responses():
    res1, res2, res3, res4 = trail_service.check_responses()
    assert res1 == 200
    assert res2 == 200
    assert res3 == 200
    assert res4 == 200



