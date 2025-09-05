import os
from databricks import sql

HOST = os.environ.get("DATABRICKS_HOST")
HTTP_PATH = os.environ.get("DATABRICKS_SQL_HTTP_PATH")
TOKEN = os.environ.get("DATABRICKS_TOKEN")

def query_table(table: str, limit: int = 10):
    with sql.connect(server_hostname=HOST.replace("https://",""),
                     http_path=HTTP_PATH,
                     access_token=TOKEN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table} LIMIT {limit}")
            return cursor.fetchall()