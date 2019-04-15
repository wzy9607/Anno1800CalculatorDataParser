# coding:utf-8

import bs4

from data_parser.template import ProductFilter, ProductFilterCategory, ProductInStream


def parse_product_filters(tags: bs4.Tag) -> list:
    product_filters = []
    for tag in tags:
        if tag.Template.string == "ItemFilter":
            continue
        node = tag.Values
        categories = parse_categories(node.ProductFilter.Categories.contents)
        product_filters.append(ProductFilter.parse(node, categories = categories))
    return product_filters


def parse_categories(tags: bs4.Tag) -> list:
    categories = []
    for tag in tags:
        node = tag
        if isinstance(node, bs4.Tag):
            categories.append(ProductFilterCategory.parse(node))
    return categories
