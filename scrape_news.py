import requests
from bs4 import BeautifulSoup
import time

def get_article_links(base_url, max_links=10):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "article" in href and href.startswith("http"):
            article_links.append(href)
        elif "article" in href:
            article_links.append(base_url + href)
        
        if len(article_links) >= max_links:
            break
    
    return list(set(article_links))

def scrape_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').get_text() if soup.find('h1') else "No Title Found"
    paragraphs = soup.find_all('p')
    content = " ".join([p.get_text() for p in paragraphs])
    return title, content

if __name__ == "__main__":
    website_url = "https://www.bbc.com/news"  # Example website
    article_urls = get_article_links(website_url)
    
    for article_url in article_urls:
        print(f"Scraping: {article_url}")
        title, content = scrape_news(article_url)
        print("Title:", title)
        print("Content Preview:", content[:500])
        time.sleep(1)  # To avoid overwhelming the server
