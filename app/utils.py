from urllib.parse import urljoin


def make_absolute(base_url: str, value: str | None):
    if not value:
        return None
    return urljoin(base_url, value)