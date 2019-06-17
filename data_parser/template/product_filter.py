# coding:utf-8

import bs4

from .asset import Asset
from .utils import grab_name


class ProductFilter(Asset):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
    </Standard>
    <ProductFilter .../> *
    id              Standard.GUID               GUID of the product filter
    name            Standard.Name               name of the product filter
    categories      ProductFilter.Categories    a list of product filter categories
        id          .Item.CategoryAsset         GUID of the category
        products    .Item.Products              a list of products in the category
        name                                    name of the category
        text                                    in-game English name of the category
    """
    
    template_name = "ProductFilter"
    
    def __init__(self, node: bs4.Tag, parse = True, **kwargs):
        super().__init__(node, parse = False)
        self.assets_map = kwargs['assets_map']
        # parse the node
        if parse:
            self.parse()
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()
        self.parse_node_product_filter(self.values_node.ProductFilter)
    
    def parse_node_product_filter(self, node: bs4.Tag):
        """
        <ProductFilter>
          <Categories> categories of product filter
            <Item>
              <CategoryAsset>GUID</CategoryAsset> * GUID of the category
              <Products>
                <Item>
                  <Product>GUID</Product> * GUID of a product in the category
                </Item>
                ...
              </Products>
            </Item>
            ...
          </Categories>
        </ProductFilter>
        categories      ProductFilter.Categories    a list of product filter categories
            id          .Item.CategoryAsset         GUID of the category
            products    .Item.Products              a list of products in the category
            name                                    name of the category
            text                                    in-game English name of the category
        :param node: the ProductFilter node
        """
        self.values['categories'] = []
        for item in node.Categories:
            if isinstance(item, bs4.Tag):
                category = dict()
                category['id'] = int(item.CategoryAsset.string)
                category.update(grab_name(category['id'], self.assets_map))
                category['products'] = [int(item.Product.string) for item in item.Products("Item")]
                self.values['categories'].append(category)
