# coding:utf-8

import bs4

from data_parser.template import Product, Text


def parse_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(Product(tag).values)
    return products


def parse_workforces(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(Product(tag).values)
    return products


def parse_abstract_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(Product(tag).values)
    return products


def parse_normal_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(Product(tag).values)
    return products


def parse_product_categories(tags: bs4.Tag) -> list:
    product_categories = []
    for tag in tags:
        product_categories.append(Text(tag).values)
    return product_categories
