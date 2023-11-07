import os
import unittest
import requests

class HealthTest(unittest.TestCase):
    host: str = os.getenv('APP_HOST', '127.0.0.1')
    port: str = os.getenv('APP_PORT', '8181')
    base_url: str = 'http://' + host + ":" + port

    def test_host_url(self) -> None:
        url = self.base_url + '/healthcheck'
        try:
            response = requests.get(url)
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertIn('uptime', response_data)
        except Exception:
            raise Exception("API is offline!")

if __name__ == '__main__':
    unittest.main()
