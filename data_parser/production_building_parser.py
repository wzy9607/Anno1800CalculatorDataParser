# coding:utf-8

import bs4

from data_parser.template import Building, BuildingCost, BuildingMaintenances, ProductInProduction


def parse_production_building(tags: bs4.Tag) -> list:
    buildings = []
    for tag in tags:
        node = tag.Values
        costs = parse_costs(node.Cost.Costs("Item"))
        inputs = []
        if node.FactoryBase.FactoryInputs:
            inputs = parse_products_in_production(node.FactoryBase.FactoryInputs("Item"))
        outputs = parse_products_in_production(node.FactoryBase.FactoryOutputs("Item"))
        maintenances = parse_maintenances(node.Maintenance.Maintenances("Item"))
        buildings.append(
                Building.parse(node, costs = costs, inputs = inputs, outputs = outputs, maintenances = maintenances))
    return buildings


def parse_farms(tags: bs4.Tag) -> list:
    farms = []
    for tag in tags:
        node = tag.Values
        costs = parse_costs(node.Cost.Costs("Item"))
        inputs = []
        if node.FactoryBase.FactoryInputs:
            inputs = parse_products_in_production(node.FactoryBase.FactoryInputs("Item"))
        outputs = parse_products_in_production(node.FactoryBase.FactoryOutputs("Item"))
        maintenances = parse_maintenances(node.Maintenance.Maintenances("Item"))
        farms.append(
                Building.parse(node, costs = costs, inputs = inputs, outputs = outputs, maintenances = maintenances))
    return farms


def parse_factories(tags: bs4.Tag) -> list:
    factories = []
    for tag in tags:
        node = tag.Values
        costs = parse_costs(node.Cost.Costs("Item"))
        inputs = []
        if node.FactoryBase.FactoryInputs:
            inputs = parse_products_in_production(node.FactoryBase.FactoryInputs("Item"))
        outputs = parse_products_in_production(node.FactoryBase.FactoryOutputs("Item"))
        maintenances = parse_maintenances(node.Maintenance.Maintenances("Item"))
        factories.append(
                Building.parse(node, costs = costs, inputs = inputs, outputs = outputs, maintenances = maintenances))
    return factories


def parse_costs(tags: bs4.Tag) -> list:
    costs = []
    for tag in tags:
        node = tag
        costs.append(BuildingCost.parse(node))
    return costs


def parse_products_in_production(tags: bs4.Tag) -> list:
    products_in_production = []
    for tag in tags:
        node = tag
        products_in_production.append(ProductInProduction.parse(node))
    return products_in_production


def parse_maintenances(tags: bs4.Tag) -> list:
    maintenances = []
    for tag in tags:
        node = tag
        maintenances.append(BuildingMaintenances.parse(node))
    return maintenances
