# coding:utf-8
import enum
import re

import bs4

from .asset import Asset
from .utils import parse_session_list


class Type(enum.Enum):
    """
    Product types
    """
    RESOURCE_PRODUCT = enum.auto()
    WORKFORCE = enum.auto()
    ABSTRACT_PRODUCT = enum.auto()
    STRATEGIC_RESOURCE = enum.auto()
    NORMAL_PRODUCT = enum.auto()


class Product(Asset):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <ID>Text</ID>
      <InfoDescription>GUID</InfoDescription>
    </Standard>
    <Text .../> *
    <Locked .../> * TODO
    <Product> *
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
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> sessions where the product can be consumed
    </Product>
    <ExpeditionAttribute .../> * TODO
    """
    
    template_name = "Product"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()
        self.get_type()
        # modify icon path and name to fit application
        self.values['icon'] = re.search('icons/icon_(?P<name>.*)', self.values['icon']).group('name')
        if self.type == Type.RESOURCE_PRODUCT:
            # TODO
            pass
        elif self.type == Type.WORKFORCE:
            self.values['icon'] = "resources/workforce_" + self.values['icon'].replace("resource_", "")
        elif self.type == Type.ABSTRACT_PRODUCT:
            # TODO
            pass
        elif self.type == Type.STRATEGIC_RESOURCE:
            # TODO
            pass
        elif self.type == Type.NORMAL_PRODUCT:
            self.values['icon'] = "goods/" + self.values['icon']
        else:
            raise NotImplementedError
        self.parse_node_text(self.values_node.Text)
        self.parse_node_product(self.values_node.Product)
    
    def parse_node_product(self, node: bs4.Tag):
        """
        <Product> *
          <ProductColor>-11415604</ProductColor> ?
          <StorageLevel>Option("Building"/"Area")</StorageLevel> ?
          <ProductCategory>GUID</ProductCategory>
          <BasePrice>UnsignedInteger</BasePrice> ?
          <CivLevel>UnsignedInteger(1, 2, 3, 4, 5)</CivLevel> ?
          <CanBeNegative>1</CanBeNegative>
          <DeltaOnly>1</DeltaOnly> ?
          <IsWorkforce>Binary(Default 0)</IsWorkforce>
          <IsAbstract>Binary(Default 0)</IsAbstract>
          <PathLayer>Option("Railway")</PathLayer> ?
          <IsStrategicResource>Binary(Default 0)</IsStrategicResource>
          <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion>
        </Product>
        category    Product.ProductCategory     the category that the product belongs to
        session     Product.AssociatedRegion    the list of session where the product can be consumed
        :param node: the Product node
        """
        if self.type == Type.RESOURCE_PRODUCT:
            pass
        elif self.type == Type.WORKFORCE:
            pass
        elif self.type == Type.ABSTRACT_PRODUCT:
            self.values['category'] = int(node.ProductCategory.string)
            self.values['session'] = parse_session_list(node.AssociatedRegion.string)
        elif self.type == Type.STRATEGIC_RESOURCE:
            self.values['category'] = int(node.ProductCategory.string)
        elif self.type == Type.NORMAL_PRODUCT:
            self.values['category'] = int(node.ProductCategory.string)
            self.values['session'] = parse_session_list(node.AssociatedRegion.string)
        else:
            raise NotImplementedError
    
    def get_type(self):
        """
        Get type of the product, see Type for available types
        """
        if self.values_node.Product.CanBeNegative and self.values_node.Product.CanBeNegative.string == "1":
            self.type = Type.RESOURCE_PRODUCT
        elif self.values_node.Product.IsWorkforce and self.values_node.Product.IsWorkforce.string == "1":
            self.type = Type.WORKFORCE
        elif self.values_node.Product.IsAbstract and self.values_node.Product.IsAbstract.string == "1":
            self.type = Type.ABSTRACT_PRODUCT
        elif self.values_node.Product.IsStrategicResource and self.values_node.Product.IsStrategicResource.string == \
                "1":
            self.type = Type.STRATEGIC_RESOURCE
        else:
            self.type = Type.NORMAL_PRODUCT
    
    # @property
    # def can_be_negative(self):
    #     if self.values_node.Product.CanBeNegative and self.values_node.Product.CanBeNegative.string == "1":
    #         return True
    #     else:
    #         return False
    #
    # @property
    # def is_workforce(self):
    #     if self.values_node.Product.IsWorkforce and self.values_node.Product.IsWorkforce.string == "1":
    #         return True
    #     else:
    #         return False
    #
    # @property
    # def is_abstract_product(self):
    #     if self.values_node.Product.IsAbstract and self.values_node.Product.IsAbstract.string == "1":
    #         return True
    #     else:
    #         return False
    #
    # @property
    # def is_strategic_resource(self):
    #     if self.values_node.Product.IsStrategicResource and self.values_node.Product.IsStrategicResource.string ==
    #     "1":
    #         return True
    #     else:
    #         return False


class ResourceProduct(Product):
    """
    Money and Influence
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <ID>Text</ID> *
    </Standard>
    <Text .../> *
    <Locked>
      <DefaultLockedState>0</DefaultLockedState> *
    </Locked>
    <Product>
      <CanBeNegative>1</CanBeNegative> * ?
    </Product>
    <ExpeditionAttribute /> *
    """


class Workforce(Product):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
    </Standard>
    <Text .../> *
    <Locked> *
      <DefaultLockedState>0</DefaultLockedState> *
    </Locked>
    <Product>
      <StorageLevel>"Area"</StorageLevel> * ?
      <DeltaOnly>1</DeltaOnly> * ?
      <IsWorkforce>1</IsWorkforce> *
    </Product>
    <ExpeditionAttribute /> *
    """


class AbstractProduct(Product):
    """
    Market, Pub, etc
    TODO 120022
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <ID>Text</ID>
    </Standard>
    <Text .../> *
    <Locked /> *
    <Product>
      <ProductColor>-11415604</ProductColor> * ?
      <StorageLevel>"Building"</StorageLevel> * ?
      <ProductCategory>GUID</ProductCategory> *
      <IsAbstract>1</IsAbstract> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Product>
    <ExpeditionAttribute /> *
    """


class NormalProduct(Product):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <ID>Text</ID>
      <InfoDescription>GUID</InfoDescription> *
    </Standard>
    <Text .../> *
    <Locked /> *
    <Product>
      <StorageLevel>"Building"</StorageLevel> *
      <ProductCategory>GUID</ProductCategory> *
      <BasePrice>UnsignedInteger</BasePrice> *
      <CivLevel>UnsignedInteger(1, 2, 3, 4, 5)</CivLevel> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Product>
    <ExpeditionAttribute .../> *
    """


class StrategicResources(Product):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <ID>Text</ID>
      <InfoDescription>GUID</InfoDescription> *
    </Standard>
    <Text .../> *
    <Locked /> *
    <Product>
      <StorageLevel>"Building"</StorageLevel> *
      <ProductCategory>GUID</ProductCategory> *
      <BasePrice>UnsignedInteger</BasePrice> *
      <CivLevel>UnsignedInteger(1, 2, 3, 4, 5)</CivLevel>
      <PathLayer>"Railway"</PathLayer> *
      <IsStrategicResource>1</IsStrategicResource> *
    </Product>
    <ExpeditionAttribute .../> *
    """
