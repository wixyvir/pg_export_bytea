#!/usr/bin/python3
# coding: utf-8

from dataclasses import dataclass

from typing_extensions import Buffer


@dataclass
class File:
    filename: str
    content: Buffer
