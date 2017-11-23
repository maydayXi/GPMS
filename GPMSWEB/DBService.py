# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 18:22:47 2017

@author: user
"""

# import sqlite3,os         # locahost database use slqite
import psycopg2 as db       # online database use postgreSQL

class DBService:

    # 2017-11-22 edit by Mayday
    # <summay> Change DB using online postgreSQL database </summary>
    # 類別初始執行
    def __init__(self):
        # self.path = os.path.dirname(__file__)       #取得資料庫所在路徑
        self.connection = db.connect(database="d1hr2vo3lmf7l",
					                 user="u691nrkdrrb3v2",
					                 password="pe1985615c773d417f2b004d74c5855cb0787fad0b05a491ed35ccc035b5d6499",
					                 host="ec2-34-236-253-151.compute-1.amazonaws.com",
					                 port="5432")

    # 2017-11-23 edit by Mayday
    # <summary> 取得所有空氣資料表 </summary>
    # <return> 空氣資料表串列 </return>
    def lst_readAllAirInfoTableName(self):
        print("lst_readAllAirInfoTableName-1")
        queryStr = '''SELECT relname FROM pg_class c
                      WHERE relkind = 'r' AND
                      relname LIKE 'a%'
                      ORDER BY relname'''
        print("lst_readAllAirInfoTableName-2")
        cursor = self.connection.cursor()
        print("lst_readAllAirInfoTableName-3")
        cursor.execute(queryStr)
        print("lst_readAllAirInfoTableName-4")
        air_table_lst = cursor.fetchall()
        print("lst_readAllAirInfoTableName-5")

        return air_table_lst

    # 2017-11-17 add by Mayday
    # <summary> 取得所有異常測站資料表 </summary>
    # <return> 異常資料表名稱串列 </return>
    def lst_readAllErrorTableName(self):
        queryStr = '''SELECT relname FROM pg_class c
                      WHERE relkind = 'r' AND
                      relname LIKE 'e%'
                      ORDER BY relname'''
        cursor = self.connection.cursor()
        cursor.execute(queryStr)
        error_table_lst = cursor.fetchall()

        return error_table_lst

    # 2017-11-23 edit by Mayday
    # <summary> Create site table </summary>
    # <param name = "id_lst">   Site id list        </param>
    # <param name = "lat_lst">  Site latitude list  </param>
    # <param name = "lon_lst">  Site longitude list </param>
    # <param name = "note_lst"> Site name list      </param>
    def createSiteData(self,id_lst,lat_lst,lon_lst,note_lst):
        self.id_lst = id_lst
        self.lat_lst = lat_lst
        self.lon_lst = lon_lst
        self.note_lst = note_lst
        # connection = sqlite3.connect('PM25.sqlite')         # local db using
        cursor = self.connection.cursor()                     # 取得資料庫操作物件

        # Create site table syntax
        sqlStr = """CREATE TABLE IF NOT EXISTS SiteInfo(
                    stId TEXT PRIMARY KEY NOT NULL,
                    stLatitude FLOAT,
                    stLongitude FLOAT,
                    stNote TEXT)"""
        cursor.execute(sqlStr)                                # 執行 SQL 語法
        self.connection.commit()                              # 資料庫更新

        for i in range(0,len(id_lst)):
            sqlStr="""INSERT INTO SiteInfo
                      (stId, stLatitude, stLongitude, stNote)
                      VALUES('{}',{},{},'{}')""".format(
                      self.id_lst[i],self.lat_lst[i],
                      self.lon_lst[i],self.note_lst[i],)
            cursor.execute(sqlStr)

        self.connection.commit()
        self.connection.close()                              # 關閉資料庫連線

    # 2017-11-23 edit by Mayday
    # <summary>Read stie information</summary>
    # <return>Site information list</return>
    def lst_readSiteData(self):
        queryStr = 'SELECT * FROM SiteInfo'
        cursor = self.connection.cursor()
        cursor.execute(queryStr)
        site_info_lst = cursor.fetchall()

        return site_info_lst

    # 2017-10-25 add by Mayday
    # <summary>Read site name by site id</summary>
    # <param name = 'id'>Site id</param>
    # <return>Site name</return>
    def readSiteNoteById(self,Id):
        connection = sqlite3.connect(self.path + '/' + 'PM25.sqlite')
        sqlStr = 'select stNote from SiteInfo where stId = "{}"'.format(
                Id)
        cursor = connection.execute(sqlStr)
        result = cursor.fetchone()

        return result

    # 2017-11-23 edit by Mayday
    # <summary> Read site position by site Name </summary>
    # <return> One site position </return>
    def m_readSitePositionByNote(self,Note):
        queryStr = '''SELECT stLatitude, stLongitude FROM SiteInfo
                      WHERE stNote = '{}'
                   '''.format(Note)
        cursor = self.connection.cursor()
        cursor.execute(queryStr)
        site_position = cursor.fetchone()

        return site_position

    # 2017-11-23 edit by Mayday
    # <summary> Create air information table </summary>
    # <param name = "timeStr">  Table name             </param>
    # <param name = "id_lst">   Site Id list           </param>
    # <param name = "pm25_lst"> PM2.5 value list       </param>
    # <param name = "pm10_lst"> PM10 value list        </param>
    # <param name = "t_lst">    Temperature value list </param>
    # <param name = "h_lst">    Humidity value list    </param>
    def createAirData(self,timeStr,id_lst,pm25_lst,pm10_lst,t_lst,h_lst):
        # Create air information table sql syntax
        sqlStr = """CREATE TABLE AirInfo_{}
                    (stId TEXT NOT NULL,
                    PM25 INTEGER,
                    PM10 INTEGER,
                    Temperature FLOAT,
                    Humidity FLOAT,
                    PRIMARY KEY(stId),
                    FOREIGN KEY(stId) REFERENCES SiteInfo(stId))""".format(timeStr)
        cursor = self.connection.cursor()
        cursor.execute(sqlStr)
        self.connection.commit()

        for i in range(0,len(id_lst)):
            sqlStr = """INSERT INTO AirInfo_{}
                        (stId, PM25, PM10, Temperature, Humidity)
                        VALUES('{}',{},{},{},{})""".format(timeStr,
                        id_lst[i],pm25_lst[i],pm10_lst[i],t_lst[i],h_lst[i])
            cursor.execute(sqlStr)
        self.connection.commit()

    # 2017-11-23 add by Mayday
    # <summary>Read air data by station name </summary>
    # <param name = "table_name"> Table name </param>
    # <param name = "stNote"> Station name   </param>
    # <return> Air data belonging to station name </return>
    def m_readAirDataByNote(self,table_name,stNote):
        queryStr = """SELECT {}.* FROM {}, SiteInfo
                      WHERE SiteInfo.stId = {}.stId and SiteInfo.stNote = '{}'
                   """.format(table_name,table_name,table_name,stNote)
        print("m_readAirDataByNote-connection")
        cursor = self.connection.cursor()
        print("m_readAirDataByNote-execute")
        cursor.execute(queryStr)
        print("m_readAirDataByNote-fetchone")
        result = cursor.fetchone()
        # self.connection.close()

        return result

    # 2017-10-12 add by Mayday
    # <summary> Read PM25 data by Id </summary>
    # <param name ="table_name"> Table name </param>
    # <param name ="Id"> Data Id </param>
    # <teturn> one PM25 data belonging to id</return>
    def readPM25ById(self,table_name,Id):
        connection = sqlite3.connect(self.path + '/' + 'PM25.sqlite')
        queryStr = 'SELECT stId,PM25 FROM {} WHERE stId = "{}"'.format(
                table_name,Id)
        cursor = connection.execute(queryStr)
        result = cursor.fetchone()

        return result

    # 2017-11-23 edit by Mayday
    # <summary> Read all site position data </summary>
    # <param name="timeStr"> table name </param>
    # <return> All site position data </return>
    def lst_readPositionData(self,timeStr):
        queryStr="""SELECT AirInfo_{}.stId, SiteInfo.stLatitude,
                    SiteInfo.stLongitude, SiteInfo.stNote
                    FROM AirInfo_{}, SiteInfo
                    WHERE SiteInfo.stId = AirInfo_{}.stId
                 """.format(timeStr,timeStr,timeStr)

        cursor = self.connection.cursor()
        cursor.execute(queryStr)
        site_position_lst = cursor.fetchall()

        return site_position_lst

    # 2017-11-23 edit by Mayday
    # <summary>Read PM25 and PM10 by Id</summary>
    # <param name = "timeStsr">table name </param>
    # <param name = "Id">      Site Id    </param>
    # <return>one PM25 and PM10 </return>
    def m_readPM25PM10ById(self,timeStr,Id):
        queryStr = '''SELECT AirInfo_{}.PM25, AirInfo_{}.PM10 FROM AirInfo_{}
                      WHERE stId = '{}'
                   '''.format(timeStr,timeStr,timeStr,Id)
        cursor = self.connection.cursor()
        cursor.execute(queryStr)
        pm25_pm10 = cursor.fetchone()

        return pm25_pm10

    # 2017-11-23 edit by Mayday
    # <summary> Select Alpha by N </summary>
    # <param name = "n"> 樣本數    </param>
    # <return> Alpha </return>
    def m_selectGAlpha(self,n):
        queryStr = '''SELECT GrubbsTValue.alpha FROM GrubbsTValue
                      WHERE N = {}'''.format(n)
        cursor = self.connection.cursor()
        cursor.execute(queryStr)
        alpha = cursor.fetchone()

        return alpha

    # 2017-11-23 edit by Maydya
    # <summary> 建立異常測站資料表 傳入異常資料 </summary>
    # <param name = "timeStr"> 偵測時間 </param>
    # <param name = "data_lst"> 異常資料 </param>
    def createErrorData(self, timeStr, error_lst):
        sqlStr = """CREATE TABLE ErrorInfo_{}
                    (stId TEXT NOT NULL,
                     stNote TEXT,
                     PM25 INTEGER,
                     PM10 INTEGER,
                     Temperature FLOAT,
                     Humidity FLOAT,
                     stLatitude FLOAT,
                     stLongitude FLOAT,
                     PRIMARY KEY(stId),
                     FOREIGN KEY(stId) REFERENCES SiteInfo(stId))
                 """.format(timeStr)
        cursor = self.connection.cursor()
        cursor.execute(sqlStr)
        self.connection.commit()

        for item in error_lst:
            sqlStr = '''INSERT INTO ErrorInfo_{}
                        (stId, stNote, PM25, PM10,
                         Temperature, Humidity, stLatitude, stLongitude)
                        VALUES('{}','{}',{},{},{},{},{},{})
                     '''.format(timeStr, item[0], item[1], item[2], item[3],
                                item[4], item[5], item[6], item[7])
            cursor.execute(sqlStr)

        self.connection.commit()

    # 2017-10-31 Add by Mayday
    # <summary>Read error site data</summary>
    # <param name = 'table_name'>Error table name</param>
    # <return>Error site data list</summay>
    def readErrorData(self, table_name):
        sqlStr = "select * from {} where {}.PM25 > 54".format(table_name,table_name)
        cursor = self.connection.cursor()
        cursor.execute(sqlStr)

        result = cursor.fetchall()

        return result
