import os
import unittest
import requests
import uuid
import random
import string

class AuthTest(unittest.TestCase):
    host: str = os.getenv('APP_HOST', '127.0.0.1')
    port: str = os.getenv('APP_PORT', '8181')
    base_url: str = 'http://' + host + ":" + port

    demo_admin: dict = {
        "username": "tests_auth_admin",
        "password": "admin"
    }
    
    demo_user: dict = {
        "username": "tests_auth_user",
        "password": "user"
    }

    tmp_user_token: str
    tmp_admin_id: int

    def test_01_get_auth_token(self) -> None:
        url = self.base_url + '/auth/login'

        # make request
        user_response = requests.post(url, json=self.demo_user)
        admin_response = requests.post(url, json=self.demo_admin)

        # check status code
        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(admin_response.status_code, 200)

        # check response content
        user_response_data = user_response.json()
        admin_response_data = admin_response.json()

        self.assertIn('token', user_response_data)
        self.assertIn('token', admin_response_data)

        self.assertIsInstance(user_response_data['token'], str)
        self.assertIsInstance(admin_response_data['token'], str)

        expected_token_length = 22
        self.assertEqual(len(user_response_data['token']), expected_token_length)
        self.assertEqual(len(admin_response_data['token']), expected_token_length)

        # set token to the users
        self.demo_user['token'] = user_response_data['token']
        self.demo_admin['token']  = admin_response_data['token']

    def test_02_revoke_my_token(self) -> None:
        # get a token
        url = self.base_url + '/auth/login'

        # make request
        user_response = requests.post(url, json=self.demo_user)
        user_response_data = user_response.json()
        token = user_response_data['token']

        auth_url = self.base_url + '/auth/token'
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }

        revoke_response = requests.delete(auth_url, headers=headers)

        # validate response
        self.assertEqual(revoke_response.status_code, 200)
        self.assertEqual(revoke_response.json(), {'status': 'OK'})

        # try to use revoked token
        new_revoke_response = requests.delete(auth_url, headers=headers)
        self.assertEqual(new_revoke_response.status_code, 401)

    def test_03_get_my_data(self) -> None:
        url = self.base_url + '/auth'
        headers = {
            "Authorization": "Bearer " + self.demo_user["token"],
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        # check status code
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        # check result fields
        self.assertIn('id', response_data)
        self.assertIn('username', response_data)
        self.assertIn('email', response_data)
        self.assertIn('role', response_data)
        self.assertIn('active', response_data)
        self.assertIn('created_at', response_data)
        self.assertIn('updated_at', response_data)
        self.assertNotIn('password', response_data)

    def test_04_update_my_data(self) -> None:
        auth_url = self.base_url + '/auth'
        username = self.get_random_username()
        data = {"email": username + "@demo.test"}
        headers = {
            "Authorization": "Bearer " + self.demo_user["token"],
            "Content-Type": "application/json"
        }
        response = requests.put(auth_url, json=data, headers=headers)

        # check status code
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        # check result fields
        self.assertIn('email', response_data)
        self.assertIn('id', response_data)
        self.assertNotIn('password', response_data)

        # check if changes where made
        self.assertEqual(response_data['email'], data["email"])

        # revert changes
        data = {"email": "test_user@bookit.demo"}
        response = requests.put(auth_url, json=data, headers=headers)

    def test_05_get_data(self) -> None:
        url = self.base_url + '/auth/manage/4'
        headers = {
            "Authorization": "Bearer " + self.demo_admin["token"],
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        # check status code
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        # check result fields
        self.assertIn('id', response_data)
        self.assertIn('username', response_data)
        self.assertIn('email', response_data)
        self.assertIn('role', response_data)
        self.assertIn('active', response_data)
        self.assertIn('created_at', response_data)
        self.assertIn('updated_at', response_data)
        self.assertNotIn('password', response_data)

        headers = {
            "Authorization": "Bearer " + self.demo_user["token"],
            "Content-Type": "application/json"
        }
        new_response = requests.get(url, headers=headers)

        # check request made with a token with user permissions
        self.assertEqual(new_response.status_code, 401)

    def test_06_get_users_list(self) -> None:
        url = self.base_url + '/auth/manage/list?p=1&limit=1'
        headers = {
            "Authorization": "Bearer " + self.demo_admin["token"],
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        # check status code
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIsInstance(response_data, list)

        # check pagination
        self.assertEqual(len(response_data), 1)
        user = response_data[0]
        self.assertIn('id', user)

    def test_07_add_user(self) -> None:
        auth_url = self.base_url + '/auth/manage'
        headers = {
            "Authorization": "Bearer " + self.demo_admin["token"],
            "Content-Type": "application/json"
        }

        # create new user
        new_username = str(uuid.uuid4())
        data = {
            "active": 1,
            "password": "user",
            "role": "user",
            "username": new_username
        }
        
        response = requests.post(auth_url, json=data, headers=headers)

        self.assertEqual(response.status_code, 201)

        response_data = response.json()

        self.assertIn('user_id', response_data)

    def test_08_update_data(self) -> None:
        auth_url = self.base_url + '/auth/manage/4'
        username = self.get_random_username()
        data = {"email": username + "@demo.test"}
        headers = {
            "Authorization": "Bearer " + self.demo_admin["token"],
            "Content-Type": "application/json"
        }
        response = requests.put(auth_url, json=data, headers=headers)

        # check status code
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        # check result fields
        self.assertIn('email', response_data)
        self.assertIn('id', response_data)
        self.assertNotIn('password', response_data)

        # check if changes where made
        self.assertEqual(response_data['email'], data["email"])

        # revert changes
        data = {"email": "test_user@bookit.demo"}
        response = requests.put(auth_url, json=data, headers=headers)

    def test_09_close_my_account(self) -> None:
        auth_url = self.base_url + '/auth'
        new_user = self.add_user()
        headers = {
            "Authorization": "Bearer " + new_user["token"],
            "Content-Type": "application/json"
        }
        response = requests.delete(auth_url, headers=headers)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn('user_id', response_data)
        self.assertEqual(response_data, {'status': 'OK', 'user_id': new_user["id"]})

        # try to do a request again
        response = requests.delete(auth_url, headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_10_close_account(self) -> None:
        new_user = self.add_user()
        auth_url = self.base_url + '/auth/manage/' + str(new_user["id"])
        headers = {
            "Authorization": "Bearer " + self.demo_admin["token"],
            "Content-Type": "application/json"
        }
        response = requests.get(auth_url, headers=headers)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertIn('id', response_data)

    def get_random_username(self) -> str:
        username_length = random.randint(5, 10)
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(username_length))
        return username
    
    def add_user(self) -> dict:
        auth_url = self.base_url + '/auth/manage'
        headers = {
            "Authorization": "Bearer " + self.demo_admin["token"],
            "Content-Type": "application/json"
        }

        # create new user
        new_username = str(uuid.uuid4())
        data = {
            "active": 1,
            "password": "user",
            "role": "user",
            "username": new_username
        }
        
        # create user fetch id
        response = requests.post(auth_url, json=data, headers=headers)
        response_data = response.json()
        data["id"] = response_data['user_id']

        # get this user token
        user_response = requests.post(self.base_url + '/auth/login', json={"username": new_username, "password": "user"})
        user_response_data = user_response.json()
        data["token"] = user_response_data['token']

        return data

if __name__ == '__main__':
    unittest.main()
