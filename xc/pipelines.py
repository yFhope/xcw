# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql,logging
from itemadapter import ItemAdapter


class XcPipeline:
    def __init__(self):
        db = {
            'host': 'node4-devsvr.realsvr.cs-xc-idc1-area1.singhand.com',
            'port': 3306,
            'user': 'cralwerdata',
            'password': r'cralwerdatastoreParch2016.',
            'database': 'CrawlerDBStore'
        }
        self.conn = pymysql.connect(**db)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'INSERT INTO scenic_info_gat(景区ID, 景区名称, 景区等级, 总体评分, 景区标签, 评论量, 景色, 趣味, 性价比) ' \
              'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        try:
            self.cur.execute(sql, [item['J_id'], item['J_name'], item['level'], item['overallScore'], item['label'],
                                   item['totalCount'], item['js'], item['qw'], item['xjb']])
            self.conn.commit()
        except Exception as e:
            logging.error(f'数据存储异常，原因：{e}')

        return item

    def close_spider(self, spider):
        pass
