# -*- coding: utf-8 -*-
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Scrapps materials from given url and saves it in the wiki_data folder

class Scrapper():
    def __init__(self, number_of_pages,start_urls):
        self.start_urls = start_urls
        self.number_of_pages = number_of_pages
        if not os.path.exists('app_data/documents'):
            os.makedirs('app_data/documents')

    def scrap(self, url):
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        url_links = []
        parsed_url = urlparse(url)
        page = os.path.basename(parsed_url.path)
        with open(f'app_data/documents/{page}.html', 'w', encoding='utf-8') as file:
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                file.write(tag.text + '\n')
                for link in tag.find_all('a'):
                    if link.get('href') != None and link.get('href').startswith('/wiki/') and ':' not in link.get('href'):
                        url_links.append('https://en.wikipedia.org' + link.get('href'))
        if os.path.getsize(f'app_data/documents/{page}.html') < 2000:
            os.remove(f'app_data/documents/{page}.html')
            return False
        return url_links

    def BFS_scrapping(self,start_url,number):
        visited = set()
        queue = deque([start_url])
        while number > 0 and queue:
            url = queue.popleft()
            if url not in visited:
                visited.add(url)
                links = self.scrap(url)
                if links:
                    number -= 1
                    for link in links:
                        queue.append(link)
    
    def scrap_all(self):
        number = self.number_of_pages//len(self.start_urls)
        for url in self.start_urls:
            self.BFS_scrapping(url,number)

