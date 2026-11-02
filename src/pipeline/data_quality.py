from src.postgres_client import get_postgres_connection


def check_daily_stats_quality():
    query = """
        SELECT
            COUNT(*) AS total_days,

            COUNT(*) FILTER (
                WHERE dau = 0
            ) AS zero_dau_days,

            COUNT(*) FILTER (
                WHERE successful_players > dau
                   OR failed_players > dau
            ) AS invalid_player_counts

        FROM daily_game_stats;
    """

    with get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

    total_days, zero_dau_days, invalid_player_counts = result

    if total_days == 0:
        raise ValueError("Veritabanında günlük istatistik bulunamadı.")

    if zero_dau_days > 0 or invalid_player_counts > 0:
        raise ValueError(
            "Veri kalitesi kontrolü başarısız! "
            f"Sıfır DAU: {zero_dau_days}, "
            f"Geçersiz oyuncu sayısı: {invalid_player_counts}"
        )

    print(f"Veri kalitesi kontrolü başarılı: {total_days} gün.")