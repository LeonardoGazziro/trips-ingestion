"""Function to execute a script in database"""
import os

from src.config import logger


def execute(db_conn, db_cursor, script_name):
    """
    Load a script from file in folder SQL and execute.
    :param db_conn: pycopg2 database connection.
    :param db_cursor: psycopg2 database cursor.
    :param script_name: Script name
    :return: None
    """
    try:
        base_path = os.getcwd()
        with open(f'{base_path}/SQL/{script_name}') as file:
            script = file.read()

        logger.info('Executing script')
        db_cursor.execute(script)
        db_conn.commit()
        logger.info('Executed script')
    except FileNotFoundError as err:
        logger.error('Load file error: {}'.format(err))
    except Exception as err:
        logger.error('Execute script error: {}'.format(err))