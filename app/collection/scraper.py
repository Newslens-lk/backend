from dataclasses import dataclass
from urllib import robotparser

import httpx

from app.collection.sources import PublisherSource
from app.preprocessing.cleaning import USER_AGENT


@dataclass
class ScrapedArticle:
    title: str
    body: str
    publisher: str
    url: str


def is_allowed(source: PublisherSource, url: str) -> bool:
    parser = robotparser.RobotFileParser()
    parser.set_url(source.robots_txt_url)
    parser.read()
    return parser.can_fetch(USER_AGENT, url)


def scrape_article(source: PublisherSource, url: str) -> ScrapedArticle:
    """Fetch and clean a single article page. Title/body extraction is
    outlet-specific and should be implemented per publisher (FR1.1)."""
    if not is_allowed(source, url):
        raise PermissionError(f"Scraping disallowed by robots.txt: {url}")

    response = httpx.get(url, headers={"User-Agent": USER_AGENT}, timeout=10.0)
    response.raise_for_status()

    raise NotImplementedError(
        f"Implement outlet-specific title/body extraction for {source.name}"
    )
