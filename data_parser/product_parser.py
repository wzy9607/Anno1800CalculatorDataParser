# coding:utf-8

import bs4

from data_parser.template import Product, Text


def parse_products(tags: bs4.Tag) -> list:
    products = [Product(tag).get_values() for tag in tags]
    return products


def parse_workforces(tags: bs4.Tag) -> list:
    products = [Product(tag).values for tag in tags]
    return products


def parse_abstract_products(tags: bs4.Tag) -> list:
    products = [Product(tag).get_values() for tag in tags]
    return products


def parse_normal_products(tags: bs4.Tag) -> list:
    products = [Product(tag).get_values() for tag in tags]
    return products


def parse_product_categories(tags: bs4.Tag) -> list:
    product_categories = [Text(tag).get_values() for tag in tags]
    return product_categories
