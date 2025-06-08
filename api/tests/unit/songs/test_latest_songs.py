import os
import requests

from unittest.mock import patch


@patch.dict(os.environ, {"LASTFM_API_KEY": ''})
def test_without_api_key(client):
    rv = client.get('/user/latest-song')
    assert rv.json['message'] == 'INTERNAL_ERROR'
    assert rv.status_code == 500


@patch.dict(os.environ, {"LASTFM_API_KEY": 'something new'})
@patch('requests.get', side_effect=[Exception()])
def test_get_with_exception(requests, client):
    rv = client.get('/user/latest-song')
    assert rv.json['message'] == 'INTERNAL_ERROR'
    assert rv.status_code == 500


@patch.dict(os.environ, {"LASTFM_API_KEY": 'something old'})
@patch('requests.get', side_effect=requests.exceptions.Timeout())
def test_get_with_timeout(mock_get, client):
    rv = client.get('/user/latest-song')
    assert rv.json['message'] == 'TIMEOUT'
    assert rv.status_code == 504


@patch.dict(os.environ, {"LASTFM_API_KEY": 'something old'})
@patch('requests.get')
def test_get_with_success(mock_get, client, lastfm_response):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = lastfm_response
    rv = client.get('/user/latest-song')
    assert rv.json == {'track': lastfm_response['recenttracks']['track'][0]}
    assert rv.status_code == mock_get.return_value.status_code


@patch.dict(os.environ, {"LASTFM_API_KEY": 'something old'})
@patch('requests.get')
def test_get_with_success_and_different_format(mock_get, client, lastfm_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = lastfm_response
    rv = client.get('/user/latest-song?format=shields.io')
    song = lastfm_response['recenttracks']['track'][0]['name'] 
    artist = lastfm_response['recenttracks']['track'][0]['artist']['#text'] 
    
    assert rv.json == {
        'schemaVersion': 1,
        'label': 'Last.FM Last Played Song',
        'message': f"{song} - {artist}"
    }
    assert rv.status_code == mock_get.return_value.status_code

@patch.dict(os.environ, {"LASTFM_API_KEY": 'something old'})
@patch('requests.get')
def test_get_with_success_no_tracks(mock_get, client, lastfm_empty_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = lastfm_empty_response
    rv = client.get('/user/latest-song')

    assert rv.status_code == 200
    assert rv.json == {
        'message': 'NO_TRACKS_FOUND'
    }

@patch.dict(os.environ, {"LASTFM_API_KEY": 'something old'})
@patch('requests.get')
def test_get_with_error_user_not_found_tracks(mock_get, client, lastfm_no_recent_tracks_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = lastfm_no_recent_tracks_response
    rv = client.get('/user/latest-song')

    assert rv.status_code == 404
    assert rv.json == {
        'message': 'USER_LIKELY_DOESNT_EXIST'
    }
