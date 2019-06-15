# coding:utf-8
import re

import bs4

from .asset import Asset


class PopulationLevel(Asset):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
    </Standard>
    <Text .../> *
    <PopulationLevel7 .../>
    id                  Standard.GUID                       the GUID of the population level
    name                Standard.Name                       the name of the population level
    icon                Standard.IconFilename               the icon of the population level
    text                Text.LocaText.English.Text          the in-game English name of the population level
    needs               PopulationLevel7.PopulationInputs   a list of needs of the population level
        id              .Item.Product                       the GUID of the product
        amount          .Item.Amount                        the amount of goods each house consumes every second
        influx          .Item.SupplyWeight                  the amount of people moving into each house due to
                                                                fulfilling this need
        happiness       .Item.HappinessValue                the increase in happiness due to fulfilling this need
        income          .Item.MoneyValue                    the increase each house in income due to fulfilling
                                                                this need
    max_pop_per_house                                       the sum of influx of needs
    """
    template_name = "PopulationLevel7"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()
        # modify icon path and name to fit application
        icon_str = self.values['icon']
        icon_str = re.search('((icons/icon_)|(profiles/resident_))(?P<name>.*)', icon_str).group('name')
        icon_str = "population/" + icon_str.replace("resident_", "")
        self.values['icon'] = icon_str
        self.parse_node_text(self.values_node.Text)
        self.parse_node_population_level(self.values_node.PopulationLevel7)
    
    def parse_node_population_level(self, node: bs4.Tag):
        """
        <PopulationLevel7>
          <PopulationInputs>
            <Item .../>
            ...
          </PopulationInputs>
          <PopulationOutputs> ?
            <Item>
              <Product>GUID</Product> *
              <Amount>100</Amount> only one
            </Item>
            ...
          </PopulationOutputs>
          <MoveInOut> ?
            <MoveInInterval>UnsignedInteger</MoveInInterval> *
            <MoveOutInterval>UnsignedInteger</MoveOutInterval> *
          </MoveInOut>
          <CategoryIcon>Path</CategoryIcon> * ?
          <PopulationParticipant></PopulationParticipant> * ?
          <PopulationAtWorkParticipant></PopulationAtWorkParticipant> * ?
          <MoodText> ?
            <Angry>
              <Text>GUID</Text> *
            </Angry>
            <Unhappy>
              <Text>GUID</Text> *
            </Unhappy>
            <Neutral>
              <Text>GUID</Text> *
            </Neutral>
            <Happy>
              <Text>GUID</Text> *
            </Happy>
            <Euphoric>
              <Text>GUID</Text> *
            </Euphoric>
          </MoodText>
        </PopulationLevel7>
        needs               PopulationLevel7.PopulationInputs   a list of needs of the population level
            id              .Item.Product                       the GUID of the product
            amount          .Item.Amount                        the amount of goods each house consumes every second
            influx          .Item.SupplyWeight                  the amount of people moving into each house due to
                                                                    fulfilling this need
            happiness       .Item.HappinessValue                the increase in happiness due to fulfilling this need
            income          .Item.MoneyValue                    the increase each house in income due to fulfilling
                                                                    this need
        max_pop_per_house                                       the sum of influx of needs
        :param node: the PopulationLevel7 node
        """
        self.values['needs'] = [parse_node_population_inputs_item(item) for item in node.PopulationInputs("Item")]
        self.values['max_pop_per_house'] = sum(x.get('influx', 0) for x in self.values['needs'])


def parse_node_population_inputs_item(node: bs4.Tag) -> dict:
    """
    <Item>
      <Product>GUID</Product> *
      <Amount>Float</Amount> ?
      <SupplyWeight>UnsignedInteger</SupplyWeight>
      <HappinessValue>UnsignedInteger</HappinessValue>
      <MoneyValue>UnsignedInteger</MoneyValue>
      <FullWeightPopulationCount>UnsignedInteger</FullWeightPopulationCount> ?
      <NoWeightPopulationCount>UnsignedInteger</NoWeightPopulationCount> ?
    </Item>
    id          .Item.Product        the GUID of the product
    amount      .Item.Amount         the amount of goods each house consumes every second
    influx      .Item.SupplyWeight   the amount of people moving into each house due to fulfilling this need
    happiness   .Item.HappinessValue the increase in happiness due to fulfilling this need
    income      .Item.MoneyValue     the increase each house in income due to fulfilling this need
    """
    need = dict()
    need['id'] = int(node.Product.string)
    if node.Amount:
        need['amount'] = float(node.Amount.string)
    if node.SupplyWeight:
        need['influx'] = int(node.SupplyWeight.string)
    if node.HappinessValue:
        need['happiness'] = int(node.HappinessValue.string)
    if node.MoneyValue:
        need['income'] = int(node.MoneyValue.string)
    return need
