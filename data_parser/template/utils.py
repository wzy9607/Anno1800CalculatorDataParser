# coding:utf-8


def parse_session_list(session_str: str) -> list:
    """
    Moderate = Old World, Colony01 = New World
    :param session_str:
    :return:
    """
    session_list = [session.strip() for session in session_str.split(';')]
    return session_list


def grab_name(guid: int, assets_map: dict) -> dict:
    """
    
    :param guid: the GUID of wanted asset
    :param assets_map: assets map
    :return: a dict contains the name and text of that asset
    """
    node = assets_map.get(guid)
    name = str(node.Values.Standard.Name.string)
    text = str(node.Values.Text.LocaText.English.Text.string)
    return {'name': name, 'text': text}
