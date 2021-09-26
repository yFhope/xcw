import json

import scrapy
from jsonpath import jsonpath
from openpyxl import load_workbook


class XcwSpider(scrapy.Spider):
    name = 'xcw'

    allowed_domains = ['ctrip.com']

    comment_params = {"arg": {"resourceId": 26184, "resourceType": 11, "pageIndex": 1, "pageSize": 10, "sortType": 3,
                              "commentTagId": -1, "collapseType": 1, "channelType": 7, "videoImageSize": "700_392",
                              "starType": 0},
                      "head": {"cid": "09031133417600395476", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                               "syscode": "09", "auth": None, "extension": [{"name": "protocal", "value": "https"}]},
                      "contentType": "json"}

    source_params = {"arg": {"resourceId": 5078351, "resourceType": 11},
                     "head": {"cid": "09031173417826624428", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                              "syscode": "09", "auth": None, "extension": [{"name": "protocal", "value": "https"}]},
                     "contentType": "json"}

    comment_api = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"
    source_api = "https://m.ctrip.com/restapi/soa2/13444/json/getPoiCommentInfoWithHotTag"

    # url = 'https://gs.ctrip.com/html5/you/sight/huangshanscenicarea19/{}.html'
    num = 0

    def start_requests(self):
        workbook = load_workbook(filename=r'C:\Users\windows\Desktop\xcw\45A.xlsx')
        sheet = workbook.active
        names = sheet['C']  # 景点名称
        ids = sheet['G']  # 景点ID
        urls = sheet['F']  # 景点url
        for name, jid, url in zip(names[1:], ids[1:], urls[1:]):
            add_params = {}
            add_params['J_name'] = name.value  # 景点名称
            add_params['J_id'] = jid.value  # 景点ID
            j_url = url.value  # 景点url
            self.num += 1
            print(f'请求数：》》》》{self.num}')
            yield scrapy.Request(url=j_url, callback=self.parse_index_data, cb_kwargs=add_params)

    def parse_index_data(self, response, J_name, J_id):
        j_kargs = {}
        j_kargs['J_name'] = J_name
        j_kargs['J_id'] = J_id
        j_kargs['level'] = response.xpath('//span[@class="titleTag"]//text()').extract_first()  # 等级 4A 5A
        j_kargs['overallScore'] = response.xpath('//span[@class="commentNum"]/text()').extract_first()  # 总体评分
        j_kargs['label'] = "".join(response.xpath('//div[@class="shortFeatures"]//text()').extract())  # 景区类型  标签

        self.source_params['arg']['resourceId'] = J_id
        yield scrapy.Request(self.source_api, callback=self.get_comm_api, method='POST',
                             body=json.dumps(self.source_params), cb_kwargs=j_kargs)

    def get_comm_api(self, response, J_name, J_id, level, overallScore, label):
        json_data = json.loads(response.text)
        totalCount = jsonpath(json_data, '$..poiInfo.commentCount')[0]  # 评论数量
        js, qw, xjb = jsonpath(json_data, '$..scores..score')  # 分维度评分
        print("ID ", J_id)
        print("名称 ", J_name)
        print("等级 ", level)
        print("总评分 ", overallScore)
        print("标签 ", label)
        print("评论数 ", totalCount)
        print(js, qw, xjb)
        print("===" * 45)

        item = {}
        item['J_id'] = J_id
        item['J_name'] = J_name
        item['level'] = level
        item['overallScore'] = overallScore
        item['label'] = label
        item['totalCount'] = totalCount
        item['js'] = js
        item['qw'] = qw
        item['xjb'] = xjb
        yield item
