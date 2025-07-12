import urllib.parse
import requests
import time

def valid_password(password):
    if password != "1234":
        time.sleep(10)
        return False
    return True

def query_eslite(keyword: str):
    """
    https://holmes.eslite.com/v1/search?q=+%E8%A1%8C%E5%8B%95%E9%9B%BB%E6%BA%90&page_size=20&page_no=1&final_price=0,&sort=desc&branch_id=0
    """
    encoded_keyword = urllib.parse.quote(keyword)
    response = requests.get(
        f"https://holmes.eslite.com/v1/search?q=+{encoded_keyword}&page_size=20&page_no=1&final_price=0,&sort=desc&branch_id=0"
    )
    data = [
        {
            "name": result["name"],
            "pricing": float(result["final_price"]), # "pricing": result["final_price"],
        }
        for result in response.json()["results"]
    ]
    return data


# 老師的 直接跟pchome要資料
def query_pchome(keyword: str):
    encoded_keyword = urllib.parse.quote(keyword)
    # print(response.get) # 在黑 pytest test_pricing_server.py -s
    response = requests.get(
        f"https://ecshweb.pchome.com.tw/search/v4.3/all/results?q={encoded_keyword}&page=1&pageCount=40"
    )
    '''
    url encode 行動電源
    https://ecshweb.pchome.com.tw/search/v4.3/all/results?q=%E8%A1%8C%E5%8B%95%E9%9B%BB%E6%BA%90&page=1&pageCount=40
    將這網址的內容存成pchome_battery.json
    '''
    data = [
        {
            "name": prod["Name"],
            "pricing": float(prod["Price"]), # "pricing": prod["Price"],
        }
        for prod in response.json()["Prods"]
    ]
    return data


if __name__ == "__main__":
    print(query_pchome("行動電源"))


# https://docs.python.org/3/library/unittest.mock.html
"""
看Quick Guide
強制將get指到我們自己的json檔案
from unittest.mock import MagicMock
thing = ProductionClass()
thing.method = MagicMock(return_value=3) # return_value=3 有時有用有時沒用
thing.method(3, 4, 5, key='value')

thing.method.assert_called_with(3, 4, 5, key='value')
"""

# 我的
# import urllib.parse
# import requests


# def query_pchome(keyword: str):
#     encoded_keyword = urllib.parse.quote(text)
#     response = requests.get(
#         f"https://ecshweb.pchome.com.tw/search/v4.3/all/results?q={encoded_keyword}&page=1&pageCount=40"
#     )
#     data = [
#         {
#             "name": prod["Name"],
#             "pricing": prod["Price"],
#         }
#         for prod in response.json()["Prods"]
#     ]
#     return data

# if __name__ == "__main__":
#     print(query_pchome("行動電源"))