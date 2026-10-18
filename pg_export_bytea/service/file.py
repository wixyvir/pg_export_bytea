#!/usr/bin/python3
# coding: utf-8

from pg_export_bytea.entity.file import File as FileEntity


def _slugify(value, allow_unicode=False):
    """
    Normalizes string, removes non-alpha characters.
    """
    import unicodedata
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    return value


class File:
    output_path: str

    def __init__(self, output_path: str):
        self.output_path = output_path

    def export(self, file: FileEntity):
        """
        Write files from a File Entity
        :param file:
        """
        with open("{}/{}".format(self.output_path, _slugify(file.filename)), "wb") as file_handler:
            file_handler.write(bytes(file.content))
