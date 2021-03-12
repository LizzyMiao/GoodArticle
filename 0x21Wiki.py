#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import collections
import time

import requests
from bs4 import BeautifulSoup
from bs4 import element

def extract_book_value_per_share_from_macrotrends(url):
    response = requests.get(
        url=url,
        verify=False
    )
    history_dict = {}
    content = response.text
    Soup = BeautifulSoup(content, 'lxml')
    for child in Soup.body.children:
        if type(child) == element.Tag and child.has_attr('class') and child.attrs['class'][0] == 'main_content_container'\
                and child.attrs['class'][1] == 'container-fluid':
            for grandChild in child.children:
                if type(grandChild) == element.Tag and grandChild.has_attr('id') and grandChild.attrs['id'] == 'main_content':
                    for ggrandChild in grandChild.children:
                        if type(ggrandChild) == element.Tag and ggrandChild.has_attr('id') and ggrandChild.attrs['id'] == 'jqxgrid':
                            for gggrandChild in ggrandChild.children:
                                if type(gggrandChild) == element.Tag:
                                    if len(gggrandChild.contents) > 4:
                                        for ggggrandChild in gggrandChild.contents[3].contents:
                                            if type(ggggrandChild) == element.Tag and ggggrandChild.has_attr('class') and \
                                                    ggggrandChild.attrs['class'][0] == 'historical_data_table' and \
                                                    ggggrandChild.attrs['class'][1] == 'table':

                                                for table_element in ggggrandChild.contents[3].contents:
                                                    if type(table_element) == element.Tag:
                                                        tr_content = table_element.contents
                                                        if type(tr_content) == list \
                                                                and type(tr_content[1]) == element.Tag \
                                                                and type(tr_content[3]) == element.Tag:
                                                            year_quarter = tr_content[1].contents[0].replace("-", "")
                                                            financial_number = tr_content[3].contents[0]
                                                            history_dict[year_quarter] = financial_number
                                        break

                            break
                    break
            break
    return history_dict


def extract_financial_data_from_macrotrends(url, financial_element):
    response = requests.get(
        url=url,
        verify=False
    )

    web_financial_index = [financial_element]
    history_array = []
    content = response.text
    Soup = BeautifulSoup(content, 'lxml')
    for child in Soup.body.children:
        if type(child) == element.Tag and child.has_attr('id') and child.attrs['id'] == 'main_content_container':
            for grandChild in child.children:
                if type(grandChild) == element.Tag and grandChild.has_attr('class') and grandChild.attrs['class'][0] == 'sub_main_content_container':
                    for ggrandChild in grandChild.children:
                        if type(ggrandChild) == element.Tag and ggrandChild.has_attr('id') and ggrandChild.attrs['id'] == 'main_content':
                            for gggrandChild in ggrandChild.children:
                                if type(gggrandChild) == element.Tag and gggrandChild.has_attr('id') and gggrandChild.attrs['id'] == 'style-1':
                                    if len(gggrandChild.contents) > 4:
                                        for ggggrandChild in gggrandChild.contents[3].contents:
                                            if type(ggggrandChild) == element.Tag and ggggrandChild.has_attr('class') and \
                                                    ggggrandChild.attrs['class'][0] == 'historical_data_table' and \
                                                    ggggrandChild.attrs['class'][1] == 'table':

                                                history_dict = dict()
                                                for table_element in ggggrandChild.contents[3].contents:
                                                    if type(table_element) == element.Tag:
                                                        tr_content = table_element.contents
                                                        if type(tr_content) == list \
                                                                and type(tr_content[1]) == element.Tag \
                                                                and type(tr_content[3]) == element.Tag:
                                                            year_quarter = tr_content[1].contents[0].replace("-", "")
                                                            financial_number = 0
                                                            if len(tr_content[3].contents) > 0:
                                                                financial_number = tr_content[3].contents[0]
                                                            history_dict[year_quarter] = financial_number

                                                history_array.append(history_dict)
                                        break
                                    elif len(gggrandChild.contents) == 3:
                                        for ggggrandChild in gggrandChild.contents[1].contents:
                                            if type(ggggrandChild) == element.Tag:
                                                if len(ggggrandChild.contents) > 0 and len(ggggrandChild.contents[1].contents) > 3 and ggggrandChild.name == 'thead':
                                                    web_financial_index.clear()
                                                    for index_financial_thead_element in ggggrandChild.contents[1].contents:
                                                        if type(index_financial_thead_element) == element.Tag and len(index_financial_thead_element.contents) > 0 and index_financial_thead_element.contents[0] != 'Date' and not index_financial_thead_element.contents[0]:
                                                            web_financial_index.append(index_financial_thead_element.contents[0])
                                                            history_array.append(dict())

                                                if ggggrandChild.name == 'tbody' and len(web_financial_index) > 0:
                                                    index_element_size = len(web_financial_index)

                                                    for table_element in ggggrandChild.contents:
                                                        i = 0
                                                        year_quater = ''
                                                        for td_content in table_element.contents:
                                                            if type(td_content) == element.Tag:

                                                                if len(table_element.contents[i*2 + 1]) > 0:
                                                                    value = table_element.contents[i*2 + 1].contents[0]
                                                                    if i == 0:
                                                                        year_quater = value.replace("-", "")
                                                                    elif i > 0:
                                                                        current_dict = history_array[i - 1]
                                                                        current_dict[year_quater] = value
                                                                elif i > 0:
                                                                    current_dict = history_array[i - 1]
                                                                    current_dict[year_quater] = 0

                                                                i = i + 1
                                                                assert i <= (index_element_size + 1)

                            break
                    break
            break

    sorted_history_array = []
    index_size = len(web_financial_index)
    i = 0
    for history_element in history_array:
        sorted_ele = collections.OrderedDict(sorted(history_element.items()))
        sorted_history_array.append(sorted_ele)
        i = i + 1

    return (sorted_history_array, web_financial_index)


