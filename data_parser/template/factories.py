# coding:utf-8
import abc

import bs4

from .building import Building


class Factory(Building):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <InfoDescription>11143</InfoDescription>
    </Standard>
    <Text .../> *
    <Building> *
      <BuildingType>"Factory"</BuildingType>
      <BuildingCategoryName>100000</BuildingCategoryName>
      <TerrainType>Enum("Coast"/"Water")</TerrainType>
      <SkipUnlockMessage>Binary(Default 0)</SkipUnlockMessage>
      <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Building>
    <Blocking> * TODO
      <DeletePropsRadius>1</DeletePropsRadius>
    </Blocking>
    <Cost .../> *
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
    <Factory7 .../> *
    <FactoryBase .../>
    <LogisticNode /> TODO
    <Slot .../> TODO
    <ModuleOwner> TODO
      <ModuleLimit>144</ModuleLimit>
      <ConstructionOptions>
        <Item>
          <ModuleGUID>1010270</ModuleGUID>
        </Item>
      </ConstructionOptions>
      <ModuleBuildRadius>0</ModuleBuildRadius>
      <HardFarmsConfig>1</HardFarmsConfig>
    </ModuleOwner>
    <AmbientMoodProvider> TODO
      <AmbientMood>AgricultureBuildingsEurope</AmbientMood>
      <Murmur>Farm</Murmur>
      <DynamicEnvironmentType>None</DynamicEnvironmentType>
    </AmbientMoodProvider>
    <Maintenance .../> *
    <Attackable> TODO
      <MaximumHitPoints>1500</MaximumHitPoints>
      <SelfHealPerHealTick>4</SelfHealPerHealTick>
    </Attackable>
    <FreeAreaProductivity> TODO
      <InfluenceRadius>11</InfluenceRadius>
      <WorkerUnit>102433</WorkerUnit>
      <MaxWorkerAmount>3</MaxWorkerAmount>
      <WorkerPause>10000</WorkerPause>
    </FreeAreaProductivity>
    <IncidentInfectable> TODO
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
    <Pausable /> TODO
    <Culture> TODO
      <CultureType>Landscaping</CultureType>
      <HasPollution>1</HasPollution>
    </Culture>
    <IncidentInfluencer> TODO
      <Influence>
        <Illness>
          <Distance>10</Distance>
        </Illness>
      </Influence>
    </IncidentInfluencer>
    <Electric /> TODO
    <ItemGenerator /> TODO
    <QuestObject /> TODO
    id                      Standard.GUID               GUID of the building
    name                    Standard.Name               name of the building
    text                    Text.LocaText.English.Text  in-game English name of the building
    session                 Building.AssociatedRegion   a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    needed_fertility        Factory7.NeededFertility    some factory requires certain island fertility
    inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product consumed per cycle
        amount_per_minute                               amount of product consumed per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product produced per cycle
        amount_per_minute                               amount of product produced per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
    maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
        id                  .Item.Product               GUID of the product
        amount              .Item.Amount                amount of product consumed per minute(?)
        inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                            paused
        shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                            less than this threshold
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
        self.parse_node_factory(self.values_node.Factory7)
        self.parse_node_factory_base(self.values_node.FactoryBase)
        self.parse_node_maintenance(self.values_node.Maintenance)
    
    def parse_node_factory(self, node: bs4.Tag):
        """
        <Factory7>
          <NeededFertility>GUID</NeededFertility> some factory requires certain island fertility
        </Factory7>
        needed_fertility    Factory7.NeededFertility    some factory requires certain island fertility
        :param node: the Factory7 node
        """
        if node.NeededFertility:
            self.values["needed_fertility"] = int(node.NeededFertility.string)
    
    def parse_node_factory_base(self, node: bs4.Tag):
        """
        <FactoryBase>
          <FactoryInputs> products that the factory consumes
            <Item>
              <Product>GUID</Product> * GUID of product
              <Amount>NaturalInteger</Amount> * amount consumed per cycle
              <StorageAmount>NaturalInteger</StorageAmount> * amount of product that the factory can store
            </Item>
            ...
          </FactoryInputs>
          <FactoryOutputs> * products that the factory produces
            <Item>
              <Product>GUID</Product> * GUID of product
              <Amount>NaturalInteger</Amount> * amount of product produced per cycle
              <StorageAmount>NaturalInteger</StorageAmount> * amount of product that the factory can store
            </Item>
            ...
          </FactoryOutputs>
          <CycleTime>NaturalInteger(Default 30)</CycleTime> the time of a production cycle (second)
        </FactoryBase>
        inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
            id                  .Item.Product               GUID of product
            amount              .Item.Amount                amount of product consumed per cycle
            amount_per_minute                               amount of product consumed per minute
            storage_amount      .Item.StorageAmount         amount of product that the factory can store
        outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
            id                  .Item.Product               GUID of product
            amount              .Item.Amount                amount of product produced per cycle
            amount_per_minute                               amount of product produced per minute
            storage_amount      .Item.StorageAmount         amount of product that the factory can store
        production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
        :param node: the FactoryBase node
        """
        if node.CycleTime:
            production_time = int(node.CycleTime.string) / 60.0
        else:
            production_time = 0.5
        self.values['inputs'] = list()
        if node.FactoryInputs:
            for item in node.FactoryInputs("Item"):
                input1 = dict()
                input1['id'] = int(item.Product.string)
                input1['amount'] = int(item.Amount.string)
                input1['amount_per_minute'] = float(input1['amount']) / production_time
                input1['storage_amount'] = float(item.StorageAmount.string)
                self.values['inputs'].append(input1)
        self.values['outputs'] = list()
        for item in node.FactoryOutputs("Item"):
            output = dict()
            output['id'] = int(item.Product.string)
            output['amount'] = int(item.Amount.string)
            output['amount_per_minute'] = float(output['amount']) / production_time
            output['storage_amount'] = float(item.StorageAmount.string)
            self.values['outputs'].append(output)
        self.values['production_time'] = production_time
    
    def parse_node_maintenance(self, node: bs4.Tag):
        """
        <Maintenance>
          <ConsumerPriority>1</ConsumerPriority> ?
          <Maintenances> * products (money, workforce, etc.) used for factory maintenance
            <Item>
              <Product>GUID</Product> * GUID of the product
              <Amount>NaturalInteger</Amount> * amount of product consumed per minute(?)
              <InactiveAmount>NaturalInteger(Default 0)</InactiveAmount> amount of product consumed per minute(?)
                                                                             when the factory is paused
              <ShutdownThreshold>Float(Default 0)</ShutdownThreshold> the factory will be shutdown if workforce fulfill
                                                                          rate is less than this threshold
            </Item>
            ...
          </Maintenances>
        </Maintenance>
        maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
            id                  .Item.Product               GUID of the product
            amount              .Item.Amount                amount of product consumed per minute(?)
            inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                                paused
            shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                                less than this threshold
        :param node: the Maintenance node
        """
        self.values['maintenances'] = list()
        for item in node.Maintenances("Item"):
            maintenance = dict()
            maintenance['id'] = int(item.Product.string)
            maintenance['amount'] = int(item.Amount.string)
            if item.InactiveAmount:
                maintenance['inactive_amount'] = int(item.InactiveAmount.string)
            else:
                maintenance['inactive_amount'] = 0
            if item.ShutdownThreshold:
                maintenance['shutdown_threshold'] = float(item.ShutdownThreshold.string)
            else:
                maintenance['shutdown_threshold'] = 0.0
            self.values['maintenances'].append(maintenance)


