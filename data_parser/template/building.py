# coding:utf-8
import re

import bs4

from .product import ProductInStream
from .template import Template


class Building(Template):
    id = None  # Standard.GUID
    name = None  # Standard.Name
    icon = None  # Standard.IconFilename
    text = None  # Text.LocaText.English.Text
    production_time = 0.5  # FactoryBase.CycleTime / 60.0
    costs = []  # Cost.Costs
    inputs = []  # FactoryBase.FactoryInputs
    outputs = []  # FactoryBase.FactoryOutputs
    maintenances = []  # Maintenance.Maintenances
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        building = dict()
        building['id'] = int(node.Standard.GUID.string)
        building['name'] = str(node.Standard.Name.string)
        icon_str = str(node.Standard.IconFilename.string)
        building['icon'] = re.search('icons/icon_(?P<name>.*)', icon_str).group('name')
        building['icon'] = "goods/" + building['icon']
        building['text'] = str(node.Text.LocaText.English.Text.string)
        if node.FactoryBase.CycleTime:
            building['production_time'] = int(node.FactoryBase.CycleTime.string) / 60.0
        else:
            building['production_time'] = 0.5
        building['costs'] = kwargs['costs']
        if node.FactoryBase.FactoryInputs:
            building['inputs'] = kwargs['inputs']
            for input1 in building['inputs']:
                input1['amount_per_minute'] = input1['amount'] / building['production_time']
        building['outputs'] = kwargs['outputs']
        for output in building['outputs']:
            output['amount_per_minute'] = output['amount'] / building['production_time']
        building['maintenances'] = kwargs['maintenances']
        return building


class Farm(Building):
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        farm = super(Farm, cls).parse(node, **kwargs)
        return farm


class Factory(Building):
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        factory = super(Factory, cls).parse(node, **kwargs)
        return factory


class BuildingCost(ProductInStream):
    id = None  # Ingredient
    amount = None  # Amount
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        building_cost = dict()
        building_cost['id'] = int(node.Ingredient.string)
        if node.Amount:
            building_cost['amount'] = float(node.Amount.string)
        return building_cost


class ProductInProduction(ProductInStream):
    id = None  # Product
    amount = None  # Amount ton per cycle per building
    amount_per_minute = None  # calculate elsewhere ton per minute per building
    storage_amount = None  # StorageAmount the amount of product that building can store
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = super(ProductInProduction, cls).parse(node, **kwargs)
        product['storage_amount'] = float(node.StorageAmount.string)
        return product


class BuildingMaintenances(ProductInStream):
    id = None  # Product
    amount = None  # Amount
    inactive_amount = None  # InactiveAmount when building is inactive
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        maintenance = super(BuildingMaintenances, cls).parse(node, **kwargs)
        if node.InactiveAmount:
            maintenance['inactive_amount'] = float(node.InactiveAmount.string)
        return maintenance
