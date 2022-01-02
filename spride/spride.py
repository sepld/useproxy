from spride.crawlers import __all__ as crawlers_cls
from models.proxyHandler import ProxyHandler
from models.proxy_model import Proxy
import asyncio


class Spride(object):
    """
    """
    def __init__(self):
        """
        """
        self.crawlers_cls = crawlers_cls
        self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]
        self.task_list = list()
        self.proxy_handler = ProxyHandler()
        self.sem = None

    async def exec_task(self, task):
        async with self.sem:
            proxys = await task
            await self.schedule_proxy(proxys)

    async def put_proxy(self, proxy):
        self.proxy_handler.db.changeTable('proxy_default')
        if not self.proxy_handler.exists(proxy):
            self.proxy_handler.put(Proxy(proxy))

    async def schedule_proxy(self, proxys):
        for proxy in proxys:
            await self.put_proxy(proxy)

    async def schedule_tasks(self):
        for crawler in self.crawlers:
            self.task_list += [
                self.exec_task(crawler.crawl(url)) for url in crawler.urls
            ]

    async def main(self):
        await self.schedule_tasks()
        self.sem = asyncio.Semaphore(10000)
        await asyncio.gather(*self.task_list)


if __name__ == '__main__':
    spride = Spride()
    asyncio.run(spride.main())

