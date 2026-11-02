from fastapi.testclient import TestClient
from src.api.main import app
from unittest.mock import patch
from datetime import date

client = TestClient(app)


def test_health_endpoint():
    response=client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_summary_endpoint():
    with patch("src.api.routes.stats.get_postgres_connection") as mock_connection:
        mock_cursor = mock_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value

        mock_cursor.fetchone.return_value = (10, 4500, 1200, 800, 450.0)

        response = client.get("/stats/summary")
        assert response.status_code == 200
        assert response.json()["total_days"] == 10


def test_summary_invalid_date_range():
    response = client.get(
        "/stats/summary?start_date=2018-07-20&end_date=2018-07-10"
    )

    assert response.status_code == 400


def test_summary_empty_data():
    with patch("src.api.routes.stats.get_postgres_connection") as mock_connection:
        mock_cursor = mock_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value

        mock_cursor.fetchone.return_value = (0, None, None, None, None)

        response = client.get("/stats/summary")
        assert response.json()["total_days"] == 0


def test_daily_endpoint():
    with patch("src.api.routes.stats.get_postgres_connection") as mock_connection:
        mock_cursor = mock_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value

        mock_cursor.fetchall.return_value = [
            (date(2018, 7, 1), 500, 300, 200),
            (date(2018, 7, 2), 600, 400, 200),
        ]

        response = client.get("/stats/daily")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["dau"] == 500
        assert response.json()[1]["successful_players"] == 400


def test_weekly_endpoint():
    with patch("src.api.routes.stats.get_postgres_connection") as mock_connection:
        mock_cursor = mock_connection.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value

        mock_cursor.fetchall.return_value = [
            (date(2018, 6, 11), 482.0,515,449),
            
        ]

        response = client.get("/stats/weekly")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["avg_dau"] == 482.0