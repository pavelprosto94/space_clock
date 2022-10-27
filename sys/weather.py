import os, sys, urequests, wifiCfg, json
sys.path.append("/flash/sys")
from helper import fileExist, safetyLoadJson
appid = "35129c3b68d0012d3ef823187750bf7d"
CACHEPATH = "/flash/res/weather"
if not fileExist(CACHEPATH):
  os.mkdir(CACHEPATH) 
 
def getCity():
  data = {}
  if ('weather.txt' in os.listdir('/flash')):
    with open('/flash/weather.txt', 'r') as json_file:
      data = json.load(json_file)
  try:
    ans=data['weather']['city']
    return ans
  except Exception as e:
    return -1
     
def SeachCity(s_city = ""):
  rez=[]
  if wifiCfg.wlan_sta.isconnected():
    if (s_city!=""):
      try:
        res = urequests.request(method="GET", 
                            url="http://api.openweathermap.org/data/2.5/find?q={}&APPID={}".format(s_city, appid), 
                            headers={ 'User-Agent': 'M5Stack'})
        data = res.json()
        for d in data['list']:
          rez.append(str(d['name'])+","+str(d['sys']['country'])+" ["+str(d['id'])+"]")
      except Exception as e:
        print("Exception (find):", e)
        pass
  return rez

def GetForecastWeather(city_id=-1, lang="en"):
  rez=["No city set", "", "?", "/flash/res/weather/error.png", "", "", "?", "/flash/res/weather/error.png", ""]
  if int(city_id)>-1:
    try:
      res = urequests.request(method="GET", 
                          url="http://api.openweathermap.org/data/2.5/forecast?id={}&units=metric&lang={}&APPID={}".format(city_id, lang, appid),
                          headers={ 'User-Agent': 'M5Stack'})
      res = res.json()
      name=res['city']['name']
      for i in range(0,2):
        data=res['list'][i*2]
        conditions=data['weather'][0]['description']
        temp=str(int(data['main']['temp']))+" C°"
        dt_txt=data['dt_txt']
        if temp[0]!="-" and temp!="0": temp="+"+temp
        icon="{}/{}.png".format(CACHEPATH,data['weather'][0]['icon'])
        iconURL="http://openweathermap.org/img/wn/{}.png".format(data['weather'][0]['icon'])
        if not fileExist(icon):
          try:
            res_img=urequests.request(method="GET", 
                                  url=iconURL, 
                                  headers={ 'User-Agent': 'M5Stack'})
            with open(icon, 'wb') as fb:
              fb.write(res_img.content) 
          except Exception as e:
            rez[0]=str(e)
            icon="/flash/res/weather/error.png"
        if i==0:
          rez=[name,conditions,temp,icon,dt_txt]
        else:
          rez=rez+[conditions,temp,icon,dt_txt]
      return(rez)
    except Exception as e:
      rez[0]=str(e)
      return(rez)
  return(rez)

def GetWeather(city_id=-1, lang="en"):
  rez=["No city set", "", "?", "/flash/res/weather/error.png"]
  if int(city_id)>-1:
    try:
      res = urequests.request(method="GET", 
                          url="http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&lang={}&APPID={}".format(city_id, lang, appid),
                          headers={ 'User-Agent': 'M5Stack'})
      data = res.json()
      name=data['name']
      conditions=data['weather'][0]['description']
      temp=str(int(data['main']['temp']))+" C°"
      if temp[0]!="-" and temp!="0": temp="+"+temp
      icon=CACHEPATH+"/{}.png".format(data['weather'][0]['icon'])
      iconURL="http://openweathermap.org/img/wn/{}.png".format(data['weather'][0]['icon'])
      if not fileExist(icon):
        try:
          res=urequests.request(method="GET", 
                                url=iconURL, 
                                headers={ 'User-Agent': 'M5Stack'})
          with open(icon, 'wb') as fb:
            fb.write(res.content) 
        except Exception as e:
          rez[0]=str(e)
          icon="/flash/res/weather/error.png"
      rez=[name,conditions,temp,icon]
      return(rez)
    except Exception as e:
      rez[0]=str(e)
      return(rez)
  return(rez)