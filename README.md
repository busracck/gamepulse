
# GamePulse — Mobile Game Analytics Platform

GamePulse is an end-to-end data analytics project that transforms raw mobile game event data into actionable insights through an interactive dashboard.

## Project Overview

The project analyzes historical Firebase Analytics event data from the Flood-It mobile game.

It demonstrates a complete data workflow:

- Extracting event data from Google BigQuery
- Transforming and validating data using Python
- Storing aggregated metrics in PostgreSQL
- Exposing analytics through FastAPI REST endpoints
- Visualizing player activity and performance using React

## Tech Stack

| Layer | Technologies |
|---|---|
| Data Source | Google BigQuery |
| Data Processing | Python, Pandas, SQL |
| Database | PostgreSQL |
| Backend | FastAPI, Pydantic |
| Frontend | React, Vite, Recharts |
| Testing | Pytest, FastAPI TestClient |
| Version Control | Git, GitHub |


## System Architecture

```text
Google BigQuery
      |
      | Raw Firebase Events
      v
Python ETL Pipeline
      |
      | Data Cleaning & Aggregation
      | Data Quality Checks
      v
PostgreSQL
      |
      | SQL Queries
      v
FastAPI REST API
      |
      | JSON Responses
      v
React Dashboard
      |
      v
Interactive Analytics & Visualizations
```

### Data Pipeline

1. **Extract:** Retrieve historical Flood-It event data from Google BigQuery.
2. **Transform:** Calculate daily active users and player success/failure metrics.
3. **Load:** Store aggregated statistics in PostgreSQL using UPSERT operations.
4. **Serve:** Provide filtered daily, weekly, and summary statistics through FastAPI.
5. **Visualize:** Display interactive charts and date-based analytics in React.



## API Endpoints

GamePulse provides REST API endpoints built with FastAPI.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/stats/daily` | Retrieve daily player statistics |
| GET | `/stats/weekly` | Retrieve weekly DAU statistics |
| GET | `/stats/summary` | Retrieve aggregated player metrics |

### Date Filtering

All statistics endpoints support optional `start_date` and `end_date` query parameters.

Example:

```http
GET /stats/daily?start_date=2018-06-12&end_date=2018-06-30
```

The API returns HTTP 400 if the start date is later than the end date.

### Interactive API Documentation

FastAPI automatically generates Swagger documentation.

Once the backend is running, visit:

`http://127.0.0.1:8000/docs`



## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/gamepulse.git
cd gamepulse
```

### 2. Backend Setup

Create a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Database Configuration

Create a PostgreSQL database named `gamepulse_db`.

Create a `.env` file in the project root and configure the database connection and Google Cloud project settings.

Google Cloud Application Default Credentials are required to run the BigQuery ETL pipeline.

### 4. Run the ETL Pipeline

After configuring PostgreSQL and Google Cloud credentials, run:

```bash
python create_db_tables.py
python main.py
```

### 5. Start the Backend

```bash
python -m uvicorn src.api.main:app --reload
```

API documentation:

`http://127.0.0.1:8000/docs`

### 6. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Dashboard:

`http://localhost:5173`

### 7. Run Automated Tests

From the project root:

```bash
python -m pytest tests/test_api.py -v
```
