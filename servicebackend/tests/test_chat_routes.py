import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from main import app
from app.api import chat


class ChatRoutesTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_send_route_is_registered(self):
        response = self.client.post(
            "/chat/send",
            json={
                "user_id": "user_1",
                "message": "牙痛怎么办",
                "thread_id": "conv_test",
            },
        )

        self.assertNotEqual(response.status_code, 404)

    def test_send_returns_non_empty_ai_message(self):
        class FakeQuery:
            def filter(self, *args, **kwargs):
                return self

            def first(self):
                return None

        class FakeDb:
            def query(self, *args, **kwargs):
                return FakeQuery()

        class FakeGraph:
            def invoke(self, *args, **kwargs):
                return {
                    "messages": [
                        AIMessage(content="建议先用温盐水漱口，并尽快看牙科。"),
                        AIMessage(content=""),
                    ]
                }

        app.dependency_overrides[chat.get_current_user] = lambda: object()
        app.dependency_overrides[chat.get_postgres_db] = lambda: FakeDb()

        with patch.object(chat, "create_medical_agent_system", return_value=FakeGraph()):
            response = self.client.post(
                "/chat/send",
                json={
                    "user_id": "user_1",
                    "message": "牙痛怎么办",
                    "thread_id": "conv_test",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "建议先用温盐水漱口，并尽快看牙科。")


if __name__ == "__main__":
    unittest.main()
