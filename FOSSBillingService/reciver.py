import json, os, time, requests, pika

from deepdiff import DeepDiff
from requests.auth import HTTPBasicAuth
from rich import print
from rich.console import Console
from dotenv import load_dotenv
from pika import BlockingConnection, ConnectionParameters

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

    def send_request(self, path, params=None):
        api_url = self.get_full_api_url(path)
        print(api_url)
        response = requests.post(api_url, auth=HTTPBasicAuth(self.admin, self.password), data=params)
        return response

class FOSSbillingClass:
    def __init__(self):
        pass

class reciverFOSS:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.console = Console()

    def setup(self):
        self.console.log("Setting up connection and channel...")
        self.connection = BlockingConnection(ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.console.log("Connection and channel established.")

    def callback(self, ch, method, properties, body):
        self.console.log(f"Received message: {body}")
        
        env_loader = EnvironmentLoader()
        api_url = env_loader.get_env_variable('API_URL')
        admin = env_loader.get_env_variable('USERNAME_ADMIN')
        password = env_loader.get_env_variable('PASSWORD')
        
        api_client = APIClient(api_url, admin, password)
        api_path_create = '/admin/client/create'
        api_path_delete = '/admin/client/delete'
        api_path_change_password = '/admin/client/change_password'
        api_path_update = '/admin/client/update'
        
        # params = {
        #     'id': '1',
        #     'email': 'antoine.goetuys@student.ehb.de'
        # }
        
        # response1 = api_client.send_request(api_path_update, params=params)
        # print(response1.text)
        email = 'antoine.goetuys@student.ehb.be'
        params = {
            'email': email,
            'first_name': email.split('@')[0],
        }
        
        self.console.log(f"Sending request with params: {params}")
        response1 = api_client.send_request(api_path_create, params=params)
        self.console.log(f"Response: {response1.text}")

    def consume(self):
        self.console.log("Starting to consume messages...")
        self.channel.basic_consume(queue='FOSSbilling', on_message_callback=self.callback, auto_ack=True)
        self.console.log('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.console.log("Closing connection...")
        self.connection.close()
        self.console.log("Connection closed.")

if __name__ == '__main__':
    r = reciverFOSS()
    r.setup()
    try:
        r.consume()
    except KeyboardInterrupt:
        r.close()