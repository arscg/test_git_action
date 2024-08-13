# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:32:08 2024

@author: arsca
"""

import pymysql
from faker import Faker
import os

# Configuration
fake = Faker()
mysql_uri = os.getenv('MYSQL_DATABASE_URI')
conn = pymysql.connect(mysql_uri)

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
