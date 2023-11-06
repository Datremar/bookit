import os
import unittest
import requests

class Test(unittest.TestCase):
    host: str = os.getenv('APP_HOST', '127.0.0.1')
    port: str = os.getenv('APP_PORT', '8181')
    base_url: str = 'http://' + host + ":" + port

    def test_host_url(self):
        url = self.base_url + '/healthcheck/'
        try:
            response = requests.get(url)
            self.assertEqual(response.status_code, 200)
            response_data = response.json()
            self.assertIn('uptime', response_data)
        except Exception:
            raise Exception("API is offline!")


    def test_get_auth_token(self):
        url = self.base_url + '/auth/login'
        data = {
            "username": "admin",
            "password": "admin"
        }

        # Send the request
        response = requests.post(url, json=data)

        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the response is JSON and get the data
        response_data = response.json()

        # Assert that the 'token' key is in the response
        self.assertIn('token', response_data)

        # Check if the token is a string and has the expected length (e.g., 22 characters)
        token = response_data['token']
        self.assertIsInstance(token, str)
        expected_token_length = 22
        self.assertEqual(len(token), expected_token_length)

if __name__ == '__main__':
    unittest.main()
