from datetime import timedelta

from src.pipeline.daily_stats import (
    get_available_date_range,
    get_last_processed_date,
    run_daily_stats_pipeline,
)

from src.pipeline.data_quality import check_daily_stats_quality


def main():
    first_date, last_date = get_available_date_range()
    last_processed_date = get_last_processed_date()

    if last_processed_date is None:
        start_date = first_date
    else:
        start_date = last_processed_date + timedelta(days=1)

    if start_date > last_date:
        print("Yeni veri bulunamadı. PostgreSQL güncel.")
    else:
        print(f"İşlenecek tarih aralığı: {start_date} - {last_date}")
        run_daily_stats_pipeline(start_date, last_date)

    check_daily_stats_quality()


if __name__ == "__main__":
    main()