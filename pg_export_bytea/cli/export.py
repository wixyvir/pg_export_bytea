#!/usr/bin/python3
# coding: utf-8
import os
from logging import Logger
import getpass

from cleo.commands.command import Command
from cleo.helpers import argument, option
from cleo.io.outputs.output import Verbosity

from pg_export_bytea import settings
from ..exception import MissingColumns
from ..service.postgres import Postgres
from ..service.file import File as FileService


class ExportCommand(Command):

    name = "export"
    description = "A CLI helping tool for exporting bytea fields of a PostgreSQL relation into files"

    options = {
        option("host", None, "database server host or socket directory (default: \"local socket\")", False, False,
               default=settings.POSTGRES_DEFAULT_HOST),
        option("port", "p", "database server port", False,
               False, default=settings.POSTGRES_DEFAULT_PORT),
        option("dbname", "d", "database name", False, False,
               default=settings.POSTGRES_DEFAULT_DB),
        option("username", "u", "database user name", False, False,
               default=settings.POSTGRES_DEFAULT_USER),
        option("prompt", "W", "prompt for password. Or use the POSTGRES_PASSWORD environment variables",
               True, False),
        option("output", "o", "output directory path", False, False,
               default=os.getcwd())
    }

    logger: Logger
    postgres: Postgres

    arguments = {
        argument("sql", "SQL queries returning '{}' and '{}' columns".
                 format(settings.DEFAULT_FILENAME_COLUMN, settings.DEFAULT_FILECONTENT_COLUMN), multiple=True)
    }

    def __init__(self, postgres: Postgres, logger: Logger):
        super().__init__()
        self.logger = logger
        self.postgres = postgres

    def handle(self) -> int:
        failed_counter = 0
        password = os.getenv("POSTGRES_PASSWORD", "")
        if self.option("prompt"):
            password = getpass.getpass()
        self.postgres.connect(self.option("host"),
                              int(self.option("port")),
                              self.option("username"),
                              password,
                              self.option("dbname"))
        writer = FileService(self.option("output"))
        for sql in self.argument('sql'):
            try:
                self.line("Handling {}".format(sql),
                          verbosity=Verbosity.VERBOSE)
                for file in self.postgres.export_files(sql):
                    writer.export(file)
            except MissingColumns as e:
                self.line(str(e), style='error')
                failed_counter += 1
                continue
        return failed_counter
