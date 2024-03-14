# zshahid
# Zaid Shahid
import sys


# Inputs: file_path: the path to the file containing URLs
# Outputs: A list of URLs read from the file
# Purpose: Read URLs from a file 
def read_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Inputs: also file_path
# Outputs: predecessors (a dictionary where keys = URL and values = sets of URLs that link to the key)
#          all_urls: set of all unique URLs in link piars
# Purpose: Read the links from the file and build the predecessors map
def read_links(file_path):
    predecessors = {}
    all_urls = set()
    line_number = 0
    with open(file_path, 'r') as file:
        for line in file:
            line_number += 1
            parts = line.strip().split()
            # I hate this
            if len(parts) != 2:
                print(f"Error on line {line_number}: {len(parts)} in {line.strip()}")
                continue
            src, dest = parts
            if dest not in predecessors:
                predecessors[dest] = set()
            predecessors[dest].add(src)
            # Add both to all_urls set
            all_urls.update([src, dest])  
    return predecessors, all_urls


# Inputs: urls: a list of all URLs in the graph
#          predecessors (a dictionary where keys = URL and values = sets of URLs that link to the key)
#          d: probability of following a link
#          convergence_threshold: the threshold for the convergence 
# Outputs:
#          dictionary where keys are URLs and values are their PageRank scores
# Purpose: Compute PageRank for a set of URLs
def pagerank(urls, predecessors, d, convergence_threshold):
    N = len(urls)
    pageranks = {url: 1 / N for url in urls}
    iterations = 0
    convergence = False

    #Paging the Rank
    while not convergence:
        iterations += 1
        new_pageranks = {url: (1 - d) / N for url in urls}
        convergence = True

        for url in urls:
            #do the shitt????
            sum_of_incoming_ranks = sum(pageranks[prev_url] / len(predecessors.get(prev_url, [])) for prev_url in predecessors.get(url, []))
            new_pageranks[url] += d * sum_of_incoming_ranks

        # Checking for convergence
        for url in urls:
            if abs(new_pageranks[url] - pageranks[url]) >= convergence_threshold:
                convergence = False
                break

        pageranks = new_pageranks

    print(f"PageRank converged after {iterations} iterations.")
    return pageranks

def main(urls_file, links_file, convergence_threshold):
    urls = read_urls(urls_file)
    predecessors, all_links_urls = read_links(links_file)
    #create new set of urls
    all_urls = set(urls) | all_links_urls
    ranks = pagerank(all_urls, predecessors, d=0.85, convergence_threshold=convergence_threshold)

    #sort the URLs by reverse order score
    sorted_ranks = sorted(ranks.items(), key=lambda item: item[1], reverse=True)


    # outputting
    with open('pagerank.output', 'w') as file:
        for url, rank in sorted_ranks:
            file.write(f"{url} {rank}\n")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python pagerank.py crawler.output links.output 0.001")
        sys.exit(1)

    crawler_output_file = sys.argv[1]
    links_output_file = sys.argv[2]
    convergence_threshold = float(sys.argv[3])

    main(crawler_output_file, links_output_file, convergence_threshold)
