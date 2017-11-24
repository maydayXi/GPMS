from GPMSWEB.main import main                   # 自建主程式類別
from GPMSWEB.DBService import DBService         # 自建資料庫類別
from GPMSWEB.TableService import TableService   # 自建資料表類別
from GPMSWEB.dataAnaly import dataAnaly         # 資料分析類別
from datetime import datetime
from firebase import firebase

# 初始所有類別物件
x = main()                                  # 爬蟲程式
db = DBService()                            # 資料庫物件
analy = dataAnaly()                         # 資料分析物件
table = TableService()                      # 表格資料物件

x = main()
x.getInitData()
x.getAirValue()
x.dataSave()
table_name_lst = table.lst_getAllAirInfoTableName()
error_site = x.analy()

error = []
json_url = 'https://ch13-ccc60.firebaseio.com/'
map_json = firebase.FirebaseApplication(json_url,None)
obj = map_json.get(json_url, None)

for i in range(len(obj)):
    map_json.delete(json_url, str(i))

for i,item in enumerate(error_site):
    error_air_data = db.m_readAirDataByNote(table_name_lst[-1], item)
    error_position = db.m_readSitePositionByNote(item)
    error.append([error_air_data[0],item,error_air_data[1],                 # stId, PM2.5
                   error_air_data[2],error_air_data[3],                     # PM10, Temperature
                   error_air_data[4],error_position[0],error_position[1]])  # Humidity, stLatitude, stLongitude
    url = table_name_lst[-1] + error_air_data[0]
    map_json.put(json_url,str(i),{"stNote":item, "lat":error_position[0], "lng":error_position[1], "url":url})

db.createErrorData(table_name_lst[-1][8:], error)
