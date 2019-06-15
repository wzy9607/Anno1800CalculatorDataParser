# coding:utf-8

import bs4

from .asset import Asset


class PopulationGroup(Asset):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
    </Standard>
    <Text .../> *
    <PopulationGroup7 .../> *
    id                  Standard.GUID                       the GUID of the population group
    name                Standard.Name                       the name of the population group
    text                Text.LocaText.English.Text          the in-game English name of the population group
    population_levels   PopulationGroup7.PopulationLevels   the list of population levels in the group
    """
    template_name = "PopulationGroup7"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()
        self.parse_node_text(self.values_node.Text)
        self.parse_node_population_group(self.values_node.PopulationGroup7)
    
    def parse_node_population_group(self, node: bs4.Tag):
        """
        <PopulationGroup7>
          <PopulationLevels>
            <Item>
              <Level>GUID</Level> *
            </Item>
            ...
          </PopulationLevels>
        </PopulationGroup7>
        population_levels   PopulationGroup7.PopulationLevels   the list of population levels in the group
        :param node: the PopulationGroup7 node
        """
        self.values['population_levels'] = [int(item.Level.string) for item in node.PopulationLevels("Item")]
