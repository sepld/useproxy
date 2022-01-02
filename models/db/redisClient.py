from redis.exceptions import TimeoutError, ConnectionError, ResponseError
from redis.connection import BlockingConnectionPool
from random import choice
from redis import Redis
import json
from loguru import logger



class RedisClient(object):
    """
    Redis client

    Redis中代理存放的结构为hash：
    key为ip:port, value为代理属性的字典;

    """
    def __init__(self, **kwargs):
        """
        init
        :param host: host
        :param port: port
        :param password: password
        :param db: db
        :return:
        """
        self.name = "proxy_temp"
        kwargs.pop("username")
        self.__conn = Redis(connection_pool=BlockingConnectionPool(
            decode_responses=True, timeout=5, socket_timeout=5, **kwargs))

    def get(self):
        """
        返回一个代理
        :return:
        """
        proxies = self.__conn.hkeys(self.name)
        proxy = choice(proxies) if proxies else None
        return self.__conn.hget(self.name, proxy) if proxy else None

    def get_one(self, proxy):
        """
        返回指定代理
        """
        return self.__conn.hget(self.name, proxy)

    def put(self, proxy_obj):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy_obj: Proxy obj
        :return:
        """
        self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.to_json) 


    def pop(self):
        """
        弹出一个代理
        :return: dict {proxy: value}
        """
        proxy = self.get()
        if proxy:
            self.__conn.hdel(self.name, json.loads(proxy).get("proxy", ""))
        return proxy if proxy else None

    def delete(self, proxy_str):
        """
        移除指定代理, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hdel(self.name, proxy_str)

    def exists(self, proxy_str):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hexists(self.name, proxy_str)

    def getAll(self):
        """
        字典形式返回所有代理, 使用changeTable指定hash name
        :return:
        """
        items = self.__conn.hvals(self.name)
        return items

    def clear(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        return self.__conn.delete(self.name)

    def getCount(self):
        """
        返回代理数量
        :return:
        """
        proxies = self.getAll()
        return {'total': len(proxies)}

    def changeTable(self, name):
        """
        切换操作对象
        :param name:
        :return:
        """
        self.name = name

    def test(self):
        try:
            self.getCount()
        except TimeoutError as e:
            return e
        except ConnectionError as e:
            return e
        except ResponseError as e:
            return e


if __name__ == "__main__":
    rc = RedisClient()
    print(rc.get())
