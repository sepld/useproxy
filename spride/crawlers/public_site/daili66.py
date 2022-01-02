from pyquery import PyQuery as pq
from spride.crawlers.base import BaseCrawler

BASE_URL = 'http://www.66ip.cn/{page}.html'

MAX_PAGE = 2000
# MAX_PAGE = 1


class Daili66Crawler(BaseCrawler):
    """
    daili66 crawler, http://www.66ip.cn/1.html
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    async def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('.containerbox table tr:gt(0)').items()
        for tr in trs:
            host = tr.find('td:nth-child(1)').text()
            port = int(tr.find('td:nth-child(2)').text())
            yield f'{host}:{port}'


if __name__ == '__main__':
    crawler = Daili66Crawler()
    for proxy in crawler.crawl():
        print(proxy)
