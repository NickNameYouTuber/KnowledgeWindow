import psycopg2

try:
    conn = psycopg2.connect(
        dbname="knowledge_base",
        user="postgres",
        port="5432",
        password="1234",
        host="localhost",
        options="-c client_encoding=utf8"
    )
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")