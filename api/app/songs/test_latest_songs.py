"""Tests for the latest_songs module."""
import os
from unittest.mock import patch

import pytest
from flask import Flask

from app.songs.latest_songs import _get_latest_song, route

@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    return app

@pytest.fixture
def mock_lastfm_response():
    """Mock Last.fm API response."""
    return {
        'recenttracks': {
            'track': [{
                'name': 'Test Song',
                'artist': {'#text': 'Test Artist'}
            }]
        }
    }

def test_get_latest_song_success(mock_lastfm_response):
    """Test successful song retrieval."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_lastfm_response
        mock_get.return_value.status_code = 200
        
        response_data, status_code = _get_latest_song('testuser', 'fake_api_key')
        
        assert status_code == 200
        assert response_data['track']['name'] == 'Test Song'
        assert response_data['track']['artist']['#text'] == 'Test Artist'

def test_get_latest_song_user_not_found():
    """Test when user doesn't exist."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {}
        mock_get.return_value.status_code = 200
        
        response_data, status_code = _get_latest_song('nonexistent', 'fake_api_key')
        
        assert status_code == 404
        assert response_data['message'] == 'USER_LIKELY_DOESNT_EXIST'

def test_get_latest_song_no_tracks():
    """Test when user has no tracks."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'recenttracks': {'track': []}}
        mock_get.return_value.status_code = 200
        
        response_data, status_code = _get_latest_song('notracks', 'fake_api_key')
        
        assert status_code == 200
        assert response_data['message'] == 'NO_TRACKS_FOUND'

def test_route_success(app, mock_lastfm_response):
    """Test successful route response."""
    with app.test_request_context():
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_lastfm_response
            mock_get.return_value.status_code = 200
            
            with patch.dict(os.environ, {'LASTFM_API_KEY': 'fake_api_key'}):
                response = route('testuser')
                
                assert response[1] == 200
                assert response[0].json['track']['name'] == 'Test Song'
                assert response[0].json['track']['artist']['#text'] == 'Test Artist'

def test_route_no_api_key(app):
    """Test route when API key is not set."""
    with app.test_request_context():
        with patch.dict(os.environ, {}, clear=True):
            response = route('testuser')
            
            assert response[1] == 500
            assert response[0].json['message'] == 'INTERNAL_ERROR'

def test_route_shields_io_format(app, mock_lastfm_response):
    """Test route with shields.io format."""
    with app.test_request_context('/?format=shields.io'):
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_lastfm_response
            mock_get.return_value.status_code = 200
            
            with patch.dict(os.environ, {'LASTFM_API_KEY': 'fake_api_key'}):
                response = route('testuser')
                
                assert response[1] == 200
                assert response[0].json['schemaVersion'] == 1
                assert response[0].json['label'] == 'Last.FM Last Played Song'
                assert response[0].json['message'] == 'Test Song - Test Artist'

def test_cache_behavior(mock_lastfm_response):
    """Test that the cache works as expected."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_lastfm_response
        mock_get.return_value.status_code = 200
        
        # First call should hit the API
        _get_latest_song('testuser', 'fake_api_key')
        assert mock_get.call_count == 1
        
        # Second call should use cache
        _get_latest_song('testuser', 'fake_api_key')
        assert mock_get.call_count == 1  # Still 1, no new API call
        
        # Different user should make new API call
        _get_latest_song('different_user', 'fake_api_key')
        assert mock_get.call_count == 2 