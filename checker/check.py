import json
import aiohttp
from aiohttp_proxy import ProxyConnector as HttpsConnector
from aiohttp_socks import ProxyConnector
import asyncio
from fake_headers import Headers
from models.proxyHandler import ProxyHandler
from models.proxy_model import Proxy
from loguru import logger

headers = Headers(headers=True).generate()


class Checker(object):
    """
    """

    def __init__(self):
        self.proxy_handler = ProxyHandler()
        self.task_type_list = list()
        self.task_location_list = list()
        self.sem = None

    async def put_proxy(self, table, proxy):
        self.proxy_handler.db.changeTable(table)
        self.proxy_handler.put(proxy)

    async def get_proxy(self, table, proxy):
        self.proxy_handler.db.changeTable(table)
        one_proxy = self.proxy_handler.get_one(proxy)
        return one_proxy

    async def aio_req(self, connector):
        async with aiohttp.ClientSession(connector=connector) as session:
            url = 'https://httpbin.org/ip'
            try:
                async with session.get(url, timeout=10,
                                       headers=headers) as response:
                    if response.status in [200, 206, 302]:
                        # js = await response.json()
                        return True
                    else:
                        return False
            except:
                pass

    async def check_http(self, proxy):
        connector = ProxyConnector.from_url(f'http://{proxy}')
        res = await self.aio_req(connector)
        if res:
            logger.debug(f"{proxy} is http")
            proxy_obj = await self.get_proxy("usable", proxy)
            if proxy_obj:
                proxy_type = proxy_obj.proxy_type
                proxy_type.append('http')
                proxy_obj.proxy_type = list(set(proxy_type))
            else:
                proxy_obj = Proxy(proxy)
                http_type = ["http"]
                proxy_obj.proxy_type = http_type
            await self.put_proxy("usable", proxy_obj)

    async def check_https(self, proxy):
        connector = HttpsConnector.from_url(f'https://{proxy}')
        res = await self.aio_req(connector)
        if res:
            logger.debug(f"{proxy} is https")
            proxy_obj = await self.get_proxy("usable", proxy)
            if proxy_obj:
                proxy_type = proxy_obj.proxy_type
                proxy_type.append('https')
                proxy_obj.proxy_type = list(set(proxy_type))
            else:
                proxy_obj = Proxy(proxy)
                http_type = ["https"]
                proxy_obj.proxy_type = http_type
            await self.put_proxy("usable", proxy_obj)

    async def check_socks4(self, proxy):
        connector = ProxyConnector.from_url(f'socks4://{proxy}')
        res = await self.aio_req(connector)
        if res:
            logger.debug(f"{proxy} is socks4")
            proxy_obj = await self.get_proxy("usable", proxy)
            if proxy_obj:
                proxy_type = proxy_obj.proxy_type
                proxy_type.append('socks4')
                proxy_obj.proxy_type = list(set(proxy_type))
            else:
                proxy_obj = Proxy(proxy)
                http_type = ["socks4"]
                proxy_obj.proxy_type = http_type
            await self.put_proxy("usable", proxy_obj)

    async def check_socks5(self, proxy):
        connector = ProxyConnector.from_url(f'socks5://{proxy}')
        res = await self.aio_req(connector)
        if res:
            logger.debug(f"{proxy} is socks5")
            proxy_obj = await self.get_proxy("usable", proxy)
            if proxy_obj:
                proxy_type = proxy_obj.proxy_type
                proxy_type.append('socks5')
                proxy_obj.proxy_type = list(set(proxy_type))
            else:
                proxy_obj = Proxy(proxy)
                http_type = ["socks5"]
                proxy_obj.proxy_type = http_type
            await self.put_proxy("usable", proxy_obj)

    async def check_location(self, proxy_list):
        p_list = [p.proxy.split(":")[0] for p in proxy_list]
        url = 'http://ip-api.com/batch'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url,
                                        data=json.dumps(p_list),
                                        timeout=5,
                                        headers=headers) as response:
                    if response.status in [200, 206, 302]:
                        resp_json = await response.json()
                        # logger.debug(resp_json)
                        await self.sched_location(resp_json, proxy_list)
                    else:
                        logger.debug(response.status)
            except Exception as e:
                print(e)

    async def sched_location(self, resp_data, proxy_list):
        pl = dict()
        for d in proxy_list:
            pl[d.proxy.split(":")[0]] = d
        for rd in resp_data:
            host = rd['query']
            proxy = pl[host]
            proxy.country = rd["country"]
            proxy.city = rd["city"]
            await self.put_proxy("usable", proxy)

    async def schedule_type(self, proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        async with self.sem:
            await asyncio.gather(self.check_http(proxy),
                                 self.check_https(proxy),
                                 self.check_socks4(proxy),
                                 self.check_socks5(proxy))

    async def get_default_proxys(self):
        self.proxy_handler.db.changeTable('proxy_default')
        all_proxy = self.proxy_handler.getAll()
        for proxy in all_proxy:
            yield proxy

    async def get_usable_proxys(self):
        self.proxy_handler.db.changeTable('usable')
        all_proxy = self.proxy_handler.getAll()
        return all_proxy

    async def schedule_type_tasks(self):
        async for proxy in self.get_default_proxys():
            self.task_type_list.append(
                asyncio.create_task(self.schedule_type(proxy.proxy)))

    async def schedule_location_tasks(self):
        all_proxys = await self.get_usable_proxys()
        all_proxys_lists = [
            all_proxys[i:i + 100] for i in range(0, len(all_proxys), 100)
        ]
        for proxy_list in all_proxys_lists:
            await self.check_location(proxy_list)

    async def main(self):
        await self.schedule_type_tasks()
        self.sem = asyncio.Semaphore(1000)
        await asyncio.gather(*self.task_type_list)
        await self.schedule_location_tasks()

    async def run(self):
        """
        test main method
        :return:
        """
        asyncio.run(self.main())


if __name__ == "__main__":
    checker = Checker()
    asyncio.run(checker.main())

    # 检查是否是http代理
    # 检查是否是https代理
    # 检查是否是sock4代理
    # 检查是否是sock5代理
    # 查询地理位置
