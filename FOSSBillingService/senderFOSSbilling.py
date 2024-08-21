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
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.0.0.44',  # Replace with the actual IP address of the RabbitMQ server
            port=5672,  # Default RabbitMQ port
            credentials=pika.PlainCredentials('guest', 'guest')  # Update with your RabbitMQ credentials
        ))
        self.channel = self.connection.channel()

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
    
    while True:
        user = None
        user1 = None
        response1 = api_client.send_request(api_path)
        time.sleep(5)
        response2 = api_client.send_request(api_path)
        a = api_client.handle_response(response1)
        b = api_client.handle_response(response2)
        ab = DeepDiff(a, b)
        
        if 'values_changed' in ab:
            print('Values changed:', ab['values_changed'])
            for key, change in ab['values_changed'].items():
                root_key = key.split('root[')[-1].split(']')[0].strip("'")
                user_data = b[root_key]
                user = {
                    'action': 'update',
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'company': user_data['company'],
                    'country': user_data['country'],
                    'postcode': user_data['postcode'],
                    'password': user_data['password']
                }
                # if "email" in key:
                #     user1 = {
                #         'action': 'remove',
                #         'username': user_data['username'],
                #         'email': user_data['email'],
                #         'company': user_data['company'],
                #         'country': user_data['country'],
                #         'postcode': user_data['postcode'],
                #         'password': user_data['password']
                #     }    
            print('User:', user)
        
        if 'dictionary_item_added' in ab:
            print('Dictionary item added:', ab['dictionary_item_added'])
            for key in ab['dictionary_item_added']:
                root_key = key.split('root[')[-1].split(']')[0].strip("'")
                user_data = b[root_key]
                user = {
                    'action': 'add',
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'company': user_data['company'],
                    'country': user_data['country'],
                    'postcode': user_data['postcode'],
                    'password': user_data['password']
                }
            print('User:', user)
        
        if 'dictionary_item_removed' in ab:
            print('Dictionary item removed:', ab['dictionary_item_removed'])
            for key in ab['dictionary_item_removed']:
                root_key = key.split('root[')[-1].split(']')[0].strip("'")
                user_data = a[root_key]
                user = {
                    'action': 'remove',
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'company': user_data['company'],
                    'country': user_data['country'],
                    'postcode': user_data['postcode'],
                    'password': user_data['password']
                }
            print('User:', user)
        
        print('Last updated value:', ab)
        if user:
            user_json = json.dumps(user)
            s.send(user_json)
        # if user1:
        #     user_json1 = json.dumps(user1)
        #     s.send(user_json1)
    s.close()