# coding:utf-8
import abc

import bs4


class Asset(abc.ABC):
    """
    <Standard>
      <GUID>GUID</GUID> *
      <Name>Text</Name> *
      <IconFilename>Path</IconFilename>
      <ID>Text</ID> ?
      <InfoDescription>GUID</InfoDescription> ?
    </Standard>
    <Text .../>
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
        id      Standard.GUID            the GUID of the asset
        name    Standard.Name            the name of the asset
        icon    Standard.IconFilename    the icon of the asset
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
              <Status>Option("Exported"/"ToBeDeleted"/"GameWriting")</Status> * ?
              <ExportCount>UnsignedInteger</ExportCount> * ?
            </English>
          </LocaText>
          <LineID>UnsignedInteger</LineID> * ?
        </Text>
        text    Text.LocaText.English.Text   the in-game English name of the asset
        :param node: the Text node
        """
        self.values['text'] = str(node.LocaText.English.Text.string)


class AssetOld:
    """
    <Values>
      <Standard>
        <GUID>GUID</GUID> *
        <Name>Text</Name> *
        <IconFilename>Path</IconFilename>
        <ID>Text</ID> ?
        <InfoDescription>GUID</InfoDescription> ?
      </Standard>
      <Text>
        <LocaText>
          <English>
            <Text>Text</Text>
            <Status>Option("Exported"/"ToBeDeleted"/"GameWriting")</Status> ?
            <ExportCount>UnsignedInteger</ExportCount> ?
          </English>
        </LocaText>
        <LineID>UnsignedInteger</LineID> ?
      </Text>
    </Values>
    """
    id = None  # Values.Standard.GUID
    name = None  # Values.Standard.Name
    icon = None  # Values.Standard.IconFilename
    text = None  # Values.Text.LocaText.English.Text
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        """
        parse Values.Standard and Values.Text
        :param node:
        :return: parsing result in a dict
        """
        asset = dict()
        values = node.Values
        asset['id'] = int(values.Standard.GUID.string)
        asset['name'] = str(values.Standard.Name.string)
        if values.Standard.IconFilename:
            asset['icon'] = str(values.Standard.IconFilename.string)
        if values.Text:
            asset['text'] = str(values.Text.LocaText.English.Text.string)
        return asset
    
    @classmethod
    def grab_name(cls, assets_map: dict, id: int) -> dict:
        node = assets_map.get(id)
        name = str(node.Values.Standard.Name.string)
        text = str(node.Values.Text.LocaText.English.Text.string)
        return {'name': name, 'text': text}


class ProductInStream:
    id = None  # Product
    amount = None  # Amount
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        product = dict()
        product['id'] = int(node.Product.string)
        if node.Amount:
            product['amount'] = float(node.Amount.string)
        return product
