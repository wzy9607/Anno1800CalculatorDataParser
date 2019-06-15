# coding:utf-8

from .asset import Asset


class Text(Asset):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
    </Standard>
    <Text>
      <LocaText>
        <English>
          <Text>Text</Text> *
          <Status>Option("Exported"/"ToBeDeleted"/"GameWriting")</Status> * ?
          <ExportCount>UnsignedInteger</ExportCount> * ?
        </English>
      </LocaText>
      <LineID>UnsignedInteger</LineID> * ?
    </Text>
    id      Standard.GUID            the GUID of the text
    name    Standard.Name            the name of the text
    text    Text.LocaText.English.Text   the in-game English text of the text
    """
    template_name = "Text"
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        super().parse()
        self.parse_node_text(self.values_node.Text)
