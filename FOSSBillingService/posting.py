import json, os, time, requests, pika

from deepdiff import DeepDiff
from requests.auth import HTTPBasicAuth
from rich import print
from dotenv import load_dotenv


class EnvironmentLoader:
    def __init__(self, env_file='.env'):
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
        response = requests.post(api_url, auth=HTTPBasicAuth(self.admin, self.password))
        return response

    def responceToJson(self, response):
        try:
            response_json = response.json()
            if response_json is None:
                print('Response JSON is None')
                return None
            response_list = response_json.get("result", {}).get("list", {})
            response_dict = {
                str(index): dict(item) for index, item in enumerate(response_list)
            }
            return response_dict
        except json.JSONDecodeError:
            print('Response is not in JSON format:', response.text)
            return None
        except ValueError:
            print('Response is not in JSON format:', response.text)
            return None

    def handle_response(self, response):
        response_json = self.responceToJson(response)
        if response_json is None:
            return None

        extracted_data = {}

        for key, value in response_json.items():
            email = value["email"]
            company = value["company"]
            country = value["country"]
            postcode = value["postcode"]
            username = email.split("@")[0]
            password = username + postcode

            extracted_data[key] = {
                "email": email,
                "company": company,
                "country": country,
                "postcode": postcode,
                "username": username,
                "password": password
            }

        if response.status_code == 201:
            print('Product created successfully:', extracted_data)
        elif response.status_code == 200:
            print('Extracted data:', extracted_data)
            return extracted_data
        else:
            print('Product not found:', response.status_code)

class senderUser:
    def __init__(self):
        self.channel = None
        self.connection = None

    def setup(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange='userData',
                exchange_type='fanout',
                durable=True
            )
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection error: {e}")
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)

    def send(self, message):
        self.channel.basic_publish(
            exchange='userData',
            routing_key='',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

    def close(self):
        if self.connection:
            self.connection.close()

if __name__ == '__main__':
    env_loader = EnvironmentLoader()
    api_url = env_loader.get_env_variable('API_URL')
    admin = env_loader.get_env_variable('USERNAME_ADMIN')
    password = env_loader.get_env_variable('PASSWORD')

    s = senderUser()
    s.setup()

    api_client = APIClient(api_url, admin, password)
    api_path = '/admin/client/get_list'
    
    response1 = api_client.send_request(api_path)
    a = api_client.handle_response(response1)
    time.sleep(20)
    response2 = api_client.send_request(api_path)
    a = api_client.handle_response(response1)
    b = api_client.handle_response(response2)
    ab = DeepDiff(a, b)

    # Extract the value of the last updated item
    last_updated_value = ab.get('values_changed', {}).get('root', {}).get('new_value', None)
    message_json = json.dumps(last_updated_value)
    print('Last updated value:', message_json)
    s.send(message_json)
    s.close()