class FarmBuilding(Factory):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <InfoDescription>11143</InfoDescription>
    </Standard>
    <Text .../> *
    <Building />
      <BuildingType>"Factory"</BuildingType>
      <BuildingCategoryName>100000</BuildingCategoryName>
      <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Building>
    <Blocking /> *
    <Cost .../> *
    <Object ...> *
    <Mesh /> *
    <Selection .../> *
    <Constructable /> *
    <Locked /> *
    <SoundEmitter .../> *
    <FeedbackController /> *
    <Infolayer /> *
    <UpgradeList /> *
    <RandomDummySpawner /> *
    <Factory7 .../> *
    <FactoryBase .../> *
    <LogisticNode /> *
    <ModuleOwner .../> *
    <AmbientMoodProvider .../> *
    <Maintenance .../> *
    <Attackable .../> *
    <IncidentInfectable .../> *
    <Pausable /> *
    <Culture .../> *
    <ItemGenerator /> *
    <QuestObject /> *
    id                      Standard.GUID               GUID of the building
    name                    Standard.Name               name of the building
    text                    Text.LocaText.English.Text  in-game English name of the building
    session                 Building.AssociatedRegion   a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    needed_fertility        Factory7.NeededFertility    some factory requires certain island fertility
    inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product consumed per cycle
        amount_per_minute                               amount of product consumed per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product produced per cycle
        amount_per_minute                               amount of product produced per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
    maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
        id                  .Item.Product               GUID of the product
        amount              .Item.Amount                amount of product consumed per minute(?)
        inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                            paused
        shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                            less than this threshold
    """
    template_name = "FarmBuilding"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()


class FreeAreaBuilding(Factory):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <InfoDescription>11143</InfoDescription>
    </Standard>
    <Text .../> *
    <Building />
      <BuildingType>"Factory"</BuildingType>
      <BuildingCategoryName>100000</BuildingCategoryName>
      <SkipUnlockMessage>Binary(Default 0)</SkipUnlockMessage>
      <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Building>
    <Blocking .../> *
    <Cost .../> *
    <Object ...> *
    <Mesh /> *
    <Selection .../> *
    <Constructable /> *
    <Locked /> *
    <SoundEmitter .../> *
    <FeedbackController /> *
    <Infolayer /> *
    <UpgradeList /> *
    <RandomDummySpawner /> *
    <Factory7 .../> *
    <FactoryBase .../> *
    <LogisticNode /> *
    <AmbientMoodProvider .../> *
    <Maintenance .../> *
    <Attackable .../> *
    <FreeAreaProductivity .../> *
    <Pausable /> *
    <IncidentInfectable .../> *
    <Culture .../> *
    <ItemGenerator /> *
    id                      Standard.GUID               GUID of the building
    name                    Standard.Name               name of the building
    text                    Text.LocaText.English.Text  in-game English name of the building
    session                 Building.AssociatedRegion   a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    needed_fertility        Factory7.NeededFertility    some factory requires certain island fertility
    inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product consumed per cycle
        amount_per_minute                               amount of product consumed per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product produced per cycle
        amount_per_minute                               amount of product produced per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
    maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
        id                  .Item.Product               GUID of the product
        amount              .Item.Amount                amount of product consumed per minute(?)
        inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                            paused
        shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                            less than this threshold
    """
    template_name = "FreeAreaBuilding"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()


