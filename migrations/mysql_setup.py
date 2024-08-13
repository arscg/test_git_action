import pymysql
from faker import Faker
import os
from urllib.parse import urlparse

# Configuration
fake = Faker()
mysql_uri = os.getenv('MYSQL_DATABASE_URI')

# Parse the URI
url = urlparse(mysql_uri)

# Extract connection parameters
host = url.hostname
port = url.port
user = url.username
password = url.password
database = url.path[1:]

# Connect to the MySQL database
conn = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

try:
    with conn.cursor() as cursor:
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price FLOAT NOT NULL
        );
        """)

        # Populate tables
        for _ in range(10):
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (fake.user_name(), fake.password()))
            cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (fake.word(), fake.random_number(digits=2)))

    conn.commit()
finally:
    conn.close()
