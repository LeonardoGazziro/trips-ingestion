"""File with function to sava CSV in raw layer."""
import pandas as pd

from src.config import settings, logger
from datetime import datetime
from src.file_functions import processed_file


def csv_to_postgres(conn, file_path, table_name):
    """
    Save CSV file to postgres, this function will create the table, using all fields like string and save the CSV file.
    :param conn: SQLAlchemy connection
    :param file_path: CSV file path
    :param table_name: table name.
    :return: None
    """
    try:
        logger.info('Starting insert CSV to Postgres')

        count = 0
        start_time = datetime.now()
        # Read the file with pandas chunks
        for chunk in pd.read_csv(file_path, chunksize=int(settings.READ_CSV_CHUNKSIZE)):
            count += 1
            logger.info(f'Reading chunk {count}, rows quantity {int(settings.READ_CSV_CHUNKSIZE) + count}')
            # Save to Postgre in chunks
            chunk.to_sql(table_name, conn, if_exists='append', chunksize=int(settings.INSERT_CHUNKSIZE))
        logger.info('Insertion time: {}'.format(datetime.now() - start_time))

        # Set file as processed
        processed_file(file_path)
    except Exception as err:
        logger.error(err)
        raise err
