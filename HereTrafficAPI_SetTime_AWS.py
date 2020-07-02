#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 20:23:12 2020

@author: rlin
"""


import re
import requests
#import urllib2
import xlrd
from bs4 import BeautifulSoup
import pandas as pd
import decimal
import geopandas as gpd
import numpy as np
import os
import time
import json
from xml.etree.ElementTree import XML, fromstring, tostring
from matplotlib import pyplot as plt
from shapely.geometry import Point, LineString, shape
from dateutil import tz
from datetime import datetime, timedelta
from threading import Timer
#import sys
#print(sys.path)


#import pause
#import schedule

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

hrs = 15
mins = 0
minInt = 60
#x=datetime.today()
path='/home/mayijun/HERE/'

def Longfunc():
    now = datetime.now()
    global minInt
    
    
    
    print("now:",now)
    # define file path and read raw data
#    path='/Users/rl/OneDrive - NYC O365 HOSTED/Desktop/subway ridership/Here Traffic Data/Here Traffic Data/'
    #masterdf = pd.read_csv(path + "MasterData.csv", header= 0, index_col=False, encoding='latin_1')
    # masterdf = pd.read_csv(path + "Handlebar Master 20191204.csv", header= 0, index_col=False, nrows =3003, encoding='latin_1')
    
    # subwayEntrance = geopandas.read_file("Subway Entrances/geo_export_1b219a58-cde8-4260-922f-9397da50675d.shp")
    #masterdf = pd.read_csv(path + "Handlebar Master 20191204.csv", header= 0, index_col=False, encoding='latin_1')
    #stations = pd.read_csv(path+"LookUpTable.csv", header= 0, index_col=False, usecols = [0,1,2,6,10,11])
    #jsonFile = pd.read_json(path+"flowjson.json")
    #dictJson = json.loads(str(jsonFile))
    
    #url = "https://traffic.ls.hereapi.com/traffic/6.2/flow.json?prox=40.708,-74.010566,50&apiKey=h98-CibKYa59kR0XZODDB9muLpx2CAc_44w0Ym9IO0U&&responseattributes=sh"
    centerLatLong = "40.712651,-74.006051"
    apiKey = "h98-CibKYa59kR0XZODDB9muLpx2CAc_44w0Ym9IO0U&&responseattributes=sh"
    meters = "30000"
    url = "https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?prox="+ centerLatLong+ "," +meters +"&apiKey=" + apiKey
    #response = urllib2.urlopen(url)
    #data = response.read()
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    body = soup.find('body')
    orgtimestamps = fromstring(str(body))[0].attrib["created_timestamp"]
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    temptimestamps = datetime.strptime(orgtimestamps, '%Y-%m-%dT%H:%M:%SZ')
    temptimestamps = temptimestamps.replace(tzinfo=from_zone)
    temptimestamps = temptimestamps.astimezone(to_zone)
    timestamps = temptimestamps.strftime("%m%d%H%M%S")
    print("timestamps:",timestamps)
    
    roads = soup.find_all('rw')
    
    
#    loc_list_hv=[]

    suList=[]
    ffList=[]
    roadList = []
    fiList=[]
#    lenList = []
    pcList = []
#    qdList = []
#    idxRoadList = []
    cnList=[]
    jfList = []
    spList = []
#    shpList = []
#    midList =[]
    liList = []
    
    #shpdf = pd.DataFrame(columns=['Roadway','FlowItem','RoadID','Length','PointCode','QueuingDirct','Lat','Long','ShapeID', 'Confidence','FreeFlow', 'JamFactor','SpCappedByLmt','Speed'])
#    idx = 0
#    idxRoad = 0
    for road in roads:
#        roadLenList = []
        roadxml = fromstring(str(road))
        description = roadxml.attrib["de"]
        li = roadxml.attrib["li"]
        if description is np.nan:
            description = "NA"
    #    print(description)
        fis = road.find_all('fi')
        fisLen = len(fis)
        for fi in fis:
#            fiLenList = []
            myxml = fromstring(str(fi))
            
            flowItem = myxml[0].attrib["de"]
#            length = myxml[0].attrib["le"]
            pointCode = myxml[0].attrib["pc"]
#            queuingDirct = myxml[0].attrib["qd"]
            for child in myxml:
                #print(child.tag, child.attrib)
#                if('fc' in child.attrib):
#                    fc=int(child.attrib['fc'])
                if('cn' in child.attrib):
                    cn=float(child.attrib['cn'])
                if('su' in child.attrib):
                    su=float(child.attrib['su'])
                if('ff' in child.attrib):
                    ff=float(child.attrib['ff'])
                if('jf' in child.attrib):
                    jf=float(child.attrib['jf'])
                if('sp' in child.attrib):
                    sp=float(child.attrib['sp'])
        #    if((fc<=2) and (cn>=0.7)):
#            if((cn>=0.5)):
#                idxShp = 0
#            shps=road.find_all("shp")
#            shpLen = len(shps)
#            for j in range(0,len(shps)):
#                shpLenList = []
#                latlong=shps[j].text.replace(',',' ').split()
#                pointLen = int(len(latlong)/2)
#                roadLenList.append(pointLen)
#                fiLenList.append(pointLen)
#                shpLenList.append(pointLen)
#                for i in range(0,pointLen):
#                    loc_list_hv.append([float(latlong[2*i]),float(latlong[2*i+1]),float(su),float(ff)])
#                        latList.append(float(latlong[2*i]))
#                        longList.append(float(latlong[2*i+1]))
            suList.append(float(su))
            ffList.append(float(ff))
#                    shpdf.loc[idx, "Roadway"] = description
#                    shpdf.loc[idx, "FlowItem"] = flowItem
#                    shpdf.loc[idx, "RoadID"] = idxRoad
#                    shpdf.loc[idx, "Length"] = length
#                    shpdf.loc[idx, "PointCode"] = pointCode
#                    shpdf.loc[idx, "QueuingDirct"] = queuingDirct
#                    shpdf.loc[idx, "Lat"] = float(latlong[2*i])
#                    shpdf.loc[idx, "Long"] = float(latlong[2*i+1])
#                    shpdf.loc[idx, "ShapeID"] = idxShp
#                    shpdf.loc[idx, "Confidence"] = cn
#                    shpdf.loc[idx, "FreeFlow"] = float(ff)
#                    shpdf.loc[idx, "JamFactor"] = jf
#                    shpdf.loc[idx, "SpCappedByLmt"] = float(sp)
#                    shpdf.loc[idx, "Speed"] = float(su)
#                        idx = idx + 1
#                lats.append(la)
#                longs.append(lo)
#                sus.append(np.mean(su1))
#                ffs.append(np.mean(ff1))
#                    shpList.extend(([idxShp] * sum(shpLenList)))
#                    idxShp = idxShp + 1
            fiList.append(flowItem)
#            idxRoadList.extend(([idxRoad] * sum(fiLenList)))
#            lenList.extend(([length] * sum(fiLenList)))
            pcList.append(pointCode)
#            qdList.extend(([queuingDirct] * sum(fiLenList)))
            cnList.append(cn)
            jfList.append(jf)
            spList.append(float(sp))
        roadList.extend(([description] * fisLen))
        liList.extend(([li] * fisLen))
#        print(idxRoad)
#        idxRoad = idxRoad + 1
    
    
    
    shpdf = pd.DataFrame({'Roadway': roadList,'FlowItem':fiList, 'Li': liList, 'PointCode':pcList,'Confidence':cnList,'FreeFlow':ffList, 'JamFactor':jfList,'SpCapped':spList,'SpeedNotCap':suList})
    shpdf["SpRtNotCap"] = shpdf["SpeedNotCap"] / shpdf["FreeFlow"]
    shpdf["SpRtCapped"] = shpdf["SpCapped"] / shpdf["FreeFlow"]  
      
#    geometry = [Point(xy) for xy in zip(shpdf.Long, shpdf.Lat)]
#    pointdf = gpd.GeoDataFrame(shpdf, geometry=geometry)
#    
#    geodf = pointdf.groupby(['Roadway','Li','FlowItem','PointCode', 'Confidence','FreeFlow', 'JamFactor','SpCappedByLmt','Speed'], as_index=False)['geometry'].agg({'geometry': lambda x:LineString(x.tolist())})
#    geodf["SpeedRatio"] = geodf["Speed"] / geodf["FreeFlow"]
#    geodf["SpeedLmtRatio"] = geodf["SpCappedByLmt"] / geodf["FreeFlow"] 
#    geodf = gpd.GeoDataFrame(geodf, geometry='geometry')
#    
#    
#    #testdf = geodf.loc[geodf["Roadway"] == "Broadway"]
#    print("Saving shp...")
#    geodf.to_file(path + "HT_" + timestamps + "_"+ meters + ".shp")
    
    #testdf.to_file("test.shp")
    shpdf.to_csv(path + "Output/HT_" + timestamps + "_"+ meters + ".csv")
    print("Duration:", datetime.now() - now)
    
    
    print("mins:",  mins + minInt)
    
    y = x.replace(day=x.day, hour=hrs, minute=mins, second=0, microsecond=0) + timedelta(minutes=minInt)
    minInt = minInt + 60
    delta_t = y-datetime.now()

    secs = delta_t.total_seconds()
#    print("Timer:", datetime.now())
    t = Timer(secs, Longfunc)
#    print("Timer:", datetime.now())
    t.start()
#    return x, minInt
#    print("start:", datetime.now())

#Longfunc(x, mins)

x=datetime.today()
print("mins:",  mins)
y = x.replace(day=x.day, hour=hrs, minute=mins, second=0, microsecond=0)
#mins = mins + 3
#y = x.replace(day=x.day, hour=22, minute=15, second=0, microsecond=0) + timedelta(seconds=0)
delta_t = y-x

secs = delta_t.total_seconds()
#def hello_world():
#    print("hello world")
##    y = x + timedelta(seconds=2)
#    delta_t = timedelta(minutes=20)
#
#    secs = delta_t.total_seconds()
#    t = Timer(secs, hello_world)
#    t.start()

t = Timer(secs, Longfunc)
t.start()

    
#schedule.every().day.at("20:36").do(Longfunc,'It is 20:36')
#
#while True:
#    schedule.run_pending()
#    time.sleep(60) # wait one minute



#print("draw pictures")            
#fig=plt.figure()
#plt.style.use('dark_background')
##plt.plot(np.linspace(0,10,10),np.linspace(0,10,10))
#plt.grid(False)
#for i in range(0,len(lats)):
#    if(sus[i]/ffs[i]<0.25):
#        plt.plot(longs[i],lats[i], c='brown',linewidth=0.5)
#    elif(sus[i]/ffs[i]<0.5):
#        plt.plot(longs[i],lats[i], c='red',linewidth=0.5)
#    elif(sus[i]/ffs[i]<0.75):
#        plt.plot(longs[i],lats[i], c='yellow',linewidth=0.5)
#    else:
#        plt.plot(longs[i],lats[i], c='green',linewidth=0.5)
#    #print(i)
##plt.xlim(-77.055,-77.015)
##plt.ylim(38.885,38.91)
#
#plt.axis('off')
#plt.show()
#fig.savefig(path+'mapCityHall1000.png', dpi=100)