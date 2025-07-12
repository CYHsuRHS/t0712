from shopping import query_pchome, query_eslite, valid_password
import json
from unittest import mock
import pytest
# 加入FastAPI
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_pricing_sort_by_desc():
    with mock.patch(
        "main.shopping.query_eslite",
        return_value=[
            {"name": "eslite1", "pricing": 100.1},
            {"name": "eslite2", "pricing": 90.1}
            ]
        ) as query_eslite:
        with mock.patch(
            "main.shopping.query_pchome",
            return_value=[
                {"name": "pchome1", "pricing": 80.1},
                {"name": "pchome2", "pricing": 110.1}
                ]
        ) as query_pchome:
            response = client.get("/pricing?keyword=行動電源&sort_by=pricing")
    
    data = response.json()
    
    for pre, curr in zip(data, data[1:]):
        assert pre["pricing"] >= curr["pricing"]


def test_pricing_sort_by_asc():
    "1,2,3"
    with mock.patch(
        "main.shopping.query_eslite",
        return_value=[
            {"name": "eslite1", "pricing": 100.1},
            {"name": "eslite2", "pricing": 90.1}
            ]
        ) as query_eslite:
        with mock.patch(
            "main.shopping.query_pchome",
            return_value=[
                # {"name": "pchome1", "pricing": 100.1},
                # {"name": "pchome2", "pricing": 101.1}
                {"name": "pchome1", "pricing": 80.1},
                {"name": "pchome2", "pricing": 110.1}
                ]
        ) as query_pchome:
            response = client.get("/pricing?keyword=行動電源&sort_by=-pricing")
    data = response.json()
    # print("----------")
    # print(data)
    for pre, curr in zip(data, data[1:]): # zip會把兩個資料1:1的接起來
        # print(pre, curr)
        assert pre["pricing"] <= curr["pricing"]
        # pytest test_pricing_server.py -s # 把print結果顯示加-s

def test_valid_password():
    with mock.patch(
        "shopping.time.sleep",
        side_effect = [None]
    ) as sleep:
        assert valid_password("1") is False
    sleep.assert_called_once_with(10)

def test_pricing_will_return_200_with_keyword():
    with mock.patch(
        "main.shopping.query_eslite",
        return_value=[{"name": "eslite", "pricing": 100.1}]
        ) as query_eslite:
        with mock.patch(
            "main.shopping.query_pchome",
            return_value=[{"name": "pchome", "pricing": 100.1}]
        ) as query_pchome:
            response = client.get("/pricing?keyword=行動電源")

    query_eslite.assert_called_once_with("行動電源")
    query_pchome.assert_called_once_with("行動電源")
    assert response.status_code == 200
    assert len(response.json()) > 0
    data = response.json()[0]
    assert "name" in data
    assert "pricing" in data

    assert isinstance(data["name"], str)
    assert isinstance(data["pricing"], float)

    assert data["name"] == "pchome"
    data = response.json()[1]
    assert data["name"] == "eslite"

# 3
# def test_pricing_will_return_200_with_keyword():
#     response = client.get("/pricing?keyword=行動電源")
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#     data = response.json()[0]
#     assert "name" in data
#     assert "pricing" in data

#     assert isinstance(data["name"], str)
#     assert isinstance(data["pricing"], float)
# 跑pytest test_pricing_server.py
# 若跑不出 assert 404 == 200 要執行 set PYTHONPATH=. 設定環境變數
# https://fastapi.tiangolo.com/deployment/manually/#install-the-server-program
# 將伺服器跑起來
# uvicorn main:app --host 0.0.0.0 --port 8000
# CTRL+C 離開伺服器
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload # 重跑
# http://localhost:8000/docs 看文件

@pytest.fixture
def pchome_battery() -> list:
    with open("./pchome_battery.json", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data


def test_query_pchome_will_return_list_of_pricing_and_name(pchome_battery):
    response = mock.Mock()
    response.json.return_value = pchome_battery

    with mock.patch("shopping.requests.get", side_effect=[response]) as get:
        result = query_pchome("行動電源")

    assert len(result) > 0
    assert "pricing" in result[0]
    assert isinstance(result[0]["pricing"], float)

    assert "name" in result[0]
    assert isinstance(result[0]["name"], str)

    assert result[0]["name"] == "超強行動電源"

@pytest.fixture
def eslite_battery() -> list:
    with open("./eslite_battery.json", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

def test_query_eslite_will_return_list_of_pricing_and_name(eslite_battery):
    response = mock.Mock()
    response.json.return_value = eslite_battery

    with mock.patch("shopping.requests.get", side_effect=[response]) as get:
        result = query_eslite("行動電源")

    assert len(result) > 0
    assert "pricing" in result[0]
    assert isinstance(result[0]["pricing"], float)

    assert "name" in result[0]
    assert isinstance(result[0]["name"], str)

    assert result[0]["name"] == "大方塊行動電源" # "name": "KINYO大方塊行動電源/ 藍/ KPB-2303BU", 改為 "name": "大方塊行動電源",


# 2
# def test_json():
#     import json

#     with open("./pchome_battery.json", encoding="utf-8") as f:
#         data = json.loads(f.read())
    
#     assert data["Prods"][0]["Name"] == "超強行動電源"

# def test_query_pchome_will_return_list_of_pricing_and_name():
#     with open("./pchome_battery.json", encoding="utf-8") as f:
#         data = json.loads(f.read())

#     def mock_get(url, *args, **kwargs):
#         response = mock.Mock()
#         response.json.return_value = data
#         return response

#     with mock.patch("shopping.requests.get") as get:
#         get.side_effect = mock_get
#         result = query_pchome("行動電源")

#     assert len(result) > 0
#     assert "pricing" in result[0]
#     assert isinstance(result[0]["pricing"], float)

#     assert "name" in result[0]
#     assert isinstance(result[0]["name"], str)
#     # 將pchome_battery.json檔案中的 "Name": "ADATA 威剛 C100 大容量10000mAh行動電源 可上飛機 蘋果/安卓通用",  改為  "Name": "超強行動電源",
#     assert result[0]["name"] == "超強行動電源" # 確認是讀我們自己的pchome_battery.json檔案,不去讀pchome網站

# 1
# def test_query_pchome_will_return_list_of_pricing_and_name():
#     result = query_pchome("行動電源")

#     assert len(result) > 0
#     assert "pricing" in result[0]
#     assert isinstance(result[0]["pricing"], float)

#     assert "name" in result[0]
#     assert isinstance(result[0]["name"], str)

#     assert result[0]["name"] == "超強行動電源"