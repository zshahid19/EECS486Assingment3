# zshahid
# Zaid Shahid
import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin, quote
from collections import deque, OrderedDict
from datetime import datetime


# Input:
#     url: The URL to check
#     domain_set: A set of valid domains
# Output: True if the URL is valid, or false if not
# Purpose: Check if a URL is valid based on the given domain set
def is_valid_url(url, domain_set):
    return any(domain in url for domain in domain_set)


# Input:
#     url: The URL to extract links from
#     domain_set: A set of valid domains
# Output: A set of valid URLs found on the page
# Purpose: Get all valid and absolute links from a given URL.
def get_links(url, domain_set):
    try:
        #wtf is this
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}
        #GET request with a timeout
        response = requests.get(url, headers=headers, timeout=10)
        # Check header for html
        if 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                abs_href = urljoin(url, href)
                # check for http and https
                if abs_href.startswith('http://') or abs_href.startswith('https://'):
                    if is_valid_url(abs_href, domain_set):
                        links.add(abs_href)
            return links
        else:
            return set()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        #print("error getting links")
        print(f"Error fetching links from {url}: {e}")
        return set()



# Input:
#       seed_urls: list of seed URLs to start the crawl from
#       max_urls: maxi number of URLs to crawl
#       domain_set: set of valid domains
# Output: A tuple with list of identified URLs and a set of all links. tupes of src,dest
# Purpose: to crawl the web like spdierman starting from the seed URLs, collecting links up to the inputed max
    
def crawl(seed_urls, max_urls, domain_set):
    visited = set()
    queue = deque(seed_urls)
    identified_urls = []
    all_links = OrderedDict()

    while queue and len(identified_urls) < max_urls:
        #remove trailing slash from the URL
        url = queue.popleft().rstrip('/')  
        if url not in visited:
            visited.add(url)
            identified_urls.append(url)
        # Fetch and store links, even if the page has been visited
        links = get_links(url, domain_set)
        for link in links:
             #remove trailing slash from the link again
            link = link.rstrip('/') 
            # Add the link to all_links, associating it with the current source URL
            if (url, link) not in all_links:
                all_links[(url, link)] = None
            if link not in visited and link not in queue:
                queue.append(link)
            if len(identified_urls) + len(queue) >= max_urls:
                break

    return identified_urls, all_links.keys()



def main(seed_file, max_urls):
    #print starting time
    start_time = datetime.now()
    print(f"Program started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    with open(seed_file, 'r') as file:
        seed_urls = [line.strip() for line in file.readlines()]

    domain_set = {
        'http://eecs.engin.umich.edu',
        'https://eecs.engin.umich.edu',
        'http://eecs.umich.edu',
        'https://eecs.umich.edu',
        'http://ece.engin.umich.edu',
        'https://ece.engin.umich.edu',
        'http://cse.engin.umich.edu',
        'https://cse.engin.umich.edu'
    }

    identified_urls, all_links = crawl(seed_urls, max_urls, domain_set)

    with open('crawler.output', 'w') as file:
        for url in identified_urls:
            file.write(url + '\n')

    
    with open('links.output', 'w') as file:
        for url1, url2 in all_links:
            # had to do thise one weird cause there was one grad student whose page somehow had a space in it??? was messing up everything
            file.write(url1.replace(' ', '%20') + ' ' + url2.replace(' ', '%20') + '\n')

    #to see how long my program takes
    end_time = datetime.now()
    print(f"Program ended at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total runtime: {end_time - start_time}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python crawler.py seed_file max_urls")
        sys.exit(1)

    seed_file = sys.argv[1]
    max_urls = int(sys.argv[2])

    main(seed_file, max_urls)
