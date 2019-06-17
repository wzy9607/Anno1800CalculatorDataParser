# coding:utf-8
import abc

import bs4


class Asset(abc.ABC):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename>
      <ID>Text</ID>
      <InfoDescription>GUID</InfoDescription>
    </Standard>
    <Text>
      <LocaText>
        <English>
          <Text>Text</Text>
          <Status>Enum("Exported"/"ToBeDeleted"/"GameWriting")</Status>
          <ExportCount>NaturalInteger</ExportCount>
        </English>
      </LocaText>
      <LineID>NaturalInteger</LineID>
    </Text>
    """
    
    @property
    @abc.abstractmethod
    def template_name(self):
        ...
    
    def __init__(self, node: bs4.Tag, parse = True):
        # check whether node is using the template that the parser handles or not
        if node.Template.string != self.template_name:
            raise AssertionError("{node} is not an instance of {temp}".format(node = node, temp = self.template_name))
        self.values_node = node.Values
        self.values = dict()
        # parse the node
        if parse:
            self.parse()
    
    def parse(self):
        """
        parse the node, the actual parsers are parse_node_{tag_name}
        """
        self.parse_node_standard(self.values_node.Standard)
    
    def parse_node_standard(self, node: bs4.Tag):
        """
        <Standard>
          <GUID>GUID</GUID> *
          <Name>Text</Name> *
          <IconFilename>Path</IconFilename>
          <ID>Text</ID> ?
          <InfoDescription>GUID</InfoDescription> ?
        </Standard>
        id      Standard.GUID            GUID of the asset
        name    Standard.Name            name of the asset
        icon    Standard.IconFilename    icon path of the asset
        :param node: the Standard node
        """
        self.values['id'] = int(node.GUID.string)
        self.values['name'] = str(node.Name.string)
        if node.IconFilename:
            self.values['icon'] = str(node.IconFilename.string)
    
    def parse_node_text(self, node: bs4.Tag):
        """
        <Text>
          <LocaText>
            <English>
              <Text>Text</Text> *
              <Status>Enum("Exported"/"ToBeDeleted"/"GameWriting")</Status> * ?
              <ExportCount>NaturalInteger</ExportCount> * ?
            </English>
          </LocaText>
          <LineID>NaturalInteger</LineID> * ?
        </Text>
        text    Text.LocaText.English.Text   in-game English name of the asset
        :param node: the Text node
        """
        self.values['text'] = str(node.LocaText.English.Text.string)
