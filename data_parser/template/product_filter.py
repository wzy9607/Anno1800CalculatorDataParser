# coding:utf-8

import bs4

from .template import Template


class ProductFilter(Template):
    id = None  # Standard.GUID
    name = None  # Standard.Name
    categories = []  # ProductFilter.Categories
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product_filter = dict()
        product_filter['id'] = int(node.Standard.GUID.string)
        product_filter['name'] = str(node.Standard.Name.string)
        product_filter['categories'] = kwargs['categories']
        return product_filter


class ProductFilterCategory(Template):
    id = None  # CategoryAsset
    name = None  # ?
    products = []  # Products
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product_filter_category = dict()
        product_filter_category['id'] = int(node.CategoryAsset.string)
        product_filter_category['products'] = [int(item.Product.string) for item in
                                               node.Products("Item")]
        return product_filter_category
