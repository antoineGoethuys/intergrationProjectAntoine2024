import os
import requests
from requests.auth import HTTPBasicAuth
from rich import print
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
api_url = os.getenv('API_URL')
# api_path = '/admin/client/get_list'
api_path = '/admin/activity/log_get_list'
admin = os.getenv('USERNAME_ADMIN')
user = os.getenv('USERNAME_CLIENT')
password = os.getenv('PASSWORD')

api = f"{api_url}{api_path}"
print(api)

# Send the request with Basic Authentication
response = (
	requests.post(
		api,
		auth = HTTPBasicAuth(
			admin,
			password
			)
		)
)

# Check the response
try:
	if response.status_code == 201:
		print('Product created successfully:', response.json())
	elif response.status_code == 200:
		print('file:', response.json())
	else:
		print('Product not found:', response.status_code)
except requests.exceptions.JSONDecodeError:
	print('Response is not in JSON format:', response.text)
