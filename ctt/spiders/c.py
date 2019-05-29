# -*- coding: utf-8 -*-
import json
import re
import time
import urllib.parse
import scrapy
from scrapy_splash import SplashRequest
from ctt.items import CttItem

lua = """
    function main(splash, args)
          splash.images_enabled = false
          assert(splash:go(args.url))
          assert(splash:wait(args.wait))
          return splash:html()
        end
"""



class CSpider(scrapy.Spider):
    name = 'c'
    # allowed_domains = ['ctoutiao.com']
    start_urls = ['http://www.ctoutiao.com/']
    base_url = "http://www.ctoutiao.com"

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(CSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        with open("/home/parrot/PycharmProjects/My_Crawl/ctoutiao/city_code.txt", "r") as f:
            for str_data in f.readlines():
                data = json.loads(str_data.strip('\n'))
                city_url = "http://www.ctoutiao.com/map/" + data["city_code"] + "/index.html?type=1&keywords=" + urllib.parse.quote("双创平台")
                yield scrapy.Request(city_url, callback=self.parse_page_num, meta={'city_url': city_url }, dont_filter=True)

    def parse_page_num(self,response):
        city_url = response.meta["city_url"]
        page_num = response.xpath("//div[@class='Mppagen']/em/text()")
        if page_num:
            ret = re.compile(r'\d+')
            number = re.findall(ret, page_num.extract_first().split('/')[-1])[0]
            if number:
                for i in range(1, int(number) + 1):
                    next_page = city_url + '&p=' + str(i)
                    print("======", next_page, "======")
                    yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = CttItem()

        city_name = response.xpath("//div[@class='Mpsearch']/div[@class='Mpcity']/span/text()").extract_first()
        item["city_name"] = city_name
        lis = response.xpath("//ul[@class='Mpctlist']/li")
        for li in lis:
            # item = {}
            item["link"] = self.base_url + li.xpath("./dl/dd/a/@href").extract_first()
            # item["name2"] = li.xpath("./dl/dd/a/h1/text()").extract_first()
            # yield SplashRequest(item["link"], callback=self.two_parse, endpoint='execute', args={'lua_source': lua, 'wait': 7})
            yield scrapy.Request(item["link"],callback=self.two_parse, meta={'item': item}, dont_filter=True)


    def two_parse(self,response):
        # from selenium import webdriver
        # broswer = webdriver.Chrome()
        # broswer.get(response.url)
        # print(broswer.page_source)
        item = response.meta['item']
        response.status_code = 'UTF-8'

        address_re = re.compile(r'"address":"(.*?)"')
        address = re.findall(address_re,response.text)
        address = address[0] if len(address) > 0 else "没有地址"
        item["address"] = address.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore')
        
        name_re = re.compile(r'"name":"(.*?)"')
        name = re.findall(name_re,response.text)
        name = name[0] if len(name) > 0 else ""
        item["name"] = name.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore')

        company_name_re = re.compile(r'"company_name":"(.*?)"')
        company_name = re.findall(company_name_re, response.text)
        company_name = company_name[0] if len(company_name) > 0 else ""
        item["company_name"] = company_name.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore')

        info_re = re.compile(r'"info":"(.*?)"')
        info = re.findall(info_re, response.text)
        info = info[0] if len(info) > 0 else ""
        item["info"] = info.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore') if info else "暂无简介"

        tel_re = re.compile(r'"phone":"(.*?)"')
        tels = re.findall(tel_re, response.text)
        tels = tels[0] if len(tels) > 0 else ""
        item["tel"] = tels if tels else "没有电话号码"

        lng_re = re.compile(r'"lng":"(.*?)"')
        lng = re.findall(lng_re, response.text)
        lng = lng[0] if len(lng) > 0 else "暂无坐标"
        item["lng"] = lng # lng.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore')

        lat_re = re.compile(r'"lat":"(.*?)"')
        lat = re.findall(lat_re, response.text)
        lat = lat[0] if len(lat) > 0 else "暂无坐标"
        item["lat"] = lat  # lng.encode('utf-8', 'ignore').decode('unicode_escape', 'ignore')

        id_re = re.compile('"nicename":"(.*?)"')
        id_res = re.findall(id_re, response.text)
        item["nicename_id"] = id_res[0] if len(id_res) > 0 else None
        if item["nicename_id"]:
            two_url = self.base_url + "/c/" + item["nicename_id"]
            item["parse_link"] = two_url
        # print(item)
        yield item
            # yield scrapy.Request(two_url,callback=self.there_parse, meta={'item': item}, dont_filter=True)

    # def there_parse(self,response):
    #     # print(response.text)
    #     item = response.meta['item']
    #     time.sleep(1)
    #     name = response.xpath("/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div/div[1]/h1/span/text()")
    #     item["name1"] = name.extract_first() if len(name) > 0 else ""
    #
    #     explain = response.xpath("//div[@class='uploadbox']/div[@class='jianjies']//text()")
    #     item["explain"] = ''.join(explain.extract()) if len(explain) > 0 else "没有简介"
    #
    #     Total = response.xpath("//div[@class='S_tcrigbon S_tcrigbon2']/div[@class='S_tcpfs S_tcpfs2']/ul[@class='S_nenuv']/li[1]/strong/text()")
    #     item["Total"] = Total.extract_first() if len(Total) > 0 else "总工位数未知"
    #
    #     S = response.xpath("//div[@class='S_tcrigbon S_tcrigbon2']/div[@class='S_tcpfs S_tcpfs2']/ul[@class='S_nenuv']/li[2]/strong/text()")
    #     item["S"] = S.extract_first() if len(S) > 0 else "总面积未知"
    #
    #     Site = response.xpath("//div[@class='S_tcrigbon S_tcrigbon2']/div[@class='S_tcpfs S_tcpfs2']/ul[@class='S_nenuv']/li[3]/strong/text()")
    #     item["Site"] = Site.extract_first() if len(Site) > 0 else "全国站点数未知"
    #
    #     Settled_rate = response.xpath("//div[@class='S_tcrigbon S_tcrigbon2']/div[@class='S_tcpfs S_tcpfs2']/ul[@class='S_nenuv']/li[4]/strong/text()")
    #     item["Settled_rate"] = Settled_rate.extract_first() if len(Settled_rate) > 0 else "入驻率未知"
    #
    #     Fraction = response.xpath("/html/body/div[4]/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/text()")
    #     item["Fraction"] = Fraction.extract_first() if len(Fraction) > 0 else "综合评分未知"
    #
    #     wz = response.xpath("//div[@class='S_tcrigle']/div[@class='S_tcrigle1 S_tcnewh']/div[@class='S_tcles']/div[1]/em/text()")
    #     item["wz"] = wz.extract_first() if len(wz) > 0 else "发表文章数未知"
    #
    #     rs = response.xpath("//div[@class='S_tcrigle']/div[@class='S_tcrigle1 S_tcnewh']/div[@class='S_tcles']/div[2]/em/text()")
    #     item["rs"] = rs.extract_first() if len(rs) > 0 else "关注人数未知"
    #
    #     fk = response.xpath("//div[@class='S_tcrigle']/div[@class='S_tcrigle1 S_tcnewh']/div[@class='S_tcles']/div[3]/em/text()")
    #     item["fk"] = fk.extract_first() if len(fk) > 0 else "最近没有访客"
    #
    #     g_q_f = response.xpath("//div[@class='Sxsbos']/h1/text()")
    #     item["g_q_f"] = g_q_f.extract_first() if len(g_q_f) > 0 else "没有附加区域或公司名"
    #
    #     address = response.xpath("//*[@id='J_branchTeam']/div[1]/div/ul/li[1]/text()")
    #     item["address"] = address.extract_first() if len(address) > 0 else "地址信息未知"
    #
    #     # s_y = response.xpath("//div[@class='Sxsbos']/ul/li[@class='Spgws']/text()")
    #     # item["s_y"] = s_y.extract_first() if len(s_y) > 0 else "仅剩工位未知"
    #     print(item)
    #     print()
    #     yield item