def get_all_financial_data():
    df = pd.read_csv('bankrupted.csv', index_col=False, sep='\t', header=None)
    #df = pd.read_csv('bankrupted.csv', index_col=False, sep='\t', header=None)
    company = df.loc[:, [0, 1]]

    columns = [ 'revenue',
                'total-assets',
                'gross-profit',
                'total-current-liabilities',
                'total-liabilities',
                'net-income-loss',
                'total-depreciation-amortization-cash-flow',
                'inventory',
                'total-current-assets',
                'total-share-holder-equity',
                'receivables-total',
                'cost-goods-sold',
                'net-property-plant-equipment',
                'operating-income',
                'operating-expenses',
                'total-current-assets',
                'total-current-liabilities',
                'cash-on-hand',
                'total-long-term-liabilities',
                'gross-profit',
                'ebitda',
                'total-current-liabilities',
                'ebit']


    find_book_value_per_share = False

    basic_url = 'https://www.macrotrends.net/stocks/charts/{0}/{1}/'
    for row in company.values:
        company_code = row[0]
        company_part_name = row[1].split(' ')[0]

        data = {}
        time_stamp_list = []
        year_based_data = {}
        year_based_time_list = []
        for column in columns:
            url = basic_url + column
            ful_url = url.format(company_code, company_part_name)
            print("requesting: " + ful_url)
            # 定义请求url
            (history_array, web_financial_index) = extract_financial_data_from_macrotrends(ful_url, column)

            assert len(history_array) == len(web_financial_index)

            for i in range(len(web_financial_index)):
                element_web_financial_data = history_array[i]
                column_time_stamps = list(history_array[i].keys())

                if len(column_time_stamps[0]) == 8:
                    data[web_financial_index[i]] = element_web_financial_data
                    time_stamp_list = time_stamp_list + column_time_stamps
                elif len(column_time_stamps[0]) == 4:
                    year_based_data[web_financial_index[i]] = element_web_financial_data
                    year_based_time_list = year_based_time_list + column_time_stamps

            unduplicate_time_stamp_list = list(set(time_stamp_list)).sort()
            unduplicate_year_based_time_list = list(set(year_based_time_list)).sort()
            time.sleep(80)

        if find_book_value_per_share == True:
            view_source = "view-source:"
            book_value_per_share = "financial-ratios"
            url = view_source + basic_url + book_value_per_share
            book_value_per_share_dict = extract_book_value_per_share_from_macrotrends(
                url.format(company_code, company_part_name))
            data["book-value-per-share"] = book_value_per_share_dict
            column_time_stamps = list(book_value_per_share_dict.keys())
            time_stamp_list = time_stamp_list + column_time_stamps

        if len(data) > 0:
            result_dataframe = pd.DataFrame(data, index=unduplicate_time_stamp_list)
            result_dataframe.to_csv(
                'C:\\Temp\\ProjectFile\\hackthon\\financial_infos\\{0}_basic_financial.csv'.format(row[0]))

        if len(year_based_data) > 0:
            result_dataframe = pd.DataFrame(year_based_data, index=unduplicate_year_based_time_list)
            result_dataframe.to_csv(
                'C:\\Temp\\ProjectFile\\hackthon\\financial_infos\\{0}_basic_financial_year.csv'.format(row[0]))


if __name__ == '__main__':
    get_all_financial_data()
