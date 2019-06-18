# coding:utf-8
import abc
import re

import bs4

from .asset import Asset
from .utils import parse_session_list


class Building(Asset):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
    </Standard>
    <Text .../> *
    <Building .../> *
    <Cost .../> * building construction cost
    id                  Standard.GUID                       GUID of the building
    name                Standard.Name                       name of the building
    text                Text.LocaText.English.Text          in-game English name of the building
    session             Building.AssociatedRegion           a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    """
    
    @property
    @abc.abstractmethod
    def template_name(self):
        ...
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()
        # modify icon path and name to fit application
        self.values['icon'] = re.search('icons/icon_(?P<name>.*)', self.values['icon']).group('name')
        self.parse_node_text(self.values_node.Text)
        self.parse_node_building(self.values_node.Building)
        self.parse_node_cost(self.values_node.Cost)
    
    def parse_node_building(self, node: bs4.Tag):
        """
        <Building>
          <BuildingType>Enum("Factory"/"Residence"/"Logistic"/"Warehouse"/"Other")</BuildingType> ?
          <BuildingCategoryName>GUID</BuildingCategoryName> ?
          <Destructable>Binary</Destructable> ?
          <Movable>Binary(Default 1)</Movable> ?
          <TakeOverTransformation>"Destroy"</TakeOverTransformation> ?
          <PickingAsset>GUID</PickingAsset> ?
          <SnapRadius>NaturalInteger</SnapRadius> ?
          <TerrainType>Enum("Coast"/"Water")</TerrainType> ?
          <SkipUnlockMessage>Binary(Default 0)</SkipUnlockMessage> ?
          <HasBorderRectOutline>0</HasBorderRectOutline> ?
          <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> ?
          <InfluencedByNeighbors> ?
            <Item>
              <Building>GUID</Building>
            </Item>
            ...
          </InfluencedByNeighbors>
          <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> sessions where the building can be built
          <DeactivateHideWhenClippingIntoCamera>Binary(Default 0)</DeactivateHideWhenClippingIntoCamera> ?
          <BuildingBlockPool> ?
            <DontCare>
              <Pool>
                <Item>
                  <DirectionOffet>NaturalInteger</DirectionOffet>
                  <Variation>NaturalInteger</Variation> * unique
                </Item>
                ...
              </Pool>
            </DontCare>
            <Corner>
              <Pool>
                <Item>
                  <DirectionOffet>NaturalInteger</DirectionOffet>
                  <Variation>NaturalInteger</Variation> * unique
                </Item>
                ...
              </Pool>
            </Corner>
            <Mid>
              <Pool>
                <Item>
                  <DirectionOffet>NaturalInteger</DirectionOffet>
                  <Variation>NaturalInteger</Variation> * unique
                </Item>
                ...
              </Pool>
            </Mid>
          </BuildingBlockPool>
        </Building>
        session     Building.AssociatedRegion    the list of sessions where the building can be built
        :param node: the Building node
        """
        if node.AssociatedRegion:
            self.values['session'] = parse_session_list(node.AssociatedRegion.string)
    
    def parse_node_cost(self, node: bs4.Tag):
        """
        <Cost> construction cost
          <Costs> *
            <Item>
              <Ingredient>GUID</Ingredient> * the GUID of resource
              <Amount>NaturalInteger(Default 0)</Amount> the amount of resource needed
            </Item>
            ...
          </Costs>
        </Cost>
        costs       Cost.Costs          a list of resources required for building construction
            id      .Item.Ingredient    GUID of the resource
            amount  .Item.Amount        amount of resource needed
        :param node: the Cost node
        """
        self.values["costs"] = list()
        for cost in node.Costs("Item"):
            tmp = {'id': int(cost.Ingredient.string)}
            if cost.Amount:
                tmp['amount'] = int(cost.Amount.string)
            self.values["costs"].append(tmp)
