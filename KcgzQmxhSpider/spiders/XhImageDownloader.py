# -*- coding: utf-8 -*-

import scrapy
import json
import re
import random

import requests


class XhImageDownloader(scrapy.Spider):
    name = "XhImage"
    start_urls = [
        "http://kechenggezi.com/campus_stars?page=1&cur_time=1455265064747"]
    cookies = {
        'Hm_lpvt_31589adaafcdee0269f5b28ec8ac344c': '1455265065',
        'Hm_lvt_31589adaafcdee0269f5b28ec8ac344c': '1455253763,1455254740,1455256199,1455264343',
        '_zg': r'%7B%22uuid%22%3A%20%221500db06c20404-005d4025a-68391f6f-3d10d-1500db06c2194f%22%2C%22sid%22%3A%201455262803.041%2C%22updated%22%3A%201455265064.764%2C%22info%22%3A%201455253762809%2C%22cuid%22%3A%20%22fbb65b1f-7c34-43d9-860a-ef8ba61fbd37%22%7D',
        'from_gezi': 'true',
        'token': 'XXXXXXXXXXXXXXXXXX',
        '_kecheng_session': 'BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTY4MDk1YzUyZGM4MzljMTI2NDA3ZTIxYmEwZTFiZTRhBjsAVEkiDHVzZXJfaWQGOwBGaQPNEZ4%3D--3f25c9aaf3b0fe73009d80f4dd2c628541c0bd7c',
        'responseTimeline': '294'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone;CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46(KHTML, like Gecko)Mobile/13D15 ClassBox/7.3 ClassBox/7.3 ClassBox/7.3',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def parse(self, response):
        yield scrapy.Request(
            url='http://kechenggezi.com/campus_stars?page=1&cur_time=145526506'+str(int(random.random() * 10000) % 10000).ljust(4,'0'),
            cookies=self.cookies,
            headers=self.headers,
            callback=self.parse_all
        )

    def parse_all(self, response):
        j = json.loads(response.body)
        total_pages = j['total_pages']
        for page in range(1, int(total_pages) + 1):
            yield scrapy.Request(
                url='http://kechenggezi.com/campus_stars?page={0}&cur_time=145526506{1}'.format(
                    page,str(int(random.random() * 10000) % 10000).ljust(4,'0')),
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse_page
            )

    def parse_page(self, response):
        j = json.loads(response.body)
        orig = re.compile(r'(.+)!300x300')
        for campus_star in j["campus_stars"]:
            avatar_url_300_300 = campus_star["avatar_url"]
            print avatar_url_300_300
            avatar_url = orig.search(avatar_url_300_300).group(1)
            try:
                r = requests.get(avatar_url)
                # change images to your own dir to save
                with open('./images/' + avatar_url.split('/')[-1], 'wb') as p:
                    p.write(r.content)
            except Exception as inst:
                print(type(inst), inst.args)