class HeavyFreeAreaBuilding(Factory):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <InfoDescription>11143</InfoDescription>
    </Standard>
    <Text .../> *
    <Building />
      <BuildingType>"Factory"</BuildingType>
      <BuildingCategoryName>100000</BuildingCategoryName>
      <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Building>
    <Blocking .../> *
    <Cost .../> *
    <Object ...> *
    <Mesh /> *
    <Selection .../> *
    <Constructable /> *
    <Locked /> *
    <SoundEmitter .../> *
    <FeedbackController /> *
    <Infolayer /> *
    <UpgradeList /> *
    <RandomDummySpawner /> *
    <Factory7 .../> *
    <FactoryBase .../> *
    <LogisticNode /> *
    <AmbientMoodProvider .../> *
    <Maintenance .../> *
    <Attackable .../> *
    <Pausable /> *
    <IncidentInfectable .../> *
    <Culture .../> *
    <IncidentInfluencer .../> *
    <FreeAreaProductivity .../> *
    <Electric /> *
    id                      Standard.GUID               GUID of the building
    name                    Standard.Name               name of the building
    text                    Text.LocaText.English.Text  in-game English name of the building
    session                 Building.AssociatedRegion   a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    needed_fertility        Factory7.NeededFertility    some factory requires certain island fertility
    inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product consumed per cycle
        amount_per_minute                               amount of product consumed per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product produced per cycle
        amount_per_minute                               amount of product produced per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
    maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
        id                  .Item.Product               GUID of the product
        amount              .Item.Amount                amount of product consumed per minute(?)
        inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                            paused
        shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                            less than this threshold
    """
    template_name = "HeavyFreeAreaBuilding"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()


class FactoryBuilding(Factory):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <InfoDescription>11143</InfoDescription>
    </Standard>
    <Text .../> *
    <Building />
      <BuildingType>"Factory"</BuildingType>
      <BuildingCategoryName>100000</BuildingCategoryName>
      <TerrainType>Enum("Coast"/"Water")</TerrainType>
      <SkipUnlockMessage>Binary(Default 0)</SkipUnlockMessage>
      <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Building>
    <Blocking .../> *
    <Cost .../> *
    <Object ...> *
    <Mesh /> *
    <Selection .../> *
    <Constructable /> *
    <Locked /> *
    <SoundEmitter .../> *
    <FeedbackController /> *
    <Infolayer /> *
    <UpgradeList /> *
    <RandomDummySpawner /> *
    <Factory7 .../> *
    <FactoryBase .../> *
    <LogisticNode /> *
    <AmbientMoodProvider .../> *
    <Maintenance .../> *
    <Attackable .../> *
    <Pausable /> *
    <IncidentInfectable .../> *
    <Electric /> *
    <Culture .../> *
    <ItemGenerator /> *
    <QuestObject /> *
    id                      Standard.GUID               GUID of the building
    name                    Standard.Name               name of the building
    text                    Text.LocaText.English.Text  in-game English name of the building
    session                 Building.AssociatedRegion   a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    needed_fertility        Factory7.NeededFertility    some factory requires certain island fertility
    inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product consumed per cycle
        amount_per_minute                               amount of product consumed per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product produced per cycle
        amount_per_minute                               amount of product produced per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
    maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
        id                  .Item.Product               GUID of the product
        amount              .Item.Amount                amount of product consumed per minute(?)
        inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                            paused
        shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                            less than this threshold
    """
    template_name = "FactoryBuilding7"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()


