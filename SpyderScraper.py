import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import re
import time

def crawl(start_url, keyword, max_domains=100):
    to_visit = [start_url]
    visited = set()
    domains = set()
    keyword_occurrences = defaultdict(int)

    print(f"Starting crawl from: {start_url}")
    print(f"Searching for keyword: '{keyword}'\n")

    while to_visit and len(domains) < max_domains:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                continue
            content = response.text
        except requests.RequestException:
            continue
    
        occurrences = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
        if occurrences > 0:
            keyword_occurrences[url] = occurrences

        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)
            parsed_url = urlparse(absolute_url)
            domain = parsed_url.netloc

            if domain and domain not in domains:
                domains.add(domain)
                to_visit.append(absolute_url)

        time.sleep(0.5)

    print(f"\nCrawling complete. Found {len(domains)} unique domains.")
    return keyword_occurrences

if __name__ == "__main__":
    start_url = 'https://en.wikipedia.org/wiki/Website'
    keyword = 'File'
    results = crawl(start_url, keyword)

    print("\nPages containing the keyword:")
    for url, count in results.items():
        print(f"{url}: {count} occurrences")