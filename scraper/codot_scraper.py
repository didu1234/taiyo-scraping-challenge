import requests
from bs4 import BeautifulSoup
from typing import List
from models.project import Project

BASE_URL = "https://www.codot.gov"
STIP_URL = BASE_URL + "/programs/planning/transportation-plans-and-studies/stip"


def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}")

    return BeautifulSoup(response.text, "html.parser")


def extract_year(text: str):
    for year in range(2000, 2035):
        if str(year) in text:
            return str(year)
    return None


def parse_stip_listing(soup: BeautifulSoup) -> List[Project]:
    projects = []

    content = soup.select_one("div#content-core")
    links = content.select("a[href]")

    for link in links:
        title = link.get_text(strip=True)
        href = link["href"]

        if not title or not href:
            continue

        project = Project(
            title=title,
            program="Statewide Transportation Improvement Program",
            year=extract_year(title),
            description=None,  # Not available on listing
            document_url=href if href.startswith("http") else BASE_URL + href,
            source_page=STIP_URL
        )

        projects.append(project)

    return projects


def scrape_codot_stip():
    soup = fetch_page(STIP_URL)
    return parse_stip_listing(soup)
