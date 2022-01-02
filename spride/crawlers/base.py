import aiohttp
from fake_headers import Headers
from models.proxyHandler import ProxyHandler

GET_TIMEOUT = 10


class BaseCrawler(object):
    urls = []

    def __init__(self):
        self.proxy_handler = ProxyHandler()

    async def get_proxy(self):
        self.proxy_handler.db.changeTable('usable')
        return self.proxy_handler.get()

    async def fetch(self, url, **kwargs):
        try:
            headers = Headers(headers=True).generate()
            kwargs.setdefault('timeout', GET_TIMEOUT)
            kwargs.setdefault('headers', headers)
            proxy = await self.get_proxy()
            if proxy:
                kwargs.update(dict(proxy=f'http://{proxy.proxy}'))
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(
                    ssl=False)) as session:
                async with session.get(url, **kwargs) as response:
                    if response.status == 200:
                        response.encoding = 'utf-8'
                        response_text = await response.text()
                        if response_text:
                            print(f"{url} fetched html, use {proxy.proxy if proxy else None}")
                        return response_text
        except Exception as e:
            # print(f"failed url {url}, {proxy.proxy if proxy else None}, {e}")
            # raise e
            pass

    async def crawl(self, url):
        """
        crawl main method
        """
        html = await self.fetch(url)
        # time.sleep(.5)
        if html:
            return [proxy async for proxy in self.parse(html)]
        else:
            # print(f"{url} response is {html}")
            return []