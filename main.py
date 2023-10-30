import requests


class CRUD:

    @staticmethod
    def get(endpoint):
        response = requests.get(endpoint)
        print(response.text)

    @staticmethod
    def post(endpoint, data):
        response = requests.post(endpoint, json=data)
        print(response.json())

    @staticmethod
    def put(endpoint, data):
        response = requests.post(endpoint, json=data)
        print(response.json())

    @staticmethod
    def delete(endpoint):
        response = requests.get(endpoint)
        print(response.status_code)


new_data = {
    'username': "John Smith",
    'password': "zaq1@WSX",
    'email': "example@example.com"
}

CRUD.get('https://jsonplaceholder.typicode.com/')
CRUD.put('https://jsonplaceholder.typicode.com/', new_data)
CRUD.post('https://jsonplaceholder.typicode.com/', new_data)
CRUD.delete('https://jsonplaceholder.typicode.com/')
