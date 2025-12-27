"""
URL Discovery Module for RAG Ingestion Pipeline

Discovers all accessible URLs from a GitHub Pages site.
"""
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
from typing import List


def discover_urls(base_url: str) -> List[str]:
    """
    Discover all accessible URLs from a GitHub Pages site.

    Args:
        base_url (str): Base URL of the GitHub Pages site

    Returns:
        List[str]: List of discovered URLs
    """
    discovered_urls = set()

    # First, try to get sitemap
    sitemap_url = urljoin(base_url, "sitemap.xml")
    sitemap_urls = _discover_from_sitemap(sitemap_url)
    discovered_urls.update(sitemap_urls)

    # If sitemap didn't provide URLs, crawl the site
    if not discovered_urls:
        discovered_urls.update(_crawl_site(base_url))

    return list(discovered_urls)


def _discover_from_sitemap(sitemap_url: str) -> List[str]:
    """Discover URLs from sitemap.xml if available."""
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            urls = []
            for loc in soup.find_all('loc'):
                urls.append(loc.text.strip())
            return urls
    except Exception as e:
        logging.warning(f"Could not fetch sitemap: {e}")

    return []


def _crawl_site(base_url: str) -> List[str]:
    """Crawl the site to discover URLs."""
    discovered_urls = set()
    to_visit = [base_url]
    visited = set()

    while to_visit:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code == 200:
                discovered_urls.add(current_url)

                # Parse for additional links
                soup = BeautifulSoup(response.content, 'html.parser')

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)

                    # Only add URLs from the same domain
                    if urlparse(full_url).netloc == urlparse(base_url).netloc:
                        if full_url not in visited and full_url.startswith(base_url):
                            to_visit.append(full_url)

        except Exception as e:
            logging.warning(f"Could not crawl {current_url}: {e}")

    return list(discovered_urls)