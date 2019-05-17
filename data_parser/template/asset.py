# coding:utf-8

import bs4


class Asset:
    """
    <Values>
      <Standard>
        <GUID></GUID> *
        <Name></Name> *
        <IconFilename></IconFilename>
        <ID></ID>
      </Standard>
      <Text>
        <LocaText>
          <English>
            <Text></Text>
            <Status></Status>
            <ExportCount></ExportCount>
          </English>
        </LocaText>
        <LineID></LineID>
      </Text>
    </Values>
    """
    id = None  # Values.Standard.GUID
    name = None  # Values.Standard.Name
    icon = None  # Values.Standard.IconFilename
    text = None  # Values.Text.LocaText.English.Text
    
    @classmethod
    def parse(cls, node: bs4.Tag, **kwargs) -> dict:
        asset = dict()
        values = node.Values
        asset['id'] = int(values.Standard.GUID.string)
        asset['name'] = str(values.Standard.Name.string)
        if values.Standard.IconFilename:
            asset['icon'] = str(values.Standard.IconFilename.string)
        if values.Text:
            asset['text'] = str(values.Text.LocaText.English.Text.string)
        return asset
