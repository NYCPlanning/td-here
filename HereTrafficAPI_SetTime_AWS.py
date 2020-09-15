#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import time
import datetime
from datetime import datetime, timedelta



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
path='/home/mayijun/HERE/'


for i in range(0,1000):
    centerLatLong = "40.712651,-74.006051"
    apiKey = "h98-CibKYa59kR0XZODDB9muLpx2CAc_44w0Ym9IO0U&&responseattributes=sh"
    meters = "30000"
    url = "https://traffic.ls.hereapi.com/traffic/6.2/flow.json?prox="+ centerLatLong+ "," +meters +"&apiKey=" + apiKey
    page = requests.get(url).json()
    orgtimestamps = page.get('CREATED_TIMESTAMP')
    timestamps=datetime.strptime(orgtimestamps.split('.')[0],'%Y-%m-%dT%H:%M:%S')
    timestamps=timestamps-timedelta(hours=4)
    timestamps=timestamps.strftime('%m%d%H%M%S')
    print("timestamps:",timestamps)
    roads=page.get('RWS')[0].get('RW')
    suList=[]
    ffList=[]
    roadList = []
    fiList=[]
    pcList = []
    cnList=[]
    jfList = []
    spList = []
    liList = []
    for road in roads:
        description=road.get('DE')
        li=road.get('LI')
        if description is np.nan:
            description = "NA"
        fis = road.get('FIS')[0].get('FI')
        fisLen = len(fis)
        for fi in fis:
            flowItem = fi.get('TMC').get('DE')
            pointCode = fi.get('TMC').get('PC')
            cn=pd.to_numeric(fi.get('CF')[0].get('CN'))
            su=pd.to_numeric(fi.get('CF')[0].get('SU'))
            ff=pd.to_numeric(fi.get('CF')[0].get('FF'))
            jf=pd.to_numeric(fi.get('CF')[0].get('JF'))
            sp=pd.to_numeric(fi.get('CF')[0].get('SP'))
            fiList.append(flowItem)
            pcList.append(pointCode)
            cnList.append(cn)
            suList.append(su)
            ffList.append(ff)            
            jfList.append(jf)
            spList.append(sp)
        roadList.extend(([description] * fisLen))
        liList.extend(([li] * fisLen))
    shpdf = pd.DataFrame({'Roadway': roadList,'FlowItem':fiList, 'Li': liList, 'PointCode':pcList,'Confidence':cnList,'FreeFlow':ffList, 'JamFactor':jfList,'SpCapped':spList,'SpeedNotCap':suList})
    shpdf["SpRtNotCap"] = shpdf["SpeedNotCap"] / shpdf["FreeFlow"]
    shpdf["SpRtCapped"] = shpdf["SpCapped"] / shpdf["FreeFlow"]
    shpdf.to_csv(path + "Output/HT_" + timestamps + "_"+ meters + ".csv")
    time.sleep(3600)
