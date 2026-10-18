#!/usr/bin/python3
# coding: utf-8

from cleo.application import Application as BaseApplication

import logging
import logging.config
import coloredlogs

from .cli.export import ExportCommand
from .service.postgres import Postgres

import pg_export_bytea.settings as settings


class Application(BaseApplication):
    def __init__(self):
        super(Application, self).__init__(settings.APP_NAME)

        # create logger
        logger = logging.getLogger()
        coloredlogs.install(
            logger=logger, fmt='%(asctime)s - %(levelname)s - %(message)s')

        postgres = Postgres()
        command = ExportCommand(postgres, logger)
        self.add(command)


def main():
    Application().run()


if __name__ == "__main__":
    main()
