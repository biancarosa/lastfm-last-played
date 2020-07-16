def test_get_lastest_songs(client):
    rv = client.get('/biahll/latest-songs')
    assert rv.status_code == 200
    assert len(rv.json['track']) != None
