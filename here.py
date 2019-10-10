import requests
import pandas as pd
import geopandas as gpd
from shapely import wkt

path='C:/Users/Yijun Ma/Desktop/HERE/'
appid=pd.read_csv(path+'KEY.csv').loc[0,'appid']
appcode=pd.read_csv(path+'KEY.csv').loc[0,'appcode']

js='https://isoline.route.api.here.com/routing/7.2/calculateisoline.json'
js+='?app_id='+appid
js+='&app_code='+appcode
js+='&mode=balanced;truck;traffic:enabled;tollroad:0'
js+='&destination=geo!40.708183,-74.010467'
js+='&range=3600,7200,10800,14400,18000'
js+='&rangetype=time'
js+='&arrival=2019-10-08T08:00:00-05'
js+='&singlecomponent=false'
js+='&resolution=0'
js+='&maxPoints=100000'
js+='&quality=1'

rs=pd.DataFrame(requests.get(js).json())
df=pd.DataFrame(columns=['range','geom'])
for i in range(0,len(rs.loc['isoline','response'])):
    df.loc[i,'range']=rs.loc['isoline','response'][i].get('range')
    df.loc[i,'geom']='POLYGON (('+','.join([x.split(',')[1]+' '+x.split(',')[0] for x in rs.loc['isoline','response'][i].get('component')[0].get('shape')])+'))'
df['range']=pd.to_numeric(df['range'])

gdf=gpd.GeoDataFrame(df,geometry=df['geom'].map(wkt.loads),crs={'init':'epsg:4326'})
gdf.to_file(path+'HERE.shp')
