from pathlib import Path
from datetime import date

from google.cloud import bigquery

from src.bigquery_client import get_bigquery_client
from src.postgres_client import get_postgres_connection


def run_daily_stats_pipeline(start_date: date, end_date: date):

    # 1. EXTRACT: BigQuery'den verileri çek
    client = get_bigquery_client()

    sql_path = Path("sql/daily_stats.sql")
    query = sql_path.read_text(encoding="utf-8")

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "start_date", "STRING", start_date.strftime("%Y%m%d")
            ),
            bigquery.ScalarQueryParameter(
                "end_date", "STRING", end_date.strftime("%Y%m%d")
            ),
        ]
    )

    result = client.query(query, job_config=job_config).result()

    # 2. TRANSFORM: Sonuçları PostgreSQL'e uygun hale getir
    rows = [
        (
            row["date"],
            row["dau"],
            row["successful_players"],
            row["failed_players"],
        )
        for row in result
    ]

    if not rows:
        print("Belirtilen tarih aralığında veri bulunamadı.")
        return

    # 3. LOAD: PostgreSQL'e aktar
    insert_query = """
        INSERT INTO daily_game_stats
            (date, dau, successful_players, failed_players)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (date)
        DO UPDATE SET
            dau = EXCLUDED.dau,
            successful_players = EXCLUDED.successful_players,
            failed_players = EXCLUDED.failed_players;
    """

    with get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_query, rows)

    print(f"{len(rows)} günlük istatistik PostgreSQL'e aktarıldı!")



def get_available_date_range():
    client = get_bigquery_client()

    query = Path("sql/available_dates.sql").read_text(
        encoding="utf-8"
    )

    rows = list(client.query(query).result())

    if not rows:
        raise ValueError("BigQuery'de günlük veri bulunamadı.")

    start_date = rows[0]["event_date"]
    end_date = rows[-1]["event_date"]

    return start_date, end_date



def get_last_processed_date():
    query = """
        SELECT MAX(date)
        FROM daily_game_stats;
    """

    with get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

    return result[0]