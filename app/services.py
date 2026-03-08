import requests
from bs4 import BeautifulSoup
from .utils import make_absolute, normalize_url

CACHE = {}


def get_meta_content(soup, attr_name, attr_value):
    tag = soup.find("meta", attrs={attr_name: attr_value})
    if tag:
        return tag.get("content")
    return None


def extract_metadata(target_url: str):
    target_url = normalize_url(target_url)

    if target_url in CACHE:
        return CACHE[target_url]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(target_url, headers=headers, timeout=10)
    response.raise_for_status()

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

    og_title = get_meta_content(soup, "property", "og:title")
    twitter_title = get_meta_content(soup, "name", "twitter:title")
    og_type = get_meta_content(soup, "property", "og:type")

    domain = target_url.split("//")[-1].split("/")[0]

    preview = {
        "title": og_title or twitter_title or title,
        "description": description,
        "image": image,
        "domain": domain
    }

    result = {
        "title": title,
        "description": description,
        "image": image,
        "favicon": favicon,
        "site_name": site_name,
        "url": target_url,
        "og_title": og_title,
        "twitter_title": twitter_title,
        "og_type": og_type,
        "preview": preview
    }

    CACHE[target_url] = result
    return result