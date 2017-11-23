# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 17:06:34 2017

@author: user
"""
#==============================import package==============================#

#from excelService import Service               # excel class
from GPMSWEB.DBService import DBService         # 資料庫 class
from GPMSWEB.Helper import Helper               # 資料爬蟲 class
from GPMSWEB.dataAnaly import dataAnaly         # 資料分析 class
import time                            # html package , time package
from urllib.request import urlopen, Request
import json

#=============================Main class==================================#
class main:

    def __init__(self):                     # 初始化所有變數
        self.db = DBService()               # Database instance
        self.ana = dataAnaly()              # DataAnaly instance
        self.data = Helper()                # Url data fetch instance
        self.sensor_lst = ['pm2.5','pm10','temperature','humidity']
        self.all_id_lst = []                # 所有測站 ID list
        self.pm25_lst = []                  # PM2.5 lsit
        self.pm10_lst = []                  # PM10 list
        self.t_lst = []                     # Temperatuer lsit
        self.h_lst = []                     # Humidity list
        self.web_error = []
        self.id_lst = []
        self.dict_pm25 = {}
        self.dict_pm10 = {}

    # 2017-11-23 edit by Mayday
    # <summary> 初始有效 ID 與爬蟲網址 </summary>
    def getInitData(self):
        print("strftime")
        self.timeStr = time.strftime('%Y_%m_%d_%H_%M')  # GET current time
        print("db.lst_read")
        site_info_lst = self.db.lst_readSiteData()      # Get all site information
        print("getInitdata_for")
        for item in site_info_lst:                      # Input all_id_lst
            self.all_id_lst.append(item[0])

        print("get useful data list")
        # Get useful data list
        # self.id_lst,self.url_lst = self.data.urlHelper(self.all_id_lst,self.sensor_lst)

        return self.timeStr

    # 2017-11-23 edit by Mayday
    # <summary> 爬蟲方法 取得測站數據 </summary>
    def getAirValue(self):
        print(len(self.all_id_lst))
        for i in range(0,len(self.all_id_lst)):
            # htmlStr = requests.get(self.url_lst[i]).text
            # tempStr = htmlStr.split(":")[-1]
            try :
                res1 = urlopen(Request("http://www.airq.org.tw/Home/GetCurrentValueApi?station={}&sensor=pm2.5".format(self.all_id_lst[i])))
                res2 = urlopen(Request("http://www.airq.org.tw/Home/GetCurrentValueApi?station={}&sensor=pm10".format(self.all_id_lst[i])))
                res3 = urlopen(Request("http://www.airq.org.tw/Home/GetCurrentValueApi?station={}&sensor=temperature".format(self.all_id_lst[i])))
                res4 = urlopen(Request("http://www.airq.org.tw/Home/GetCurrentValueApi?station={}&sensor=humidity".format(self.all_id_lst[i])))

            except IOError:
                self.web_error.append(self.all_id_lst[i])

            else:
                pm25_pack = json.loads(res1.read())[0]['text'][14:]
                pm10_pack = json.loads(res2.read())[0]['text'][14:]
                temperature_pack = json.loads(res3.read())[0]['text'][14:]
                humidity_pack = json.loads(res4.read())[0]['text'][14:]

                self.id_lst.append(self.all_id_lst[i])
                self.pm25_lst.append(int(pm25_pack))
                self.pm10_lst.append(int(pm10_pack))
                self.h_lst.append(float(humidity_pack))
                self.t_lst.append(float(temperature_pack))

        print(len(self.id_lst))
        print(len(self.pm25_lst))
        print(len(self.pm10_lst))
        print(len(self.t_lst))
        print(len(self.h_lst))

        # id -> pm25
        self.dict_pm25 = dict(zip(self.id_lst, self.pm25_lst))
        # id -> pm10
        self.dict_pm10 = dict(zip(self.id_lst, self.pm10_lst))


    # 2017-11-23 edit by Mayday
    # <summary> 儲存測站數據 </summary>
    # <param name="timeStr"> 表格名稱 </summary>
    # <param name="id_lst"> 所有測站 ID 串列 </param>
    # <param name="pm25_lst"> 所有測站 PM2.5 數據串列 </param>
    # <param name="pm10_lst"> 所有測站 PM10 數據串列 </param>
    # <param name="t_lst"> 所有測站溫度數據串列 </param>
    # <param name="h_lst"> 所有測站濕度數據串列 </param>
    def dataSave(self):
        self.db.createAirData(self.timeStr,self.id_lst,self.pm25_lst,self.pm10_lst,self.t_lst,self.h_lst)    # Create AriInfo table
        # self.data = self.db.readAreaData(self.timeStr)     # Read AreaInfo table

    # 分析錯誤資料  傳回錯誤測站
    def analy(self):
        print("ana.getAreaId")
        self.ana.getAreaId(self.timeStr)                   # Get near area
        print("ana.getAreaAirInfo")
        self.ana.getAreaAirInfo(self.timeStr,self.dict_pm25,self.dict_pm10)              # Get near area PM25 and PM10 information

        print("s_PM25")
        self.ana.s_PM25()                                  # Cal near area air PM25 標準差
        print("s_PM10")
        self.ana.s_PM10()                                  # Cal near area air PM10 標準差
        print("avg_PM25")
        self.ana.avg_PM25()                                # Cal near area average PM25
        print("avg_PM10")
        self.ana.avg_PM10()                                # Cal near area average PM10

        print("GrubbsTest")
        error_site = self.ana.grubbsTest()                 # Get final error site value

        return error_site
