import requests
from bs4 import BeautifulSoup
from .utils import make_absolute

CACHE = {}


def get_meta_content(soup, attr_name, attr_value):
    tag = soup.find("meta", attrs={attr_name: attr_value})
    if tag:
        return tag.get("content")
    return None


def extract_metadata(target_url: str):
    if target_url in CACHE:
        return CACHE[target_url]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise Exception("Could not access this website (it may block automated requests)")

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else None

    description = (
        get_meta_content(soup, "name", "description")
        or get_meta_content(soup, "property", "og:description")
        or get_meta_content(soup, "name", "twitter:description")
    )

    image = (
        get_meta_content(soup, "property", "og:image")
        or get_meta_content(soup, "name", "twitter:image")
    )

    site_name = get_meta_content(soup, "property", "og:site_name")

    favicon = None
    icon_link = soup.find("link", rel=lambda x: x and "icon" in x.lower())
    if icon_link:
        favicon = icon_link.get("href")

    if not favicon:
        favicon = "/favicon.ico"

    image = make_absolute(target_url, image)
    favicon = make_absolute(target_url, favicon)

    result = {
        "title": title,
        "description": description,
        "image": image,
        "favicon": favicon,
        "site_name": site_name,
        "url": target_url
    }

    CACHE[target_url] = result
    return result