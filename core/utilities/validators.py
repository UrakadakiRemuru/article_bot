import re

def is_valid_url(url: str) -> bool:
    """
    Проверяет, соответствует ли строка формату URL.

    Args:
        url (str): Строка для проверки.

    Returns:
        bool: True, если строка — валидный URL, иначе False.
    """
    pattern = re.compile(
        r'^https?://'
        r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
        r'(?:/[\w\-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    )
    return re.match(pattern, url) is not None
