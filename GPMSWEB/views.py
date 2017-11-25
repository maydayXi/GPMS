from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime                   # 時間
from GPMSWEB.main import main                   # 自建主程式類別
from GPMSWEB.DBService import DBService         # 自建資料庫類別
from GPMSWEB.TableService import TableService   # 自建資料表類別
from GPMSWEB.dataAnaly import dataAnaly         # 資料分析類別
import psycopg2
from firebase import firebase

# Create your views here.

# 初始所有類別物件   全域
db = DBService()                            # 資料庫物件
analy = dataAnaly()                         # 資料分析物件
table = TableService()                      # 表格資料物件

# 找出有問題的站點
def Main(requests):
    x = main()
    x.getInitData()
    x.getAirValue()
    x.dataSave()
    table_name_lst = table.lst_getAllAirInfoTableName()
    error_site = x.analy()

    error = []
    for item in error_site:
        error_air_data = db.m_readAirDataByNote(table_name_lst[-1], item)
        error_position = db.m_readSitePositionByNote(item)
        error.append([error_air_data[0],item,error_air_data[1],                 # stId, PM2.5
                       error_air_data[2],error_air_data[3],                     # PM10, Temperature
                       error_air_data[4],error_position[0],error_position[1]])  # Humidity, stLatitude, stLongitude

    db.createErrorData(table_name_lst[-1][8:],error)

    return render(requests, "test.html", {"result":error})

# 首頁
def index(requests):
    error_table_name_lst = table.lst_getAllErrorTableName()
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

    # data = HttpResponse(json.dumps(data),content_type="application/json")

    return render(requests, "data.html", locals())

# 取得有問題的測站，傳送至 wrongList.html 頁面
def wronglist(requests):
    if(len(requests.GET) == 0):
        url = ""
        errorSiteVal = ""
        errorTimeVal = ""
    else:
        print(requests.GET)
        url = requests.GET['url']
        errorSiteVal = requests.GET['errorSiteVal']
        errorTimeVal = requests.GET['errorTimeVal']

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

    return render(requests, 'test.html', locals())
