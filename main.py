"""Entry point for trips ingestion."""
from src.config import settings
from src.csv_to_db import csv_to_postgres
from src.execute_db_script import execute
from src.database.postgres import PostgreConnections


def trips_ingestion():
    """
    Start trips CSV ingestion
    :return: None
    """
    pg = PostgreConnections()

    csv_to_postgres(pg.get_pg_engine({'options': '-csearch_path={}'.format(settings.PG_SCHEMA)}), 'input_files/trips.csv', 'trips_log')

    pg_conn, pg_cursor = pg.get_pg_connection_and_cursor()
    execute(pg_conn, pg_cursor, 'create_trips_log.sql')


if __name__ == '__main__':
    trips_ingestion()