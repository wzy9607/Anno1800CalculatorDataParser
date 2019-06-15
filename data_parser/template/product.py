# coding:utf-8
import re

import bs4

from .utils import parse_session_list
from .asset import Asset


class Product(Asset):
    """
    <Locked .../>
    <Product>
      <ProductColor>-11415604</ProductColor> ? only used for Abstract Products
      <StorageLevel>Option("Building"/"Area")</StorageLevel> ?
      <ProductCategory>GUID</ProductCategory>
      <BasePrice>UnsignedInteger</BasePrice>
      <CivLevel>UnsignedInteger(1, 2, 3, 4, 5)</CivLevel> population level start from witch the product is shown in
                                                              depots
      <CanBeNegative>1</CanBeNegative> ?
      <DeltaOnly>1</DeltaOnly> ?
      <IsWorkforce>Binary(Default 0)</IsWorkforce> 1 for Workforce
      <IsAbstract>Binary(Default 0)</IsAbstract> 1 for Abstract Products
      <PathLayer>Option("Railway")</PathLayer> ? only used for Strategic Resources
      <IsStrategicResource>Binary(Default 0)</IsStrategicResource> 1 for Strategic Resources
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion>
    </Product>
    <ExpeditionAttribute .../>
    """
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        assert (node.Template.string == "Product")
        product = super().parse(node, **kwargs)
        values = node.Values.Product
        # modify icon path and name to fit application
        product['icon'] = re.search('icons/icon_(?P<name>.*)', product['icon']).group('name')
        if values.CanBeNegative:
            pass
        elif values.IsWorkforce:
            # modify icon path and name to fit application
            product['icon'] = "resources/workforce_" + product['icon'].replace("resource_", "")
        elif values.IsAbstract:
            # TODO modify icon path and name to fit application
            product['category'] = int(values.ProductCategory.string)
            product['session'] = parse_session_list(values.AssociatedRegion.string)
        elif values.IsStrategicResource:
            product['category'] = int(values.ProductCategory.string)
        else:  # normal product
            # modify icon path and name to fit application
            product['icon'] = "goods/" + product['icon']
            product['category'] = int(values.ProductCategory.string)
            product['session'] = parse_session_list(values.AssociatedRegion.string)
        return product


class ResourceProduct(Product):
    """
    Money and Influence
    <Locked>
      <DefaultLockedState>0</DefaultLockedState> * ?
    </Locked>
    <Product>
      <CanBeNegative>1</CanBeNegative> * ?
    </Product>
    <ExpeditionAttribute />
    """
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(ResourceProduct, cls).parse(node, **kwargs)
        return product


class Workforce(Product):
    """
    <Locked>
      <DefaultLockedState>0</DefaultLockedState> * ?
    </Locked>
    <Product>
      <StorageLevel>"Area"</StorageLevel> * ?
      <DeltaOnly>1</DeltaOnly> * ?
      <IsWorkforce>1</IsWorkforce> * is a Workforce
    </Product>
    <ExpeditionAttribute />
    """
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(Workforce, cls).parse(node, **kwargs)
        values = node.Values.Product
        assert (values.IsWorkforce.string == "1")
        return product


class AbstractProduct(Product):
    """
    Market, Pub, etc
    TODO 120022
    <Locked />
    <Product>
      <ProductColor>-11415604</ProductColor> * ?
      <StorageLevel>"Building"</StorageLevel> * ?
      <ProductCategory>GUID</ProductCategory> *
      <IsAbstract>1</IsAbstract> * is a Abstract Product
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Product>
    <ExpeditionAttribute />
    """
    category = None  # Product.ProductCategory product category
    session = None  # Product.AssociatedRegion in witch sessions this product can be consumed
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(AbstractProduct, cls).parse(node, **kwargs)
        values = node.Values.Product
        assert (values.IsAbstract.string == "1")
        return product


class NormalProduct(Product):
    """
    <Locked />
    <Product>
      <StorageLevel>"Building"</StorageLevel> * ?
      <ProductCategory>GUID</ProductCategory> *
      <BasePrice>UnsignedInteger</BasePrice> *
      <CivLevel>UnsignedInteger(1, 2, 3, 4, 5)</CivLevel> * population level start from witch the product is shown in
                                                              depots
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion>
    </Product>
    <ExpeditionAttribute .../>
    """
    category = None  # Product.ProductCategory product category
    session = None  # Product.AssociatedRegion in witch sessions this product can be consumed
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(NormalProduct, cls).parse(node, **kwargs)
        return product


# TODO strategic resources


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
