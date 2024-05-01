from processing.web_scrapper import Scrapper
scrapper = Scrapper(100000,['https://en.wikipedia.org/wiki/Tornado','https://en.wikipedia.org/wiki/Mieszko_I','https://en.wikipedia.org/wiki/Algorithm'])
scrapper.scrap_all()