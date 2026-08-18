from dataclasses import dataclass


@dataclass(frozen=True)
class PublisherSource:
    name: str
    base_url: str
    robots_txt_url: str


# REQ-1.1.1: at least five Sinhala news publishers. Fill in real
# base/robots URLs as scrapers are implemented for each outlet.
PUBLISHER_SOURCES: list[PublisherSource] = [
    # PublisherSource(name="...", base_url="https://...", robots_txt_url="https://.../robots.txt"),
]
