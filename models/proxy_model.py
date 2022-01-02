import json


class Proxy(object):
    def __init__(self,
                 proxy,
                 country="",
                 city="",
                 anonymity="",
                 check_count=0,
                 status=True,
                 last_time="",
                 proxy_type=[]):
        self._proxy = proxy
        self._city = city
        self._country = country
        self._anonymity = anonymity
        self._check_count = check_count
        self._status = status
        self._last_time = last_time
        self._proxy_type = proxy_type

    @classmethod
    def createFromJson(cls, proxy_json):
        _dict = json.loads(proxy_json)
        return cls(proxy=_dict.get("proxy", ""),
                   city=_dict.get("city", ""),
                   country=_dict.get("country", ""),
                   anonymity=_dict.get("anonymity", ""),
                   check_count=_dict.get("check_count", 0),
                   status=_dict.get("status", True),
                   last_time=_dict.get("last_time", ""),
                   proxy_type=_dict.get("proxy_type", []))

    @property
    def proxy(self):
        """ 代理 ip:port """
        return self._proxy

    @property
    def check_count(self):
        """ 代理检测次数 """
        return self._check_count

    @property
    def city(self):
        return self._city

    @property
    def country(self):
        """ 国家 """
        return self._country

    @property
    def anonymity(self):
        """ 匿名 """
        return self._anonymity

    @property
    def status(self):
        """ 最后一次检测结果  True -> 可用; False -> 不可用"""
        return self._status

    @property
    def last_time(self):
        """ 最后一次检测时间 """
        return self._last_time

    @property
    def proxy_type(self):
        """ 代理类型 """
        return self._proxy_type

    @property
    def to_dict(self):
        """ 属性字典 """
        return {
            "proxy": self.proxy,
            "proxy_type": self.proxy_type,
            "city": self.city,
            "country": self.country,
            "anonymity": self.anonymity,
            "check_count": self.check_count,
            "status": self.status,
            "last_time": self.last_time
        }

    @property
    def to_json(self):
        """ 属性json格式 """
        return json.dumps(self.to_dict, ensure_ascii=False)

    @city.setter
    def city(self, value):
        self._city = value

    @country.setter
    def country(self, value):
        self._country = value

    @check_count.setter
    def check_count(self, value):
        self._check_count = value

    @status.setter
    def status(self, value):
        self._status = value

    @last_time.setter
    def last_time(self, value):
        self._last_time = value

    @proxy_type.setter
    def proxy_type(self, value):
        self._proxy_type = value
