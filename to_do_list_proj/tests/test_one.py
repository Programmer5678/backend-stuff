import pytest

def test_juan(client):
    print(client.post("/signup", json={"username" : "username", "password" : "password"}).json())
    assert 5 == 5