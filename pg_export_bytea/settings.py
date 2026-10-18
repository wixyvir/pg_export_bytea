#!/usr/bin/python3
# coding: utf-8

import os

APP_NAME = "pg_export_bytea"

POSTGRES_DEFAULT_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DEFAULT_HOST = os.getenv("POSTGRES_HOST", "/var/run/postgresql/")
POSTGRES_DEFAULT_USER = os.getenv(
    "POSTGRES_USER", os.getenv("USER", "postgres"))
POSTGRES_DEFAULT_DB = os.getenv("POSTGRES_DB", "public")

DEFAULT_FILENAME_COLUMN = "filename"
DEFAULT_FILECONTENT_COLUMN = "binary"