class HeavyFactoryBuilding(Factory):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <InfoDescription>11143</InfoDescription>
    </Standard>
    <Text .../> *
    <Building />
      <BuildingType>"Factory"</BuildingType>
      <BuildingCategoryName>100000</BuildingCategoryName>
      <TerrainType>Enum("Coast"/"Water")</TerrainType>
      <SkipUnlockMessage>Binary(Default 0)</SkipUnlockMessage>
      <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Building>
    <Blocking .../> *
    <Cost .../> *
    <Object ...> *
    <Mesh /> *
    <Selection .../> *
    <Constructable /> *
    <Locked /> *
    <SoundEmitter .../> *
    <FeedbackController /> *
    <Infolayer /> *
    <UpgradeList /> *
    <RandomDummySpawner /> *
    <Factory7 .../> *
    <FactoryBase .../> *
    <LogisticNode /> *
    <AmbientMoodProvider .../> *
    <Maintenance .../> *
    <Attackable .../> *
    <Pausable /> *
    <IncidentInfectable .../> *
    <Culture .../> *
    <IncidentInfluencer .../> *
    <Electric /> *
    <ItemGenerator /> *
    <QuestObject /> *
    id                      Standard.GUID               GUID of the building
    name                    Standard.Name               name of the building
    text                    Text.LocaText.English.Text  in-game English name of the building
    session                 Building.AssociatedRegion   a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    needed_fertility        Factory7.NeededFertility    some factory requires certain island fertility
    inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product consumed per cycle
        amount_per_minute                               amount of product consumed per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product produced per cycle
        amount_per_minute                               amount of product produced per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
    maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
        id                  .Item.Product               GUID of the product
        amount              .Item.Amount                amount of product consumed per minute(?)
        inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                            paused
        shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                            less than this threshold
    """
    template_name = "HeavyFactoryBuilding"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()


class SlotFactoryBuilding(Factory):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename> *
      <InfoDescription>11143</InfoDescription>
    </Standard>
    <Text .../> *
    <Building />
      <BuildingType>"Factory"</BuildingType>
      <BuildingCategoryName>100000</BuildingCategoryName>
      <SkipUnlockMessage>Binary(Default 0)</SkipUnlockMessage>
      <BuildModeRandomRotation>Enum(90/180)</BuildModeRandomRotation> *
      <AssociatedRegion>List("Moderate";"Colony01")</AssociatedRegion> *
    </Building>
    <Blocking .../> *
    <Cost .../> *
    <Object ...> *
    <Mesh /> *
    <Selection .../> *
    <Constructable /> *
    <Locked /> *
    <SoundEmitter .../> *
    <FeedbackController /> *
    <Infolayer /> *
    <UpgradeList /> *
    <RandomDummySpawner /> *
    <Factory7 .../> *
    <FactoryBase .../> *
    <LogisticNode /> *
    <Slot /> *
    <AmbientMoodProvider .../> *
    <Maintenance .../> *
    <Attackable .../> *
    <Pausable /> *
    <IncidentInfectable .../> *
    <Culture .../> *
    <Electric /> *
    id                      Standard.GUID               GUID of the building
    name                    Standard.Name               name of the building
    text                    Text.LocaText.English.Text  in-game English name of the building
    session                 Building.AssociatedRegion   a list of sessions where the building can be built
    costs                   Cost.Costs                  a list of resources required for building construction
        id                  .Item.Ingredient            GUID of the resource
        amount              .Item.Amount                amount of resource needed
    needed_fertility        Factory7.NeededFertility    some factory requires certain island fertility
    inputs                  FactoryBase.FactoryInputs   a list of products that the factory consumes
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product consumed per cycle
        amount_per_minute                               amount of product consumed per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    outputs                 FactoryBase.FactoryOutputs  a list of products that the factory produces
        id                  .Item.Product               GUID of product
        amount              .Item.Amount                amount of product produced per cycle
        amount_per_minute                               amount of product produced per minute
        storage_amount      .Item.StorageAmount         amount of product that the factory can store
    production_time         FactoryBase.CycleTime       the time of a production cycle (minute)
    maintenances            Maintenance.Maintenances    a list of products that the factory used for maintenance
        id                  .Item.Product               GUID of the product
        amount              .Item.Amount                amount of product consumed per minute(?)
        inactive_amount     .Item.InactiveAmount        amount of product consumed per minute(?) when the factory is
                                                            paused
        shutdown_threshold  .Item.ShutdownThreshold     the factory will be shutdown if workforce fulfill rate is
                                                            less than this threshold
    """
    template_name = "SlotFactoryBuilding7"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()
