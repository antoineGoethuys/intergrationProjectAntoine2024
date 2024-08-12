import json
import os
import time
import requests

from deepdiff import DeepDiff
from requests.auth import HTTPBasicAuth
from rich import print
from dotenv import load_dotenv


class EnvironmentLoader:
	def __init__(self, env_file = '.env'):
		self.env_file = env_file
		self.load_environment()

	def load_environment(self):
		load_dotenv(self.env_file)

	def get_env_variable(self, key):
		return os.getenv(key)


class APIClient:
	def __init__(self, base_url, admin, password):
		self.base_url = base_url
		self.admin = admin
		self.password = password

	def get_full_api_url(self, path):
		return f"{self.base_url}{path}"

	def send_request(self, path):
		api_url = self.get_full_api_url(path)
		print(api_url)
		response = requests.post(api_url, auth = HTTPBasicAuth(self.admin, self.password))
		return response

	def responceToJson(self, response):
		response_json: json = response.json()
		response_list: json = (
			response_json
			.get("result", {})
			.get("list", {})
		)
		response_dict = {
			str(index):
				dict(item) for index,
			item in enumerate(response_list)
			}
		return response_dict

	def handle_response(self, response):
		try:
			response_json = self.responceToJson(response)
			extracted_data = {}

			for key, value in response_json.items():
				email = value["email"]
				company = value["company"]
				country = value["country"]
				postcode = value["postcode"]
				username = email.split("@")[0]
				password = username + postcode

				extracted_data[key] = {
					"email"   : email,
					"company" : company,
					"country" : country,
					"postcode": postcode,
					"username": username,
					"password": password
					}

			if response.status_code == 201:
				print('Product created successfully:', extracted_data)
			elif response.status_code == 200:
				# print('Extracted data:', extracted_data)
				return extracted_data
			else:
				print('Product not found:', response.status_code)
		except requests.exceptions.JSONDecodeError:
			print('Response is not in JSON format:', response.text)

if __name__ == '__main__':
	env_loader = EnvironmentLoader()
	api_url = env_loader.get_env_variable('API_URL')
	admin = env_loader.get_env_variable('USERNAME_ADMIN')
	password = env_loader.get_env_variable('PASSWORD')

	api_client = APIClient(api_url, admin, password)
	api_path = '/admin/client/get_list'
	response1 = api_client.send_request(api_path)
	time.sleep(20)
	response2 = api_client.send_request(api_path)
	a = api_client.handle_response(response1)
	b = api_client.handle_response(response2)
	ab = DeepDiff(a, b)
	print(ab)