# -*- coding: utf-8 -*-
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Scrapper():
    def __init__(self, number_of_pages,start_urls, dict_path = 'app_data/documents'):
        self.start_urls = start_urls
        self.number_of_pages = number_of_pages
        self.dict_path = dict_path

    def scrap(self, url):
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        url_links = []
        parsed_url = urlparse(url)
        page = os.path.basename(parsed_url.path)
        flag = False
        if os.path.exists(f'{self.dict_path}/{page}.html'):
            flag = True
        with open(f'{self.dict_path}/{page}.html', 'w', encoding='utf-8') as file:
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                file.write(tag.text + '\n')
                for link in tag.find_all('a'):
                    if link.get('href') != None and link.get('href').startswith('/wiki/') and ':' not in link.get('href'):
                        url_links.append('https://en.wikipedia.org' + link.get('href'))
        if os.path.getsize(f'{self.dict_path}/{page}.html') < 2000:
            os.remove(f'{self.dict_path}/{page}.html')
            return url_links, False
        if flag:
            return url_links, False
        return url_links, True

    def BFS_scrapping(self,start_url,number):
        visited = set()
        queue = deque([start_url])
        while number > 0 and queue:
            url = queue.popleft()
            if url not in visited:
                visited.add(url)
                links, scrapped = self.scrap(url)
                if scrapped:
                    number -= 1
                for link in links:
                    queue.append(link)
    
    def scrap_all(self):
        number = self.number_of_pages//len(self.start_urls)
        rest = self.number_of_pages % len(self.start_urls)
        flag = True
        for url in self.start_urls:
            if flag:
                self.BFS_scrapping(url,number+rest)
                flag = False
            else:
                self.BFS_scrapping(url,number)

