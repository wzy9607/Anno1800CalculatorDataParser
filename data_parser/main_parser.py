# coding:utf-8
import json
import pathlib

from bs4 import BeautifulSoup

from data_parser import population_parser, product_parser, production_building_parser

JSON_INDENT = 2


def main():
    output_path = pathlib.Path("../json")
    with open("../data/assets.xml", mode = "r", encoding = "utf-8") as file:
        soup = BeautifulSoup(file, "lxml-xml")
        
        farm_tags = \
            soup.AssetList.contents[1].contents[3].contents[1].contents[1].contents[1].contents[1].contents[1] \
                .contents[3].contents[1].contents[1]("Asset")
        farms = production_building_parser.parse_farms(farm_tags)
        factory_tags = \
            soup.AssetList.contents[1].contents[3].contents[1].contents[1].contents[1].contents[1].contents[1] \
                .contents[3].contents[1].contents[3]("Asset")
        factories = production_building_parser.parse_factories(factory_tags)
        production_buildings = farms + factories
        with (output_path / "production_buildings.json").open(mode = "w", encoding = "utf-8") as output_file:
            json.dump(production_buildings, output_file, ensure_ascii = False, indent = JSON_INDENT)
        
        # resource_product_tags = \
        #     soup.AssetList.contents[1].contents[5].contents[1].contents[1].contents[1].contents[1]("Asset")
        # resource_products = product_parser.parse_resource_products(resource_product_tags)
        # with (output_path / "resource_products.json").open(mode = "w", encoding = "utf-8") as output_file:
        #     json.dump(resource_products, output_file, ensure_ascii = False, indent = JSON_INDENT)
        
        workforce_tags = soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[
            1].Groups("Asset")
        workforces = product_parser.parse_workforces(workforce_tags)
        with (output_path / "workforces.json").open(mode = "w", encoding = "utf-8") as output_file:
            json.dump(workforces, output_file, ensure_ascii = False, indent = JSON_INDENT)
        
        # abstract_need_product_tags = \
        #     soup.AssetList.contents[1].contents[5].contents[1].contents[1].contents[1].contents[3].contents[1] \
        #         .contents[3].contents[1]("Asset")
        
        product_tags = \
            soup.AssetList.Groups.contents[5].Groups.contents[1].Groups.contents[3].Groups.contents[5].Groups.contents[
                1].Groups("Asset")
        products = product_parser.parse_normal_products(product_tags)
        with (output_path / "products.json").open(mode = "w", encoding = "utf-8") as output_file:
            json.dump(products, output_file, ensure_ascii = False, indent = JSON_INDENT)
        
        product_category_tags = \
            soup.AssetList.Groups.contents[1].Groups.contents[3].Groups.contents[23].Groups.contents[1].Assets("Asset")
        product_categories = product_parser.parse_product_categories(product_category_tags)
        for category in product_categories:
            category['products'] = list()
        for product in products:
            category_id = product['category']
            for category in product_categories:
                if category['id'] == category_id:
                    category['products'].append(product['id'])
        with (output_path / "product_categories.json").open(mode = "w", encoding = "utf-8") as output_file:
            json.dump(product_categories, output_file, ensure_ascii = False, indent = JSON_INDENT)
        
        population_group_tags = soup.AssetList.contents[1].contents[7].contents[1].contents[1]("Asset")
        population_groups = population_parser.parse_population_groups(population_group_tags)
        with (output_path / "population_groups.json").open(mode = "w", encoding = "utf-8") as output_file:
            json.dump(population_groups, output_file, ensure_ascii = False, indent = JSON_INDENT)
        
        population_level_tags = soup.AssetList.contents[1].contents[7].contents[1].contents[3]("Asset")
        population_levels = population_parser.parse_population_levels(population_level_tags)
        with (output_path / "population_levels.json").open(mode = "w", encoding = "utf-8") as output_file:
            json.dump(population_levels, output_file, ensure_ascii = False, indent = JSON_INDENT)
        
        # product_filter_tags = \
        #     soup.contents[0].contents[1].contents[35].contents[1].contents[7].contents[1].contents[3].contents[1] \
        #         .contents[1].Assets("Asset")
        # product_filters = product_filter_parser.parse_product_filters(product_filter_tags)
        # with (output_path / "product_filters.json").open(mode = "w", encoding = "utf-8") as output_file:
        #     json.dump(product_filters, output_file, ensure_ascii = False, indent = JSON_INDENT)


if __name__ == "__main__":
    main()
