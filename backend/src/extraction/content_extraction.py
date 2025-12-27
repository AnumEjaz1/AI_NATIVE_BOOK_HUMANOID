"""
Content Extraction Module for RAG Ingestion Pipeline

Extracts clean text content from web pages while preserving structural metadata.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging


class Document:
    def __init__(self, url: str, title: str, content: str, html_content: Optional[str] = None,
                 headings: Optional[List[str]] = None, sections: Optional[List[str]] = None):
        self.id = url  # Using URL as ID for simplicity
        self.url = url
        self.title = title
        self.content = content
        self.html_content = html_content
        self.headings = headings or []
        self.sections = sections or []


def extract_content(url: str) -> Document:
    """
    Extract clean text content from a single URL.

    Args:
        url (str): URL to extract content from

    Returns:
        Document: Document object with content and metadata
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Could not fetch content from {url}: {e}")
        raise

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Extract title
    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ""

    # Extract headings (h1, h2, h3, h4, h5, h6)
    headings = []
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        headings.append(heading.get_text().strip())

    # Extract content using Docusaurus-specific selectors first
    content_selectors = [
        '.main-wrapper',  # Common Docusaurus wrapper
        'article.markdown',  # Docusaurus markdown article
        '.theme-doc-markdown',  # Docusaurus doc markdown
        '.container',  # General container
        'main',  # Main content area
        '.content',  # Generic content class
        'body'  # Fallback to body
    ]

    content = ""
    for selector in content_selectors:
        if selector == 'body':
            content = soup.get_text()
        else:
            elements = soup.select(selector)
            if elements:
                content = " ".join([elem.get_text() for elem in elements])
                break

    # Clean up the content
    lines = (line.strip() for line in content.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    content = ' '.join(chunk for chunk in chunks if chunk)

    return Document(
        url=url,
        title=title,
        content=content,
        html_content=html_content,
        headings=headings
    )