# coding:utf-8

import bs4

from data_parser.template import AbstractProduct, NormalProduct, Product, ProductCategory, Workforce


def parse_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(Product.parse(tag))
    return products


def parse_workforces(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(Workforce.parse(tag))
    return products


def parse_abstract_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(AbstractProduct.parse(tag))
    return products


def parse_normal_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        products.append(NormalProduct.parse(tag))
    return products


def parse_product_categories(tags: bs4.Tag) -> list:
    product_categories = []
    for tag in tags:
        node = tag.Values
        product_categories.append(ProductCategory.parse(node))
    return product_categories
