# coding:utf-8
from abc import abstractmethod

import bs4


class Template:
    @classmethod
    @abstractmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        ...
