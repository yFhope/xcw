# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import logging
import random
import time

import requests
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class XcSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class XcDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomProxy(object):
    def get_proxies(self):
        """
        代理
        :return:代理地址>dict
        """
        try:
            proxies_url = 'http://node2-calcsvr.realsvr.cs-xc-idc2-area1.singhand.com:9099/domestic/applyZM'
            proxies_response = requests.post(url=proxies_url, timeout=(5, 5))
            if proxies_response.status_code == 200:
                ip = proxies_response.json()['data']['ip']
                port = proxies_response.json()['data']['port']
                ip_port = str(ip) + ':' + str(port)
                logging.info(f'agent used：{ip_port}')
                proxies = {'http': ip_port, 'https': ip_port}
                return proxies
            raise Exception('proxy error~')
        except Exception as e:
            logging.error(f'代理调度失败,10s后重试，原因:{e}')
            time.sleep(10)
            return self.get_proxies()

    def process_request(self, request, spider):
        request.meta['proxy'] = "http://" + self.get_proxies()['http']
        # request.meta['proxy'] = "http://" + "117.34.192.57:4230"

        # proxy = random.choice(PROXIES)

        # if proxy['user_passwd'] is None:
        # 没有代理账户验证的代理使用方式
        # request.meta['proxy'] = "http://" + proxy['ip_port']
        # else:
        #     # 对账户密码进行base64编码转换
        #     base64_userpasswd = base64.b64encode(proxy['user_passwd'])
        #     # 对应到代理服务器的信令格式里
        #     request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
        #     request.meta['proxy'] = "http://" + proxy['ip_port']
