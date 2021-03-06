# coding:utf-8
import json

import bs4

from data_parser import population_parser, product_filter_parser, product_parser, production_building_parser
from data_parser.config import DATA_VERSION, JSON_INDENT, data_path, output_path


def load_assets():
    """
    load assets.xml
    :return: GUID to asset map
    """
    with open(data_path / "assets.xml", encoding = "utf-8") as file:
        soup = bs4.BeautifulSoup(file, "lxml-xml")
    assets_map = dict()
    templates = set()
    for assets in soup.find_all("Assets"):
        for asset in assets.children:
            if isinstance(asset, bs4.NavigableString):
                continue
            if asset.name == "Globe":
                continue
            tag = asset.Values
            guid = int(tag.Standard.GUID.string)
            assets_map[guid] = asset
    for asset in assets_map.values():
        if not asset.Template:
            pass  # TODO solve inheritance
    for asset in assets_map.values():
        if asset.Template:
            template = asset.Template.string
            templates.add(template)
    templates = {"Version": DATA_VERSION, "Templates": sorted(templates)}
    with (output_path / "templates.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(templates, output_file, ensure_ascii = False, indent = JSON_INDENT)
    return assets_map


def main():
    assets_map = load_assets()
    with open(data_path / "assets.xml", encoding = "utf-8") as file:
        soup = bs4.BeautifulSoup(file, "lxml-xml")
    
    farm_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[1]("Asset")
    farms = production_building_parser.parse_farms(farm_tags)
    production_buildings = farms
    factory1_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[3]("Asset")
    factories1 = production_building_parser.parse_factories(factory1_tags)
    production_buildings.extend(factories1)
    factory2_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[5]("Asset")
    factories2 = production_building_parser.parse_factories(factory2_tags)
    production_buildings.extend(factories2)
    factory3_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[7]("Asset")
    factories3 = production_building_parser.parse_factories(factory3_tags)
    production_buildings.extend(factories3)
    factory4_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[9]("Asset")
    factories4 = production_building_parser.parse_factories(factory4_tags)
    production_buildings.extend(factories4)
    factory5_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[11]("Asset")
    factories5 = production_building_parser.parse_factories(factory5_tags)
    production_buildings.extend(factories5)
    factory6_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[13]("Asset")
    factories6 = production_building_parser.parse_factories(factory6_tags)
    production_buildings.extend(factories6)
    factory7_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[1].contents[1] \
            .contents[3].contents[1].contents[15]("Asset")
    factories7 = production_building_parser.parse_factories(factory7_tags)
    production_buildings.extend(factories7)
    factory10_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[3].Groups.contents[
            1]("Asset")
    factories10 = production_building_parser.parse_factories(factory10_tags)
    production_buildings.extend(factories10)
    factory10_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[3].Groups.contents[
            3]("Asset")
    factories10 = production_building_parser.parse_factories(factory10_tags)
    production_buildings.extend(factories10)
    factory10_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[3].Groups.contents[
            5]("Asset")
    factories10 = production_building_parser.parse_factories(factory10_tags)
    production_buildings.extend(factories10)
    factory8_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[3].Groups.contents[
            7]("Asset")
    factories8 = production_building_parser.parse_factories(factory8_tags)
    production_buildings.extend(factories8)
    factory9_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[3].Groups.contents[
            13]("Asset")
    factories9 = production_building_parser.parse_factories(factory9_tags)
    production_buildings.extend(factories9)
    factory10_tags = \
        soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[3].Groups.contents[
            15]("Asset")
    factories10 = production_building_parser.parse_factories(factory10_tags)
    production_buildings.extend(factories10)
    production_buildings = {"Version": DATA_VERSION, "ProductionBuildings": production_buildings}
    with (output_path / "production_buildings.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(production_buildings, output_file, ensure_ascii = False, indent = JSON_INDENT)
    
    # resource_product_tags = \
    #     soup.AssetList.contents[1].contents[5].contents[1].contents[1].contents[1].contents[1]("Asset")
    # resource_products = product_parser.parse_resource_products(resource_product_tags)
    # with (output_path / "resource_products.json").open(mode = "w", encoding = "utf-8") as output_file:
    #     json.dump(resource_products, output_file, ensure_ascii = False, indent = JSON_INDENT)
    
    workforce_tags = \
        soup.AssetList.Groups.contents[7].Groups.contents[1].Groups.contents[3].Groups.contents[1].Groups("Asset")
    workforces = product_parser.parse_workforces(workforce_tags)
    workforces = {"Version": DATA_VERSION, "Workforces": workforces}
    with (output_path / "workforces.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(workforces, output_file, ensure_ascii = False, indent = JSON_INDENT)
    
    # abstract_need_product_tags = \
    #     soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[1].Groups("Asset")
    
    product_tags = \
        soup.AssetList.Groups.contents[7].Groups.contents[1].Groups.contents[3].Groups.contents[5].Groups("Asset")
    products = product_parser.parse_normal_products(product_tags)
    # coal and oil
    product2_tags = \
        soup.AssetList.Groups.contents[7].Groups.contents[1].Groups.contents[3].Groups.contents[7]("Asset")
    products2 = product_parser.parse_normal_products(product2_tags)
    products.extend(products2)
    products = {"version": DATA_VERSION, "Products": products}
    with (output_path / "products.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(products, output_file, ensure_ascii = False, indent = JSON_INDENT)
    
    product_category_tags = \
        soup.AssetList.Groups.contents[3].Groups.contents[3].Groups.contents[23].Groups.contents[1].Assets("Asset")
    product_categories = product_parser.parse_product_categories(product_category_tags)
    for category in product_categories:
        category['products'] = list()
    for product in products['Products']:
        category_id = product['category']
        for category in product_categories:
            if category['id'] == category_id:
                category['products'].append(product['id'])
    product_categories = {"Version": DATA_VERSION, "ProductCategories": product_categories}
    with (output_path / "product_categories.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(product_categories, output_file, ensure_ascii = False, indent = JSON_INDENT)
    
    population_group_tags = soup.AssetList.Groups.contents[9].contents[1].contents[1]("Asset")
    population_groups = population_parser.parse_population_groups(population_group_tags)
    population_groups = {"Version": DATA_VERSION, "PopulationGroups": population_groups}
    with (output_path / "population_groups.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(population_groups, output_file, ensure_ascii = False, indent = JSON_INDENT)
    
    population_level_tags = soup.AssetList.Groups.contents[9].contents[1].contents[3]("Asset")
    population_levels = population_parser.parse_population_levels(population_level_tags)
    population_levels = {"Version": DATA_VERSION, "PopulationLevels": population_levels}
    with (output_path / "population_levels.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(population_levels, output_file, ensure_ascii = False, indent = JSON_INDENT)
    
    product_filter_tags = \
        soup.AssetList.Groups.contents[39].Groups.contents[7].Groups.contents[3].Groups.contents[1].Assets("Asset")
    product_filters = product_filter_parser.parse_product_filters(product_filter_tags, assets_map)
    product_filters = {"Version": DATA_VERSION, "ProductFilters": product_filters}
    with (output_path / "product_filters.json").open(mode = "w", encoding = "utf-8") as output_file:
        json.dump(product_filters, output_file, ensure_ascii = False, indent = JSON_INDENT)


if __name__ == "__main__":
    main()
