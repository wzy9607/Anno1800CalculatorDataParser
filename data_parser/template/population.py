# coding:utf-8
import re

import bs4

from .product import ProductInStream
from .template import Template


class PopulationGroup(Template):
    id = None  # Standard.GUID
    name = None  # Standard.Name
    icon = None  # Standard.IconFilename
    text = None  # Text.LocaText.English.Text
    population_levels = []  # PopulationLevels
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        population_group = dict()
        population_group['id'] = int(node.Standard.GUID.string)
        population_group['name'] = str(node.Standard.Name.string)
        population_group['text'] = str(node.Text.LocaText.English.Text.string)
        population_group['population_levels'] = [int(item.Level.string) for item in
                                                 node.PopulationGroup7.PopulationLevels("Item")]
        return population_group


class PopulationLevel(Template):
    id = None  # Standard.GUID
    name = None  # Standard.Name
    icon = None  # Standard.IconFilename
    text = None  # Text.LocaText.English.Text
    max_pop_per_house = None  # sum of influx of needs
    needs = []  # PopulationInputs
    outputs = []  # PopulationOutputs ?
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        population_level = dict()
        population_level['id'] = int(node.Standard.GUID.string)
        population_level['name'] = str(node.Standard.Name.string)
        icon_str = str(node.Standard.IconFilename.string)
        population_level['icon'] = re.search('((icons/icon_)|(profiles/resident_))(?P<name>.*)', icon_str).group('name')
        population_level['icon'] = "population/" + population_level['icon'].replace("resident_", "")
        population_level['text'] = str(node.Text.LocaText.English.Text.string)
        population_level['needs'] = kwargs['needs']
        population_level['outputs'] = kwargs['outputs']
        population_level['max_pop_per_house'] = sum(x.get('influx', 0) for x in population_level.get('needs'))
        return population_level


class Need(ProductInStream):
    id = None  # Product
    amount = None  # Amount ton per minute per pop
    influx = None  # SupplyWeight The amount of people moving into each house when fulfilled this need.
    happiness = None  # HappinessValue
    income = None  # MoneyValue
    
    # FullWeightPopulationCount ?
    # NoWeightPopulationCount ?
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        need = super(Need, cls).parse(node)
        if node.SupplyWeight:
            need['influx'] = int(node.SupplyWeight.string)
        if node.HappinessValue:
            need['happiness'] = int(node.HappinessValue.string)
        if node.MoneyValue:
            need['income'] = float(node.MoneyValue.string)
        return need
