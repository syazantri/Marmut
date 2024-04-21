import psycopg2, os
from psycopg2 import Error

try:
    # Connect ke db
    connection = psycopg2.connect(user=os.getenv('DATABASE_USER'),
                                  password=os.getenv('DATABASE_PASSWORD'),
                                  host=os.getenv('DATABASE_HOST'),
                                  port=os.getenv('DATABASE_PORT'),
                                  database=os.getenv('DATABASE_NAME'))

    # Buat cursor buat operasiin db
    cursor = connection.cursor()

    # Print detail postgre 
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    # Coba query
    cursor.execute("SELECT version();")

    # Fetch result
    record = cursor.fetchall()
    print("You are connected to - ", record, "\n")

    # Masuk ke schema A5
    cursor.execute("SET search_path TO A5")
  
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

# Tutup connection
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")