from GPMSWEB.DBService import DBService
import numpy as np
import math

class dataAnaly:

    # 2017-10-20 add by Mayday
    def __init__(self):
        self.db = DBService()                       # Database instance
        self.area_gps = []                          # Final site area list
        self.note = []                              # Site name list

    # 2017-11-23 edit by Mayday
    # <summary>Get area point id</summary>
    # <param name = "timeStr">Table name</param>
    def getAreaId(self,timeStr):
        gps = []                                                        # Site area temp list
        print("read_DB_Postition")
        site_position_lst = self.db.lst_readPositionData(timeStr)       # Read site position data

        print("add_Position_to_GPS[]")
        for item in site_position_lst:
            gps.append([item[0],item[1],item[2]])   # Add site id,lat and lon
            self.note.append(item[3])               # Add site name

        # cal area point
        for i in gps:
            temp = []                               # Temp list
            temp.append(i[0])                       # Add point itself

            print("add_area_function")
            for j in gps:
                if (self.haversine(i[2],i[1],j[2],j[1]) > 0 and
                self.haversine(i[2],i[1],j[2],j[1]) <= 5) :
                    temp.append(j[0])

            self.area_gps.append(temp)

    # 2017-11-24 edit by Mayday
    # <summary> 取得區域測站名稱 </summary>
    # <return> 區域測站名稱串列 </return>
    def lst_getAreaSite(self, row):
        st_note_lst = []

        for item in self.area_gps[row]:
            st_note = self.db.m_readSiteNoteById(item)
            st_note_lst.append(st_note[0])

        return st_note_lst

    # <summary>計算附近的點</summary>
    # <param name = "lon1">第一點經度</param>
    # <param name = "lat1">第一點緯度</param>
    # <param name = "lon2">第二點經度</param>
    # <param name = "lat2">第二點緯度</param>
    def haversine(self,lon1, lat1, lon2, lat2):         # 經度1，緯度1，經度2，緯度2
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        # haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371                                        # 地球半徑
        return c * r

    # 2017-11-23 edit by Mayday
    # <summary>Get area PM2.5 and PM10 information</summary>
    # <param name = "timeStr">Table name</param>
    def getAreaAirInfo(self,timeStr,dict_pm25,dict_pm10):

        self.area_pm25 = []             # Area PM2.5 list
        self.area_pm10 = []             # Area PM10 list
        for item in self.area_gps:
            print("getAreaAirInfo-1")
            temp25 = []                 # Temp PM2.5 list
            temp10 = []                 # Temp PM10 list
            for Id in item:
                print("getAreaAirInfo-2")
                temp25.append(dict_pm25['{}'.format(Id)])
                temp10.append(dict_pm10['{}'.format(Id)])

            self.area_pm25.append(temp25)
            self.area_pm10.append(temp10)

        #return self.neighbor_pm25,self.neighbor_pm10

    # PM25 標準差
    def s_PM25(self):
        self.s_pm25_lst = []
        for item in self.area_pm25:
            self.s_pm25_lst.append(np.std(item))

    # PM10 標準差
    def s_PM10(self):
        self.s_pm10_lst = []
        for item in self.area_pm10:
            self.s_pm10_lst.append(np.std(item))

    # PM25 Average
    def avg_PM25(self):
        self.avg_pm25_lst = []
        for item in self.area_pm25:
            self.avg_pm25_lst.append(np.mean(item))

    # PM10 Average
    def avg_PM10(self):
        self.avg_pm10_lst = []
        for item in self.area_pm10:
            self.avg_pm10_lst.append(np.mean(item))

    # Cal grubbsTest value
    def grubbsTest(self):

        print("grubbsTest-1")
        self.area_final = []
        index = 0                                       # item index
        print("grubbsTest-2")
        for item in self.area_pm25:
            An = self.db.m_selectGAlpha(len(item))
            if An != None:          # if N >= 3
                x = An[0]
                Gn = abs((item[0] - self.avg_pm25_lst[index]) / self.s_pm25_lst[index])
                final = x - Gn
                if final < 0:
                    self.area_final.append(self.note[index])

            index += 1

        print("grubbsTest-3")
        return self.area_final
