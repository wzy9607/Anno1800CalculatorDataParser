# coding:utf-8
import re

import bs4

from .asset import Asset
from .product import ProductInStream


class PopulationGroup(Asset):
    """
    <PopulationGroup7>
      <PopulationLevels>
        <Item>
          <Level></Level> *
        </Item>
        ...
      </PopulationLevels>
    </PopulationGroup7>
    """
    population_levels = []  # Values.PopulationGroup7.PopulationLevels
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        assert (node.Template.string == "PopulationGroup7")
        population_group = super().parse(node, **kwargs)
        values = node.Values.PopulationGroup7
        population_group['population_levels'] = [int(item.Level.string) for item in values.PopulationLevels("Item")]
        return population_group


class PopulationLevel(Asset):
    """
    <PopulationLevel7>
      <PopulationInputs>
        <Item>
          <Product></Product> *
          <Amount></Amount>
          <SupplyWeight></SupplyWeight>
          <HappinessValue></HappinessValue>
          <MoneyValue></MoneyValue>
          <FullWeightPopulationCount></FullWeightPopulationCount>
          <NoWeightPopulationCount></NoWeightPopulationCount>
        </Item>
        ...
      </PopulationInputs>
      <PopulationOutputs>
        <Item>
          <Product></Product> *
          <Amount></Amount> only one
        </Item>
        ...
      </PopulationOutputs>
      <MoveInOut>
        <MoveInInterval></MoveInInterval>
        <MoveOutInterval></MoveOutInterval>
      </MoveInOut>
      <CategoryIcon></CategoryIcon>
      <PopulationParticipant></PopulationParticipant>
      <PopulationAtWorkParticipant></PopulationAtWorkParticipant>
      <MoodText>
        <Angry>
          <Text></Text>
        </Angry>
        <Unhappy>
          <Text></Text>
        </Unhappy>
        <Neutral>
          <Text></Text>
        </Neutral>
        <Happy>
          <Text></Text>
        </Happy>
        <Euphoric>
          <Text></Text>
        </Euphoric>
      </MoodText>
    </PopulationLevel7>
    """
    max_pop_per_house = None  # sum of influx of needs
    needs = []  # Values.PopulationLevel7.PopulationInputs
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        assert (node.Template.string == "PopulationLevel7")
        population_level = super().parse(node, **kwargs)
        population_level['icon'] = re.search('((icons/icon_)|(profiles/resident_))(?P<name>.*)',
                                             population_level['icon']).group('name')
        population_level['icon'] = "population/" + population_level['icon'].replace("resident_", "")
        values = node.Values.PopulationLevel7
        population_level['needs'] = [Need.parse(item) for item in values.PopulationInputs("Item")]
        population_level['max_pop_per_house'] = sum(x.get('influx', 0) for x in population_level.get('needs'))
        return population_level


class Need(ProductInStream):
    """
    <Item>
      <Product></Product> *
      <Amount></Amount>
      <SupplyWeight></SupplyWeight>
      <HappinessValue></HappinessValue>
      <MoneyValue></MoneyValue>
      <FullWeightPopulationCount></FullWeightPopulationCount>
      <NoWeightPopulationCount></NoWeightPopulationCount>
    </Item>
    """
    id = None  # Item.Product
    amount = None  # Item.Amount The amount of goods each house consumes every second.
    influx = None  # Item.SupplyWeight The amount of people moving into each house due to fulfilling  this need.
    happiness = None  # Item.HappinessValue The increase in happiness due to fulfilling this need.
    income = None  # Item.MoneyValue The increase each house in income due to fulfilling this need.
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        need = super().parse(node, **kwargs)
        if node.SupplyWeight:
            need['influx'] = int(node.SupplyWeight.string)
        if node.HappinessValue:
            need['happiness'] = int(node.HappinessValue.string)
        if node.MoneyValue:
            need['income'] = float(node.MoneyValue.string)
        return need
