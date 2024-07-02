import requests
import sqlite3


class LocalDatabase:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()

    def insert_user(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
        ''', (data['username'], data['password'], data['email']))
        self.conn.commit()

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

    def update_user(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users
            SET username=?, password=?, email=?
            WHERE id=?
        ''', (data['username'], data['password'], data['email'], data['id']))
        self.conn.commit()

    def delete_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users')
        self.conn.commit()


class CRUD:
    @staticmethod
    def get(endpoint, database):
        response = requests.get(endpoint)
        database.insert_user(response.text)
        print("Users from API added to the local database.")

    @staticmethod
    def post(endpoint, data, database):
        existing_user = database.get_user_by_id(data.get('id'))

        if existing_user:
            response = requests.put(endpoint, json=data)
            if response.status_code == 200:
                user_id = response.json().get('id')
                print(f"User with ID {user_id} updated successfully on the API.")
                database.update_user(response.json())
        else:
            response = requests.post(endpoint, json=data)
            if response.status_code == 201:
                user_id = response.json().get('id')
                print(f"User with ID {user_id} added successfully to the API.")
                database.insert_user(response.json())

    @staticmethod
    def put(endpoint, data, database):
        response = requests.put(endpoint, json=data)
        if response.status_code == 200:
            user_id = response.json().get('id')
            print(f"User with ID {user_id} updated successfully on the API.")
            database.insert_user(response.json())

    @staticmethod
    def delete(endpoint, database):
        response = requests.delete(endpoint)
        if response.status_code == 200:
            print("Users deleted successfully on the API.")
            database.delete_all_users()


new_data = {
    'username': "John Doe",
    'password': "zaq1@WSX",
    'email': "example@example.com"
}

local_database = LocalDatabase('local_db.sqlite')

CRUD.get('https://jsonplaceholder.typicode.com/', local_database)
CRUD.post('https://jsonplaceholder.typicode.com/', new_data, local_database)
CRUD.put('https://jsonplaceholder.typicode.com/', new_data, local_database)
CRUD.delete('https://jsonplaceholder.typicode.com/', local_database)
