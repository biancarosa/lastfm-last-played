import pytest
import faker
import os
import tempfile


from app.main import app as flask_app


@pytest.fixture
def fake():
    return faker.Faker()


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def lastfm_response():
    return {
        "recenttracks": {
            "@attr": {
                "page": "1",
                "perPage": "1",
                "total": "229279",
                "totalPages": "229279",
                "user": "biahll"
            },
            "track": [
                {
                    "@attr": {
                        "nowplaying": "true"
                    },
                    "album": {
                        "#text": "My My My!",
                        "mbid": ""
                    },
                    "artist": {
                        "#text": "Mother's Daughter",
                        "mbid": ""
                    },
                    "image": [
                        {
                            "#text": "https: //lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
                            "size": "small"
                        },
                        {
                            "#text": "https: //lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
                            "size": "medium"
                        },
                        {
                            "#text": "https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
                            "size": "large"
                        },
                        {
                            "#text": "https: //lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                            "size": "extralarge"
                        }
                    ],
                    "mbid": "",
                    "name": "My My My!",
                    "streamable": "0",
                    "url": "https: //www.last.fm/music/Mother%27s+Daughter/_/My+My+My!"
                },
                {
                    "album": {
                        "#text": "Glory Days (Japan Edition)",
                        "mbid": ""
                    },
                    "artist": {
                        "#text": "Little Mix",
                        "mbid": "38f59974-2f4d-4bfa-b2e3-d2696de1b675"
                    },
                    "date": {
                        "#text": "16 Jul 2020,        22: 30",
                        "uts": "1594938632"
                    },
                    "image": [
                        {
                            "#text": "https: //lastfm.freetls.fastly.net/i/u/34s/9e824c0b80bbf5c24807f22d081566c4.jpg",
                            "size": "small"
                        },
                        {
                            "#text": "https://lastfm.freetls.fastly.net/i/u/64s/9e824c0b80bbf5c24807f22d081566c4.jpg",
                            "size": "medium"
                        },
                        {
                            "#text": "https://lastfm.freetls.fastly.net/i/u/174s/9e824c0b80bbf5c24807f22d081566c4.jpg",
                            "size": "large"
                        },
                        {
                            "#text": "https: //lastfm.freetls.fastly.net/i/u/300x300/9e824c0b80bbf5c24807f22d081566c4.jpg",
                            "size": "extralarge"
                        }
                    ],
                    "mbid": "02930d7b-3e67-41c5-9d6e-ad593228d441",
                    "name": "Shout Out to My Ex",
                    "streamable": "0",
                    "url": "https://www.last.fm/music/Little+Mix/_/Shout+Out+to+My+Ex"
                }
            ]
        }
    }
