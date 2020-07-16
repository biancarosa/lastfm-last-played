import os

from unittest.mock import patch


def test_get_healthcheck(client):
    rv = client.get('/')
    assert rv.status_code == 200
