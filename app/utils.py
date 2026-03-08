from urllib.parse import urljoin


def make_absolute(base_url: str, link: str | None):
    if not link:
        return None
    return urljoin(base_url, link)


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url