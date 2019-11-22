import pytest
import tempfile
import os
import json

from .. import main


@pytest.fixture
def client():
    db_fd, main.app.config['DATABASE'] = tempfile.mkstemp()
    main.app.config['TESTING'] = True

    with main.app.test_client() as client:
        # with main.app.app_context():
            # main.init_db()
        yield client

    os.close(db_fd)
    os.unlink(main.app.config['DATABASE'])


class TestRest:
    def test_consumable_exist(self, client):
        expected_payload = json.loads("""
        {
            "name": "antidote",
            "details": {
                "image": "http://foapi.io/resources/images/antidote",
                "type": "item",
                "subtype": "consumable",
                "addiction_rate": "0",
                "weight": "1",
                "value": "25"
            },
            "effects": [
                {
                    "when": "immediate",
                    "type": "Poison",
                    "value": "-25"
                },
                {
                    "when": "after 1 minute",
                    "type": "Poison",
                    "value": "-25"
                },
                {
                    "when": "after 2 minutes",
                    "type": "Poison",
                    "value": "-25"
                }
            ]
        }
        """)
        resp = client.get('/consumable/1')
        assert resp.status_code == 200
        assert json.loads(resp.get_data()) == expected_payload

    def test_consumable_not_exist(self, client):
        resp = client.get('/consumable/999')
        assert resp.status_code == 404

    def test_consumable_not_int(self, client):
        expected_payload = json.loads("""
        {
            "error": ""
        }
        """)
        resp = client.get('/consumable/not_existing')
        assert resp.status_code == 503
        assert json.loads(resp.get_data()) == expected_payload
