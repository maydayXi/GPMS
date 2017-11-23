# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 05:27:44 2017

@author: Mayday
"""

from GPMSWEB.DBService import DBService          # 資料庫類別
from GPMSWEB.dataAnaly import dataAnaly          # 資料分析類別

class TableService:

    # 2017-10-12 add by Mayday
    def __init__(self):
        self.db = DBService()                   # New database instance
        self.ana = dataAnaly()                  # New dataAnaly instance

    # 2017-11-23 edit by Mayday
    # <summary> 取得所有空氣資料表格名稱 </summary>
    # <return> 所有空氣資料表名稱串列 </return>
    def lst_getAllAirInfoTableName(self):
        tables = self.db.lst_readAllAirInfoTableName()

        air_table_lst = []
        for item in tables:
            air_table_lst.append(item[0])

        return air_table_lst

    # 2017-11-23 edit by Maydya
    # <summary> 取得所有異常資料表名稱 </summary>
    # <return> 所有異常資料表名稱串列 </return>
    def lst_getAllErrorTableName(self):
        tables = self.db.lst_readAllErrorTableName()

        error_table_lst = []
        for table in tables:
            error_table_lst.append(table[1])

        return error_table_lst

    # 2017-10-12 add by Mayday
    # <summary> 取得 x 與 y 軸的數據 </summary>
    # <param name = "table_name"> 表格名稱或表格陣列 </param>
    # <param name = "stId"> 測站 ID </param>
    # <param name = "tag"> 時間模式 </param>
    # <return> X 軸數據, y 軸數據 </return>
    def getXYAxis(self,table_name,stId,interval):

        pm25_lst = []       #Y 軸數據
        time_lst = []       #X 軸數據

        if interval == 60:                              # get the timeline of hour
            h = int(table_name[-1].split('_')[-2])      # get current hour
            for i in range(h-11,h+1):                   # 過去 12 小時到現在做為 X 軸
                if(i < 0):                              # < 0 時往前會出現負數
                    i = 24 + i
                time_lst.append(i)

            for i in range(len(table_name)-144,         # 取得過去 12 小時的空氣資料
                           len(table_name),12):         # 一小時取一次，間隔 12(5分)
                y = self.db.readPM25ById(table_name[i],
                                         stId)
                if y == None:                           # 感測器如果關了
                    pm25_lst.append(-1)                 # 填入 -1
                else:
                    pm25_lst.append(y[1])               # 填充 Y 軸

        elif interval == 30:                            # get the timeline of 30 min

            for i in range(len(table_name)-72,          # 取得過去 6 小時的空氣資料
                           len(table_name),6):          # 半小時取一次，間隔 6(5分)
                x = table_name[i][-5:].replace(         # 取得 X 軸，即時、分
                        '_',':')
                time_lst.append(x)                      # 數據填充 X 軸

                y = self.db.readPM25ById(table_name[i], # 取得 Y 軸，即 PM2.5 的值
                                         stId)
                if y == None:                           # 感測器如果關了
                    pm25_lst.append(-1)                 # 填入 -1
                else:
                    pm25_lst.append(y[1])               # 數據填充 Y 軸

        elif interval == 5:                             # get the timeline of 5 min
            for i in range(len(table_name)-12,          # 取得過去 1 小時的空氣資料
                           len(table_name)):            # 5 分鐘取一次，間隔 12(1H)
                x = table_name[i][-5:].replace(         # 取得 X 軸，即時、分
                        '_',':')
                time_lst.append(x)                      # 填充 X 軸

                y = self.db.readPM25ById(table_name[i], # 取得 Y 軸，即PM2.5 的值
                                         stId)
                if y == None:                           # 感測器如果關了
                    pm25_lst.append(-1)                 # 填入 -1
                else:
                    pm25_lst.append(y[1])               # 填充 Y 軸

        else:
            x = self.ana.getAreaData(table_name[8:])

            temp = []
            for item in x:
                if stId == item[0]:
                    temp = item

            for item in temp:
                y = self.db.readPM25ById(table_name,item)
                pm25_lst.append(y[1])
                time_lst.append(self.db.readSiteNoteById(item)[0])

        return time_lst,pm25_lst
