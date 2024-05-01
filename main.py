from processing.web_scrapper import Scrapper
scrapper = Scrapper(9453, ['https://en.wikipedia.org/wiki/Python_(programming_language)'])
scrapper.scrap_all()