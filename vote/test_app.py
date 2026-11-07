import json
from unittest.mock import Mock

import pytest
import app as vote_app


@pytest.fixture
def client():
    vote_app.app.config.update(TESTING=True)
    with vote_app.app.test_client() as client:
        yield client


def test_vote_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert vote_app.option_a.encode() in response.data
    assert vote_app.option_b.encode() in response.data
    assert "voter_id=" in response.headers["Set-Cookie"]


@pytest.mark.parametrize("choice", ["a", "b"])
def test_vote_is_queued(client, monkeypatch, choice):
    redis = Mock()
    monkeypatch.setattr(vote_app, "get_redis", lambda: redis)
    client.set_cookie("voter_id", "test-voter")
    response = client.post("/", data={"vote": choice})
    assert response.status_code == 200
    redis.rpush.assert_called_once()
    queue, payload = redis.rpush.call_args.args
    assert queue == "votes"
    assert json.loads(payload) == {"voter_id": "test-voter", "vote": choice}
