from google.cloud import bigquery


def get_bigquery_client():
    return bigquery.Client(project="projem-468906")