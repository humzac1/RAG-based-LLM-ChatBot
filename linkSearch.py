import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

def get_html(url):
    """Fetch the HTML content of a webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Checks for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_links(url, pattern):
    """Scrape all the links that match a given pattern from a webpage."""
    html_content = get_html(url)
    if html_content is None:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)  # Use urljoin to construct full URL

        # Debugging: Print all collected links
        print(f"Collected link: {full_url}")

        if re.match(pattern, full_url):
            links.add(full_url)
            print(f"Matched link: {full_url}")

    return list(links)

def recursive_scrape(start_url, pattern, all_links=set(), visited=set(), depth=0, max_depth=2):
    """Recursively scrape links matching the pattern starting from start_url."""
    if depth > max_depth or start_url in visited:
        return all_links
    
    visited.add(start_url)
    links = scrape_links(start_url, pattern)
    for link in links:
        if link not in all_links:
            all_links.add(link)
            recursive_scrape(link, pattern, all_links, visited, depth + 1, max_depth)
    
    return all_links

def main():
    start_url = "" # website that needs to be scraped
    link_pattern = r"" # if you want to give your scraper an example to go off
    
    # Recursively scrape and gather all links
    all_links = recursive_scrape(start_url, link_pattern)
    
    # Save all links to a file
    save_directory = "scraped_links"
    os.makedirs(save_directory, exist_ok=True)
    with open(os.path.join(save_directory, "all_links.txt"), 'w', encoding='utf-8') as file:
        for link in sorted(all_links):
            file.write(link + '\n')
    
    print(f"Saved all links to {os.path.join(save_directory, 'desired_name_of_file.txt')}")

if __name__ == "__main__":
    main()
