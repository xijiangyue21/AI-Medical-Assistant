import unittest

from main import app


class MedicalUploadRoutesTest(unittest.TestCase):
    def test_upload_route_is_registered(self):
        route_paths = {route.path for route in app.routes}

        self.assertIn("/documents/upload", route_paths)


if __name__ == "__main__":
    unittest.main()
