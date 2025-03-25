import os
import requests

def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_html_to_file(directory, url, content):
    if content:
        filename = os.path.join(directory, url.replace("http://", "").replace("https://", "").replace("/", "_") + ".html")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

def main(urls_file, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(urls_file, 'r') as file:
        urls = file.read().splitlines()
    
    for url in urls:
        print(f"Fetching {url}")
        content = fetch_html_content(url)
        save_html_to_file(output_directory, url, content)

if __name__ == "__main__":
    urls_file = ""  # The path to your file containing URLs
    output_directory = ""  # Desired output directory
    main(urls_file, output_directory)
