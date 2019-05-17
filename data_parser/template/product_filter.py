# coding:utf-8

import bs4

from .asset import Asset


class ProductFilter(Asset):
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


class ProductFilterCategory(Asset):
    id = None  # CategoryAsset
    name = None  # ? Standard.Name
    text = None  # ? Text.LocaText.English.Text
    products = []  # Products
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product_filter_category = dict()
        product_filter_category['id'] = int(node.CategoryAsset.string)
        product_filter_category['products'] = [int(item.Product.string) for item in
                                               node.Products("Item")]
        return product_filter_category
    
    @classmethod
    def grab_name(cls, assets_map: dict, id: int):
        node = assets_map.get(id)
        node = node.Values
        name = str(node.Standard.Name.string)
        text = str(node.Text.LocaText.English.Text.string)
        return {'name': name, 'text': text}
