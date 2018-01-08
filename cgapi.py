# -*- coding: utf-8 -*-

import requests
import bs4
from selenium import webdriver
import sys

class cgapi:

    @staticmethod
    def get_rate_from_coingecko_with_requests(coin_id, currency_id):
        return cgapi.get_rate_from_html(requests.get(cgapi.get_url_of_coingecho(coin_id, currency_id)).content)

    @staticmethod
    def get_rate_from_coingecko_with_selenium(coin_id, currency_id='btc'):
        browser = webdriver.Chrome()
        browser.get(cgapi.get_url_of_coingecho(coin_id, currency_id))
        html = browser.page_source
        browser.close()
        return cgapi.get_rate_from_html(html)

    @staticmethod
    def get_rate_from_coingecho_with_phantomjs(coin_id, currency_id):
        driver = webdriver.PhantomJS()
        driver.get(cgapi.get_url_of_coingecho(coin_id, currency_id))
        html = driver.page_source
        driver.quit()
        return cgapi.get_rate_from_html(html)

    @staticmethod
    def get_url_of_coingecho(coin_id, currency_id):
        return 'https://www.coingecko.com/ja/%E7%9B%B8%E5%A0%B4%E3%83%81%E3%83%A3%E3%83%BC%E3%83%88/' + coin_id + '/' + currency_id

    @staticmethod
    def get_rate_from_html(html):
        soup_obj = bs4.BeautifulSoup(html, "html.parser").find("div", class_="coin-value").span
        ret_rate = float(cgapi.remove_currency_mark(soup_obj.text.strip()))
        return ret_rate

    @staticmethod
    def remove_currency_mark(str_val):
        return str_val.replace('¥', '').replace(',', '').replace('$', '').replace('฿', '')

args = sys.argv
coin_id = args[1]
currency_id = args[2]
method_type = 'phantomjs'
rate_result = ''

if len(args) > 3 and args[3] in ['phantomjs', 'selenium', 'requests']:
    method_type = args[3]

if method_type == 'phantomjs':
    rate_result = cgapi.get_rate_from_coingecho_with_phantomjs(coin_id, currency_id)
elif method_type == 'selenium':
    rate_result = cgapi.get_rate_from_coingecko_with_selenium(coin_id, currency_id)
elif method_type == 'requests':
    rate_result = cgapi.get_rate_from_coingecko_with_requests(coin_id, currency_id)

print(rate_result)
