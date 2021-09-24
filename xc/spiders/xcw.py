import scrapy
from openpyxl import load_workbook


class XcwSpider(scrapy.Spider):
    name = 'xcw'

    allowed_domains = ['ctrip.com']

    # url = 'https://gs.ctrip.com/html5/you/sight/huangshanscenicarea19/{}.html'

    def start_requests(self):
        workbook = load_workbook(filename='../4A5A汇总.xlsx')
        sheet = workbook.active
        names = sheet['C']  # 景点名称
        ids = sheet['G']  # 景点ID
        urls = sheet['F']  # 景点url
        for name, jid, url in zip(names[2:30], ids[2:30], urls[2:30]):
            add_params = {}
            add_params['J_name'] = name.value  # 景点名称
            add_params['J_id'] = jid.value  # 景点ID
            j_url = jid.value  # 景点url
            yield scrapy.Request(url=j_url, callback=self.parse_data, cb_kwargs=add_params)

    def parse_data(self, response, J_name, J_id):
        print(response)
        print('---' * 32)
