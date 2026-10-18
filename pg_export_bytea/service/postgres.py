#!/usr/bin/python3
# coding: utf-8
from typing import Optional, List
import psycopg
from psycopg.pq import ConnStatus
from psycopg.rows import dict_row
from typing_extensions import LiteralString

import pg_export_bytea.entity.file as file_entity
from pg_export_bytea import settings
from pg_export_bytea.exception import MissingColumns


class Postgres:
    _host: Optional[str]
    _port: Optional[int]
    _username: Optional[str]
    _password: Optional[str]
    _dbname: Optional[str]
    _dsn: Optional[str]
    _connection: Optional[psycopg.Connection]

    def _build_dsn(self, host: str, port: int, username: str, password: str, dbname: str) -> None:
        """
        Build an internal connection string for PostgreSQL
        :param host:
        :param port:
        :param username:
        :param password:
        :param dbname:
        """
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._dbname = dbname
        self._dsn = "host='{}' user='{}' dbname='{}' port={} ".format(
            self._host,
            self._username.replace("'", r"\'"),
            self._dbname.replace("'", r"\'"),
            self._port,
        ) + "password='{}'".format(self._password.replace("'", r"\'"))\
            if self._password is not None and self._password != "" else ""

    def connect(self, host: str, port: int, username: str, password: str, dbname: str) -> None:
        """
        Connect to the specified PostgreSQL database
        :param host:
        :param port:
        :param username:
        :param password:
        :param dbname:
        """
        self._build_dsn(host, port, username, password, dbname)
        self._connection = psycopg.connect(self._dsn,
                                           application_name=settings.APP_NAME)

    def connection_ok(self) -> bool:
        """
        Returns true if database connection is usable
        :return:
        """
        if self._connection is None:
            raise RuntimeError(
                'Connection to database must be established first')
        return self._connection.info.status == ConnStatus.OK

    def export_files(self, sql: LiteralString,
                     content_column: str = settings.DEFAULT_FILECONTENT_COLUMN,
                     filename_column: str = settings.DEFAULT_FILENAME_COLUMN):
        """
        yields Files from a sql query, extracting them from content_column and filename_column
        :param sql:
        :param content_column:
        :param filename_column:
        """
        if not self.connection_ok():
            raise RuntimeError('Connection to database is not available')
        with self._connection.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, binary=True)
            for record in cur:
                if filename_column not in record or content_column not in record:
                    raise MissingColumns("Missing columns {} and {} in SQL {}".format(
                        filename_column, content_column, sql))
                yield file_entity.File(filename=record[filename_column], content=record[content_column])
