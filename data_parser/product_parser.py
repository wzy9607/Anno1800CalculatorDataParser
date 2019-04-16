# coding:utf-8

import bs4

from data_parser.template import NormalProduct, Product, ProductCategory, ResourceProduct, Workforce


def parse_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        node = tag.Values
        products.append(Product.parse(node))
    return products


def parse_resource_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        node = tag.Values
        products.append(ResourceProduct.parse(node))
    return products


def parse_workforces(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        node = tag.Values
        products.append(Workforce.parse(node))
    return products


def parse_normal_products(tags: bs4.Tag) -> list:
    products = []
    for tag in tags:
        node = tag.Values
        products.append(NormalProduct.parse(node))
    return products


def parse_product_categories(tags: bs4.Tag) -> list:
    product_categories = []
    for tag in tags:
        node = tag.Values
        product_categories.append(ProductCategory.parse(node))
    return product_categories
