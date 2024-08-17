import pymysql
from faker import Faker
import os
from urllib.parse import urlparse
import random

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
database = 'ANIMOV'  # Nom de la base de données à créer

# Connect to the MySQL server (sans spécifier de base de données)
conn = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password
)

try:
    with conn.cursor() as cursor:
        # Modifier le mot de passe de 'root' pour 'admin'
        cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY 'admin';")

        # Accorder tous les privilèges à 'root'
        cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;")

        # Appliquer les modifications
        cursor.execute("FLUSH PRIVILEGES;")

        # Créer la base de données si elle n'existe pas
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        
        # Sélectionner la base de données
        cursor.execute(f"USE {database};")

        # Modifier le mot de passe de 'root' pour 'admin'
        cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY 'admin';")

        # Accorder tous les privilèges à 'root'
        cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;")

        # Appliquer les modifications
        cursor.execute("FLUSH PRIVILEGES;")
        
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

        # Ajouter un utilisateur spécifique 'arscg'
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('arscg', 'arscg'))

        # Create table `table_chevres_minute_serveur_v2`
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS table_chevres_minute_serveur_v2 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp BIGINT(20) NOT NULL,
            source INT(11) NOT NULL,
            total INT(11) NOT NULL,
            couche INT(11) NOT NULL,
            debout INT(11) NOT NULL,
            max_total INT(11) NOT NULL,
            max_couche INT(11) NOT NULL,
            max_debout INT(11) NOT NULL,
            min_total INT(11) NOT NULL,
            min_couche INT(11) NOT NULL,
            min_debout INT(11) NOT NULL,
            std_total DECIMAL(6, 3) NOT NULL,
            std_couche DECIMAL(6, 3) NOT NULL,
            std_debout DECIMAL(6, 3) NOT NULL,
            Q1_total DECIMAL(6, 3) NOT NULL,
            Q1_couche DECIMAL(6, 3) NOT NULL,
            Q1_debout DECIMAL(6, 3) NOT NULL,
            Q2_total DECIMAL(6, 3) NOT NULL,
            Q2_couche DECIMAL(6, 3) NOT NULL,
            Q2_debout DECIMAL(6, 3) NOT NULL,
            Q3_total DECIMAL(6, 3) NOT NULL,
            Q3_couche DECIMAL(6, 3) NOT NULL,
            Q3_debout DECIMAL(6, 3) NOT NULL,
            mode_total TEXT,
            mode_couche TEXT,
            mode_debout TEXT,
            nb_frames INT(11) NOT NULL
        );
        """)

        # Populate table with Faker data
        for _ in range(100):  # Nombre de lignes à insérer
            timestamp = fake.unix_time()
            source = random.randint(1, 4)
            total = random.randint(0, 100)
            couche = random.randint(0, total)
            debout = total - couche
            max_total = random.randint(total, total + 10)
            max_couche = random.randint(couche, couche + 5)
            max_debout = random.randint(debout, debout + 5)
            min_total = random.randint(total - 10, total)
            min_couche = random.randint(couche - 5, couche)
            min_debout = random.randint(debout - 5, debout)
            std_total = round(random.uniform(0, 10), 3)
            std_couche = round(random.uniform(0, 10), 3)
            std_debout = round(random.uniform(0, 10), 3)
            Q1_total = round(random.uniform(0, total / 4), 3)
            Q1_couche = round(random.uniform(0, couche / 4), 3)
            Q1_debout = round(random.uniform(0, debout / 4), 3)
            Q2_total = round(random.uniform(total / 4, total / 2), 3)
            Q2_couche = round(random.uniform(couche / 4, couche / 2), 3)
            Q2_debout = round(random.uniform(debout / 4, debout / 2), 3)
            Q3_total = round(random.uniform(total / 2, 3 * total / 4), 3)
            Q3_couche = round(random.uniform(couche / 2, 3 * couche / 4), 3)
            Q3_debout = round(random.uniform(debout / 2, 3 * debout / 4), 3)
            mode_total = str(fake.random_elements(elements=('A', 'B', 'C'), length=3))
            mode_couche = str(fake.random_elements(elements=('X', 'Y', 'Z'), length=3))
            mode_debout = str(fake.random_elements(elements=('L', 'M', 'N'), length=3))
            nb_frames = random.randint(1, 1000)

            cursor.execute("""
                INSERT INTO table_chevres_minute_serveur_v2 (
                    timestamp, source, total, couche, debout, max_total, max_couche, max_debout, 
                    min_total, min_couche, min_debout, std_total, std_couche, std_debout, 
                    Q1_total, Q1_couche, Q1_debout, Q2_total, Q2_couche, Q2_debout, 
                    Q3_total, Q3_couche, Q3_debout, mode_total, mode_couche, mode_debout, nb_frames
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                timestamp, source, total, couche, debout, max_total, max_couche, max_debout, 
                min_total, min_couche, min_debout, std_total, std_couche, std_debout, 
                Q1_total, Q1_couche, Q1_debout, Q2_total, Q2_couche, Q2_debout, 
                Q3_total, Q3_couche, Q3_debout, mode_total, mode_couche, mode_debout, nb_frames
            ))

    # Commit the changes
    conn.commit()

finally:
    conn.close()
