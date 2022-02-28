"""PostgreSQL class to create SQLAlchemy engine and psycopg2 connection and cursor"""
from src.config import settings
from sqlalchemy import create_engine
import psycopg2


class PostgreConnections:
    def __init__(self, host=None, database=None, user=None, password=None, port=None):
        """
        Class init
        :param host: Postgres host
        :param database: Postgres database name
        :param user: Postgres user
        :param password: Postgres password
        :param port: Postgres port
        """
        self._host = host if host else settings.PG_HOST
        self._db = database if database else settings.PG_DATABASE
        self._user = user if user else settings.PG_USER
        self._pass = password if password else settings.PG_PASSWORD
        self._port = port if port else settings.PG_PORT

        # create connection string
        self._conn_string = f'postgresql://{self._user}:{self._pass}@{self._host}:{self._port}/{self._db}'
        self._engine = None
        self._conn = None
        self._cur = None

    def __repr__(self):
        """
        Class representation
        :return: String with class name
        """
        return 'PostgreConnections()'

    def __str__(self):
        """
        Class to str (when you use print(ClassObject), this function will be called)
        :return: String with class name and db connected
        """
        return f'PostgreConnections(db={self._db})'

    def __create_sqlalchemy_engine(self, connect_args=None):
        """
        Create SQLAlchemy engine, this is an internal function called only for self class
        :param connect_args: SQLAlchemy connection arguments. Type: Dict.
        :return: None
        """
        if connect_args is None:
            connect_args = {}
        self._engine = create_engine(self._conn_string, connect_args=connect_args)

    def __create_psycopg_connection_and_cursor(self):
        """
        Create Psycopg2 connection and class, this is an internal function called only for self class
        :return: None
        """
        self._conn = psycopg2.connect(host=self._host, database=self._db, user=self._user, password=self._pass,
                                      port=self._port)
        self._cur = self._conn.cursor()

    def get_pg_engine(self, connect_args=None):
        """
        Get Postgres SQLAlchemy engine
        :param connect_args: SQLAlchemy connection arguments. Type: Dict.
        :return: SQLAlchemy engine
        """
        if connect_args is None:
            connect_args = {}
        if self._engine is None:
            self.__create_sqlalchemy_engine(connect_args)

        return self._engine

    def get_pg_connection_and_cursor(self):
        """
        Get Postgres psycopg2 connection and cursor
        :return: psycopg2 connection, psycopg2 cursor
        """
        if self._conn is None:
            self.__create_psycopg_connection_and_cursor()

        return self._conn, self._cur
