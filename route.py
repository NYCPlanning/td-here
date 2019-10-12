import requests
import pandas as pd
import geopandas as gpd
from shapely import wkt

path='C:/Users/Yijun Ma/Desktop/D/DOCUMENT/DCP2019/HERE/'
appid=pd.read_csv(path+'KEY.csv').loc[0,'appid']
appcode=pd.read_csv(path+'KEY.csv').loc[0,'appcode']

# https://developer.here.com/documentation/routing/topics/resource-calculate-route.html
js='https://route.api.here.com/routing/7.2/calculateroute.json'
js+='?app_id='+appid
js+='&app_code='+appcode
js+='&waypoint0=geo!41.374151,-73.897709'
js+='&waypoint1=geo!40.817355,-73.883310'
js+='&mode=balanced;truck;traffic:enabled;tollroad:0'
js+='&alternatives=3'
js+='&metricSystem=imperial'
js+='&resolution=0:10'
js+='&instructionFormat=text'
rs=pd.DataFrame(requests.get(js).json())



# https://developer.here.com/documentation/fleet-telematics/api-reference.html#operation%2FcalculateRouteUsingGET
js='https://fleet.cit.api.here.com/2/calculateroute.json'
js+='?app_id='+appid
js+='&app_code='+appcode
js+='&waypoint0=geo!41.374151,-73.897709'
js+='&waypoint1=geo!40.817355,-73.883310'
js+='&mode=fastest;truck;traffic:enabled;tollroad:0'
js+='&tollVehicleType=3'