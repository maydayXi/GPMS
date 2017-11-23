# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 00:49:04 2017

@author: Mayday
"""

import requests
from bs4 import BeautifulSoup as bs

# <summary>Get useful data class</summary>
class Helper:

    # 2017-11-23 edit by Mayday
    # <summary> Find all error url and remove it by id </summary>
    # <param name = "id_lst">     Site id list </param>
    # <param name = "sensor_lst"> Sensor list  </param>
    # <return> Useful id list  </return>
    # <return> Useful url list </return>
    def urlHelper(self, all_id_lst, sensor_lst):
        self.error_id_lst = []
        self.error_sensor_list = []
        self.url_lst = []
        self.id_lst = []

        count = 0
        for Id in all_id_lst:
            for sensor in sensor_lst:
                # Get url
                url = 'http://www.airq.org.tw/Home/GetCurrentValueApi?station={}&sensor={}'.format(Id,sensor)
                # Get html text
                html = requests.get(url).text
                parse = bs(html,'html.parser')

                # Remove invalid id
                if str(parse.find('title')).find('錯誤') == 7:
                    self.error_id_lst.append(Id)
                    self.error_sensor_list.append(sensor)
                else:
                    self.url_lst.append(url)
                    if count%4 == 0:
                        self.id_lst.append(Id)
                    count += 1

        return self.id_lst,self.url_lst

    # <summary></summary>
    # <param name = "id_lst">  All site id lsit        </param>
    # <param name = "lon_lst"> All stie longitude list </param>
    # <param name = "lat_lst"> All site Latitude list  </param>
    # <param name = "note_lst">All site name lsit      </param>
    # <return> Useful site latitude list  </return>
    # <return> Useful site longitude list </return>
    # <return> Useful site name lsit      </return>
    def dataHelper(self,id_lst,lat_lst,lon_lst,note_lst):
        self.lon_lst = []
        self.lat_lst = []
        self.note_lst = []

        for item in self.id_lst:                #item = useful id
            for idx in range(0,len(id_lst)):
                if (item == id_lst[idx]):
                    self.lat_lst.append(lat_lst[idx])
                    self.lon_lst.append(lon_lst[idx])
                    self.note_lst.append(note_lst[idx])

        return self.lat_lst,self.lon_lst,self.note_lst
