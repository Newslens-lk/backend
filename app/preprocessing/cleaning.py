import re
import unicodedata

import httpx
from bs4 import BeautifulSoup

_WHITESPACE_RE = re.compile(r"\s+")
USER_AGENT = "NewslensBot/0.1 (+https://github.com/Newslens-lk)"


def clean_text(raw_text: str) -> str:
    """Strip markup/whitespace and normalise Unicode for Sinhala text (FR1.1)."""
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(separator=" ")
    text = unicodedata.normalize("NFC", text)
    return _WHITESPACE_RE.sub(" ", text).strip()


def fetch_and_clean_url(url: str) -> str:
    response = httpx.get(
        url, headers={"User-Agent": USER_AGENT}, timeout=10.0, follow_redirects=True
    )
    response.raise_for_status()
    return clean_text(response.text)
