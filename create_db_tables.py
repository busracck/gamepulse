from pathlib import Path
from src.postgres_client import get_postgres_connection

sql_path = Path("sql/create_tables.sql")

query = sql_path.read_text(encoding="utf-8")

with get_postgres_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(query)

print("Tablo başarıyla oluşturuldu!")