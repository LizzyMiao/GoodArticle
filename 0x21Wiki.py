#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import time
import requests
from bs4 import BeautifulSoup
from bs4 import element

# 循环构建请求参数并且发送请求
for page_start in range(0, 1):
    # 定义请求url
    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    response = requests.get(
        url=url,
        verify=False
    )
    # main attributes
    company_name = ""
    company_type = ""
    traded_as = ""
    isin = ""
    industry = ""
    founded = ""
    founders = ""
    headquarters = ""
    products = ""
    services = ""
    revenue = 0.0
    operating_income = 0.0
    net_income = 0.0
    total_assets = 0.0
    total_equity = 0.0
    number_of_employee = 0


    # 方式一:直接转换json方法
    # results = response.json()
    # 方式二: 手动转换
    # 获取字节串
    content = response.text
    Soup = BeautifulSoup(content, 'lxml')
    body_content = Soup.body.find_all(id='content')
    for child in Soup.body.children:
        if type(child) == element.Tag and child.attrs['id'] == 'content':
            for grandChild in child.children:
                if type(grandChild) == element.Tag and grandChild.has_attr('id') and grandChild.attrs['id'] == 'bodyContent':
                    for ggrandChild in grandChild.children:
                        if type(ggrandChild) == element.Tag and ggrandChild.has_attr('id') and ggrandChild.attrs['id'] == 'mw-content-text':
                            for gggrandChild in ggrandChild.children:
                                if type(gggrandChild) == element.Tag and gggrandChild.has_attr('class') and gggrandChild.attrs['class'][0] == 'mw-parser-output':
                                    for ggggrandChild in gggrandChild.children:
                                        if type(ggggrandChild) == element.Tag and ggggrandChild.has_attr('class') and ggggrandChild.attrs['class'][0] == 'infobox' and ggggrandChild.attrs['class'][1] == 'vcard':
                                            company_name = ggggrandChild.caption.contents[0]
                                            for table_element in ggggrandChild.contents[1].contents:
                                                tr_content = table_element.contents[0]
                                                if type(tr_content) == element.Tag and type(ggggrandChild.contents[1].contents[2].contents[0].contents) == list:
                                                    separator = ','
                                                    th_value = separator.join(tr_content.contents)
                                                    if tr_content.has_attr('class') and tr_content.attrs['class'][0] == 'category':
                                                        print(tr_content)

                                    break
                            break
                    break
            break

    all_a = Soup.find("body").find('div')
    for a in all_a:
        title = a.get_text()
        print('------开始保存：', title)
        # 转换成字符串
    string = content.decode('utf-8')
    # 把字符串转成python数据类型
    results = json.loads(string)
    time.sleep(100)
    # 解析结果
    for movie in results["subjects"]:
        print(movie["title"], movie["rate"])
