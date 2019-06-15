# coding:utf-8

import bs4


class Asset:
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
