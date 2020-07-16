import os

from unittest.mock import patch


@patch.dict(os.environ, {"LASTFM_API_KEY": ''})
def test_without_api_key(client):
    rv = client.get('/user/latest-songs')
    assert rv.json['message'] == 'INTERNAL_ERROR'
    assert rv.status_code == 500


@patch.dict(os.environ, {"LASTFM_API_KEY": 'something new'})
@patch('requests.get', side_effect=[Exception()])
def test_get_with_exception(requests, client):
    rv = client.get('/user/latest-songs')
    assert rv.json['message'] == 'INTERNAL_ERROR'
    assert rv.status_code == 500


@patch.dict(os.environ, {"LASTFM_API_KEY": 'something old'})
@patch('requests.get')
def test_get_with_success(mock_get, client):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = ['something boworred']
    rv = client.get('/user/latest-songs')
    assert rv.json == mock_get.return_value.json.return_value
    assert rv.status_code == mock_get.return_value.status_code
