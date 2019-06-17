# coding:utf-8
import abc
import re

import bs4

from .asset import Asset
from .utils import parse_session_list


class Factory(Asset):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
    </Standard>
    <Text .../> *
    <Building> *
      <BuildingType>Enum("Factory"/"Residence"/"Logistic"/"Warehouse"/"Other")</BuildingType> ?
      <BuildingCategoryName>GUID</BuildingCategoryName> ?
      <Destructable>Binary</Destructable> ?
      <Movable>Binary(Default 1)</Movable> ?
      <TakeOverTransformation>"Destroy"</TakeOverTransformation> ?
      <PickingAsset>GUID</PickingAsset> the building which this building is upgraded from
      <SnapRadius>NaturalInteger</SnapRadius> ?
      <TerrainType>Enum("Coast"/"Water")</TerrainType> ?
      <SkipUnlockMessage>Binary(Default 0)</SkipUnlockMessage> 1 if unlocked from game start
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
      <BuildingBlockPool> for building block which is used for tier 4 and tier 5 residence
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
    <Blocking /> * TODO
    <Cost> * building construction cost
      <Costs>
        <Item>
          <Ingredient>GUID</Ingredient> * the GUID of resource
          <Amount>NaturalInteger(Default 0)</Amount> the amount of resource needed
        </Item>
        ...
      </Costs>
    </Cost>
    <Object> TODO
      <Variations>
        <Item>
          <Filename>data/graphics/buildings/production/agriculture_01/agriculture_01.cfg
          </Filename>
        </Item>
      </Variations>
    </Object>
    <Mesh /> TODO
    <Selection> TODO
      <ParticipantMessageArcheType>Resident_tier01_atWork</ParticipantMessageArcheType>
      <Colors>
        <WeakSelectionColorType>NoColor</WeakSelectionColorType>
      </Colors>
    </Selection>
    <Constructable /> TODO
    <Locked /> TODO
    <SoundEmitter> TODO
      <ActiveSounds>
        <Item>
          <Sound>214800</Sound>
        </Item>
        <Item>
          <Sound>206376</Sound>
        </Item>
      </ActiveSounds>
      <ConstructionSounds>
        <BuildMoveSuccess>
          <Item>
            <VectorElement>
              <InheritedIndex>0</InheritedIndex>
              <InheritanceMapV2>
                <Entry>
                  <TemplateName>FarmBuilding</TemplateName>
                  <Index>0</Index>
                </Entry>
              </InheritanceMapV2>
            </VectorElement>
            <Sound>214783</Sound>
          </Item>
        </BuildMoveSuccess>
      </ConstructionSounds>
      <MaterialType>Wood</MaterialType>
    </SoundEmitter>
    <FeedbackController /> TODO
    <Infolayer /> TODO
    <UpgradeList /> TODO
    <RandomDummySpawner /> TODO
    <Factory7> *
      <NeededFertility>1010571</NeededFertility>
    </Factory7>
    <FactoryBase>
      <FactoryOutputs>
        <Item>
          <Product>1010192</Product>
          <Amount>1</Amount>
          <StorageAmount>2</StorageAmount>
        </Item>
      </FactoryOutputs>
      <CycleTime>60</CycleTime>
    </FactoryBase>
    <LogisticNode />
    <ModuleOwner>
      <ModuleLimit>144</ModuleLimit>
      <ConstructionOptions>
        <Item>
          <ModuleGUID>1010270</ModuleGUID>
        </Item>
      </ConstructionOptions>
      <ModuleBuildRadius>0</ModuleBuildRadius>
      <HardFarmsConfig>1</HardFarmsConfig>
    </ModuleOwner>
    <AmbientMoodProvider>
      <AmbientMood>AgricultureBuildingsEurope</AmbientMood>
    </AmbientMoodProvider>
    <Maintenance>
      <Maintenances>
        <Item>
          <Product>1010017</Product>
          <Amount>20</Amount>
          <InactiveAmount>10</InactiveAmount>
        </Item>
        <Item>
          <Product>1010052</Product>
          <Amount>20</Amount>
        </Item>
      </Maintenances>
    </Maintenance>
    <Attackable>
      <MaximumHitPoints>1500</MaximumHitPoints>
      <SelfHealPerHealTick>4</SelfHealPerHealTick>
    </Attackable>
    <IncidentInfectable>
      <Infectable>
        <Illness>
          <Escalated>0</Escalated>
        </Illness>
        <Explosion>
          <Base>0</Base>
          <Escalated>0</Escalated>
        </Explosion>
      </Infectable>
      <Explosion>
        <ExplosionCoreDamage>1000</ExplosionCoreDamage>
        <DamageExplosionChance>0</DamageExplosionChance>
      </Explosion>
      <IncidentInfectionChanceFactors>
        <Fire>
          <DensityFactor>0.025</DensityFactor>
          <DensityDistance>20</DensityDistance>
          <FactoryProductivityFactor>0.1</FactoryProductivityFactor>
          <FactoryUndertimeFactor>0.05</FactoryUndertimeFactor>
        </Fire>
        <Riot>
          <FactoryOvertimeFactor>0.4</FactoryOvertimeFactor>
          <FactoryUndertimeFactor>0.2</FactoryUndertimeFactor>
          <FactoryHappinessFactor>0.2</FactoryHappinessFactor>
          <HappinessThreshold>20</HappinessThreshold>
        </Riot>
      </IncidentInfectionChanceFactors>
    </IncidentInfectable>
    <Pausable />
    <Culture>
      <CultureType>Landscaping</CultureType>
    </Culture>
    <ItemGenerator />
    <QuestObject />
    id                  Standard.GUID                       the GUID of the building
    name                Standard.Name                       the name of the building
    text                Text.LocaText.English.Text          the in-game English name of the building
    session             Building.AssociatedRegion           the list of sessions where the building can be built
    costs       Cost.Costs          the list of build construction costs
        id      .Item.Ingredient    the GUID of resource
        amount  .Item.Amount        the amount of resource needed
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
          <BuildingType>Enum("Residence"/"Logistic"/"Warehouse"/"Other")</BuildingType> ?
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
          <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion>
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
        <Cost>
          <Costs>
            <Item>
              <Ingredient>GUID</Ingredient> *
              <Amount>NaturalInteger(Default 0)</Amount>
            </Item>
            ...
          </Costs>
        </Cost>
        costs       Cost.Costs          the list of build construction costs
            id      .Item.Ingredient    the GUID of resource
            amount  .Item.Amount        the amount of resource needed
        :param node: the Cost node
        """
        self.values["costs"] = list()
        for cost in node.Costs("Item"):
            tmp = {'id': int(cost.Ingredient.string)}
            if cost.Amount:
                tmp['amount'] = int(cost.Amount.string)
            self.values["costs"].append(tmp)
