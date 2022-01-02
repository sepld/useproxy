from models.proxy_model import Proxy
from models.db.dbClient import DbClient

DB_CONN = 'redis://:@127.0.0.1:6379/0'
TEMP_TABLE_NAME = 'proxy_default'


class ProxyHandler(object):
    """ Proxy CRUD operator"""
    def __init__(self):
        self.db = DbClient(DB_CONN)
        self.db.changeTable(TEMP_TABLE_NAME)

    def get(self):
        """
        return a proxy
        Args:
            https: True/False
        Returns:
        """
        proxy = self.db.get()
        return Proxy.createFromJson(proxy) if proxy else None

    def get_one(self, proxy):
        pro = self.db.get_one(proxy)
        return Proxy.createFromJson(pro) if pro else None

    def pop(self):
        """
        return and delete a useful proxy
        :return:
        """
        proxy = self.db.pop()
        return Proxy.createFromJson(proxy) if proxy else None

    def put(self, proxy):
        """
        put proxy into use proxy
        :return:
        """
        self.db.put(proxy)

    def delete(self, proxy):
        """
        delete useful proxy
        :param proxy:
        :return:
        """
        return self.db.delete(proxy)

    def getAll(self):
        """
        get all proxy from pool as Proxy list
        :return:
        """
        proxies = self.db.getAll()
        return [Proxy.createFromJson(_) for _ in proxies]

    def exists(self, proxy):
        """
        check proxy exists
        :param proxy:
        :return:
        """
        return self.db.exists(proxy)

    def getCount(self):
        """
        return raw_proxy and use_proxy count
        :return:
        """
        total_use_proxy = self.db.getCount()
        return {'count': total_use_proxy}
