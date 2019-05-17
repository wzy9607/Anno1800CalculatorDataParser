# coding:utf-8
import re

import bs4

from .asset import Asset


class Product(Asset):
    id = None  # Standard.GUID
    name = None  # Standard.Name
    icon = None  # Standard.IconFilename
    text = None  # Text.LocaText.English.Text
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = dict()
        product['id'] = int(node.Standard.GUID.string)
        product['name'] = str(node.Standard.Name.string)
        icon_str = str(node.Standard.IconFilename.string)
        product['icon'] = re.search('icons/icon_(?P<name>.*)', icon_str).group('name')
        product['text'] = str(node.Text.LocaText.English.Text.string)
        return product


class ResourceProduct(Product):
    """Money and Influence"""
    
    # ?
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(ResourceProduct, cls).parse(node, **kwargs)
        return product


class Workforce(Product):
    # ?
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(Workforce, cls).parse(node, **kwargs)
        product['icon'] = "resources/workforce_" + product['icon'].replace("resource_", "")
        return product


class RealProduct(Product):
    """Asset that is spmewhat a product in game """
    category = None  # Product.ProductCategory
    
    # ?
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(RealProduct, cls).parse(node, **kwargs)
        product['category'] = int(node.Product.ProductCategory.string)
        return product


class AbstractProduct(RealProduct):
    """Market, Pub, etc"""
    
    # ?
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(AbstractProduct, cls).parse(node, **kwargs)
        return product


class NormalProduct(RealProduct):
    # ?
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(NormalProduct, cls).parse(node, **kwargs)
        product['icon'] = "goods/" + product['icon']
        return product


class ProductInStream:
    id = None  # Product
    amount = None  # Amount
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = dict()
        product['id'] = int(node.Product.string)
        if node.Amount:
            product['amount'] = float(node.Amount.string)
        return product


class ProductCategory(Asset):
    id = None  # Standard.GUID
    name = None  # Standard.Name
    text = None  # Text.LocaText.English.Text
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product_category = dict()
        product_category['id'] = int(node.Standard.GUID.string)
        product_category['name'] = str(node.Standard.Name.string)
        product_category['text'] = str(node.Text.LocaText.English.Text.string)
        return product_category
