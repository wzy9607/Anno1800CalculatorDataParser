# coding:utf-8

import bs4

from .asset import Asset


class ProductFilter(Asset):
    """
    <ProductFilter>
      <Categories>
        <Item>
          <CategoryAsset>guid</CategoryAsset>
          <Products>
            <Item>
              <Product>guid</Product>
            </Item>
            ...
          </Products>
        </Item>
        ...
      </Categories>
    </ProductFilter>
    """
    categories = []  # ProductFilter.Categories
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        assert (node.Template.string == "ProductFilter")
        product_filter = super().parse(node, **kwargs)
        values = node.Values.ProductFilter
        assets_map = kwargs['assets_map']
        product_filter['categories'] = []
        for item in values.Categories:
            if isinstance(item, bs4.Tag):
                category = ProductFilterCategory.parse(item)
                category.update(ProductFilterCategory.grab_name(assets_map, category['id']))
                product_filter['categories'].append(category)
        return product_filter


class ProductFilterCategory(Asset):
    """
    <Item>
      <CategoryAsset>guid</CategoryAsset>
      <Products>
        <Item>
          <Product>guid</Product>
        </Item>
        ...
      </Products>
    </Item>
    """
    products = []  # Item.Products
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product_filter_category = dict()
        product_filter_category['id'] = int(node.CategoryAsset.string)
        product_filter_category['products'] = [int(item.Product.string) for item in node.Products("Item")]
        return product_filter_category
