from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime                   # 時間
from GPMSWEB.DBService import DBService         # 自建資料庫類別
from GPMSWEB.TableService import TableService   # 自建資料表類別
from GPMSWEB.dataAnaly import dataAnaly         # 資料分析類別
from firebase import firebase

# Create your views here.

# 初始所有類別物件   全域
db = DBService()                            # 資料庫物件
analy = dataAnaly()                         # 資料分析物件
table = TableService()                      # 表格資料物件

def index(requests):
    error_table_name_lst = table.lst_getAllErrorTableName()
    print(error_table_name_lst[-1])
    error = db.readErrorData(error_table_name_lst[-1])
    date = error_table_name_lst[-1][10:20].replace("_","-")
    time = error_table_name_lst[-1][-5:].replace("_",":")

    return render(requests, "index.html", locals())

# 取得所有測站資料 傳送至 data.html 頁面
def data(requests):
    if(len(requests.GET) == 0):
        row = 0
    else:
        row = int(requests.GET['selectedIndex'])

    table_name_lst = table.lst_getAllAirInfoTableName()
    temp = db.lst_readSiteData()        # 暫存測站資料
    site_lst = []                       # 測站串列
    air_data_lst = []                   # 空氣資料串列
    data = {}                           # 過去空氣資料字典

    analy.getAreaId(table_name_lst[-1][8:])             # 取得鄰近測站資料  ID
    area = analy.lst_getAreaSite(row)                   # 取得鄰近站點資料名稱

    air_data = db.lst_readAirData(table_name_lst[-1])
    for item in air_data:
        site_lst.append([item[1],item[0]])                          # (id,stNote)
        air_data_lst.append([item[2], item[3],              # (pm2.5, pm10,
                            item[4], item[5]])              # 溫度, 濕度)

    data[site_lst[row][1]] = {"12":[],"6":[],"1":[],"area":[]}
    time_lst,pm25_lst = table.getXYAxis(table_name_lst,site_lst[row][0],interval=60)
    data[site_lst[row][1]]["12"] = pm25_lst
    time_lst,pm25_lst = table.getXYAxis(table_name_lst,site_lst[row][0],interval=30)
    data[site_lst[row][1]]["6"] = pm25_lst
    time_lst,pm25_lst = table.getXYAxis(table_name_lst,site_lst[row][0],interval=5)
    data[site_lst[row][1]]["1"] = pm25_lst
    data[site_lst[row][1]]["area"] = area

    return render(requests, "data.html", locals())

# 取得有問題的測站，傳送至 wrongList.html 頁面
def wronglist(requests):
    if(len(requests.GET) == 0):
        url = ""
        errorSiteVal = ""
        errorTimeVal = ""
        pm25_val = ""
        pm10_val = ""
        temperature_val = ""
        humidity_val = ""
    else:                                                       # 記錄 POST 過來的訊息
        errorSiteVal = requests.GET['errorSiteVal']
        errorTimeVal = requests.GET['errorTimeVal']
        pm25_val = requests.GET['PM25Val']
        pm10_val = requests.GET['PM10Val']
        temperature_val = requests.GET['TemperatureVal']
        humidity_val = requests.GET['HumidityVal']

    json_url = 'https://ch13-ccc60.firebaseio.com/'
    map_json = firebase.FirebaseApplication(json_url,None)
    error_json = map_json.get(json_url, None)                   # 取得即時的異常測站

    error_labels = []                                           # 異常測站的名稱串列
    if error_json != None:
        for item in error_json:
            error_labels.append(item['stNote'])


    return render(requests, "wrongList.html", locals())

# Json 資料網址
def json(requests):
    json_url = 'https://ch13-ccc60.firebaseio.com/'
    map_json = firebase.FirebaseApplication(json_url,None)
    error_json = map_json.get(json_url, None)

    return JsonResponse({"data":error_json})

def map(requests):
    json_url = 'https://ch13-ccc60.firebaseio.com/'
    map_json = firebase.FirebaseApplication(json_url,None)
    error_json = map_json.get(json_url, None)
    print(error_json)

    error_labels = []
    for item in error_json:
        error_labels.append(item['stNote'])
    print(error_labels)

    return render(requests, 'test.html', locals())

def historyData(requests):
    dateStr = datetime.now().strftime('%Y-%m-%d')
    history_json_url = 'https://errorsite-2017.firebaseio.com/{}/'.format(dateStr)
    error_site_obj = firebase.FirebaseApplication(history_json_url, None)           # 取得累計三次的測站資料

    if error_site_obj is not None:
        error_site_data = error_site_obj.get(history_json_url, None)
        print("errorSiteData = >", error_site_data)

    return render(requests, "history.html", locals())
