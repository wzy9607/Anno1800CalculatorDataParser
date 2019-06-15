# coding:utf-8

import bs4

from data_parser.template import ProductFilter


def parse_product_filters(tags: bs4.Tag, assets_map: dict) -> list:
    product_filters = []
    for tag in tags:
        if tag.Template.string == "ItemFilter":
            continue
        product_filters.append(ProductFilter.parse(tag, assets_map = assets_map))
    return product_filters
