from datetime import date

from pydantic import BaseModel

from src.postgres_client import get_postgres_connection
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)


class DailyStatsResponse(BaseModel):
    date: date
    dau: int
    successful_players: int
    failed_players: int


class WeeklyStatsResponse(BaseModel):
    week_start: date
    avg_dau: float
    max_dau: int
    min_dau: int



class SummaryStatsResponse(BaseModel):
    total_days: int
    total_dau: int
    total_successful_players: int
    total_failed_players: int
    avg_dau: float 



@router.get("/daily", response_model=list[DailyStatsResponse])
def get_daily_stats(
    start_date: date | None = None,
    end_date: date | None = None
):

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Başlangıç tarihi bitiş tarihinden büyük olamaz."
        )

    query = """
        SELECT
            date,
            dau,
            successful_players,
            failed_players
        FROM daily_game_stats
        WHERE (%s::date IS NULL OR date >= %s::date)
          AND (%s::date IS NULL OR date <= %s::date)
        ORDER BY date;
    """

    with get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (start_date, start_date, end_date, end_date)
            )
            rows = cursor.fetchall()

    return [
        DailyStatsResponse(
            date=row[0],
            dau=row[1],
            successful_players=row[2],
            failed_players=row[3]
        )
        for row in rows
    ]



@router.get("/weekly", response_model=list[WeeklyStatsResponse])

def get_weekly_stats(
    start_date: date | None = None,
    end_date: date | None = None
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Başlangıç tarihi bitiş tarihinden büyük olamaz."
        )
    query = """
        SELECT
            DATE_TRUNC('week', date) AS week_start,
            ROUND(AVG(dau), 2) AS avg_dau, 
            MAX(dau) AS max_dau,
            MIN(dau) AS min_dau
        FROM daily_game_stats
        WHERE (%s::date IS NULL OR date >= %s::date)
          AND (%s::date IS NULL OR date <= %s::date)
        GROUP BY DATE_TRUNC('week', date)
        ORDER BY week_start;
    """

    with get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (start_date, start_date, end_date, end_date)
            )
            rows = cursor.fetchall()

    return [
        WeeklyStatsResponse(
            week_start=row[0],
            avg_dau=float(row[1]),
            max_dau=row[2],
            min_dau=row[3]
        )
        for row in rows
    ]




@router.get("/summary", response_model=SummaryStatsResponse)

def get_summary_stats(
    start_date: date | None = None,
    end_date: date | None = None
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Başlangıç tarihi bitiş tarihinden büyük olamaz."
        )

    query = """
        SELECT
            COUNT(*) AS total_days,
            SUM(dau) AS total_dau,
            SUM(successful_players) AS total_successful_players,
            SUM(failed_players) AS total_failed_players,
            ROUND(AVG(dau), 2) AS avg_dau
        FROM daily_game_stats
        WHERE (%s::date IS NULL OR date >= %s::date)
          AND (%s::date IS NULL OR date <= %s::date)
    """

    with get_postgres_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (start_date, start_date, end_date, end_date)
            )
            row = cursor.fetchone()

    return SummaryStatsResponse(
        total_days=row[0],
        total_dau=row[1] or 0,
        total_successful_players=row[2] or 0,
        total_failed_players=row[3] or 0,
        avg_dau=float(row[4]) if row[4] is not None else 0.0
    )
