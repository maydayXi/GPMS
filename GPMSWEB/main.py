# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 17:06:34 2017

@author: user
"""
#==============================import package==============================#

#from excelService import Service        #excel class
from GPMSWEB.DBService import DBService         #DB class
from GPMSWEB.Helper import Helper               #data helper class
from GPMSWEB.dataAnaly import dataAnaly         #data analy package
import requests,time                    #html package , time package
#from FB import getInfo

class main:

    def __init__(self):                     #初始化所有參數
        self.db = DBService()               #database instance
        self.ana = dataAnaly()              #dataAnaly instance
        self.data = Helper()                #url data fetch instance
        self.sensor_lst = ['pm2.5','pm10','temperature','humidity']
        self.all_id_lst = []
        self.pm25_lst = []                   #pm2.5 lsit
        self.pm10_lst = []                   #pm10 list
        self.t_lst = []                      #temperatuer lsit
        self.h_lst = []                      #humidity list

    def getInitData(self):
        result = self.db.readSiteData()      #get all site information
        for item in result:
            self.all_id_lst.append(item[0])
        #get useful data list
        self.id_lst,self.url_lst = self.data.urlHelper(self.all_id_lst,self.sensor_lst)

    def getAirValue(self):
        self.timeStr = time.strftime('%Y_%m_%d_%H_%M')       #get current time
        for i in range(0,len(self.url_lst)):
            htmlStr = requests.get(self.url_lst[i]).text
            tempStr = htmlStr.split(":")[-1]
            if i%4 == 0:
                self.pm25_lst.append(int(tempStr[:-3]))
            if i%4 == 1:
                self.pm10_lst.append(int(tempStr[:-3]))
            if i%4 == 2:
                self.t_lst.append(float(tempStr[:-3]))
            if i%4 == 3:
                self.h_lst.append(float(tempStr[:-3]))

    def dbHandle(self):
        self.db.createAirData(self.timeStr,self.id_lst,self.pm25_lst,self.pm10_lst,self.t_lst,self.h_lst)    #Create AriInfo table
        self.data = self.db.readAreaData(self.timeStr)                                   #Read AriInfo table

    def analy(self):
        self.ana.getAreaId(self.timeStr)                   #get near area
        self.ana.getAreaAirInfo(self.timeStr)              #get near area air information

        self.ana.s_PM25()                                  #cal near area air PM25 標準差
        self.ana.s_PM10()                                  #cal near area air PM10 標準差
        self.ana.avg_PM25()                                #cal near area average PM25
        self.ana.avg_PM10()                                #cal near area average PM10
        result = self.ana.grubbsTest()                     #cal final value

        return result
