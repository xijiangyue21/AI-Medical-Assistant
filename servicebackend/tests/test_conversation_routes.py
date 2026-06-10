import unittest

from fastapi.testclient import TestClient

from main import app


class ConversationRoutesTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_list_route_is_registered(self):
        response = self.client.get("/conversations/list", params={"user_id": 1})

        self.assertNotEqual(response.status_code, 404)

    def test_create_route_is_registered(self):
        response = self.client.post(
            "/conversations/create",
            params={"user_id": 1},
            json={"id": "conv_test", "title": "conv_test"},
        )

        self.assertNotEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
