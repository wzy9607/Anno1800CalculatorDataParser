# coding:utf-8


def parse_session_list(session_str: str) -> list:
    """
    Moderate = Old World, Colony01 = New World
    :param session_str:
    :return:
    """
    session_list = [session.strip() for session in session_str.split(';')]
    return session_list
