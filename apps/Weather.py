try:
  if str(__file__) == "menu/app.py":
    import machine
    fileA = open('/flash/apps/Weather.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    machine.reset()
except Exception as e:
  print("run weather")
import lvgl as lv
rootLoading = lv.obj()
label = lv.label(rootLoading)
label.align(rootLoading,lv.ALIGN.CENTER, -20, 0)
label.set_text('Loading...')
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
from m5stack import touch
import os, sys, time, wifiCfg, _thread, json
sys.path.append("/flash/sys")
import weather
from helper import vibrating, distance
if not wifiCfg.wlan_sta.isconnected():
  wifiCfg.autoConnect()
  wait(0.5)

def saveWeather():
  data = {}
  if ('weather.txt' in os.listdir('/flash')):
    with open('/flash/weather.txt', 'r') as json_file:
      data = json.load(json_file)
  data['weather'] = {'city' : w_city}
  with open('/flash/weather.txt', 'w') as outfile:
    json.dump(data, outfile)

def event_handler(obj, event):
  global subscreen
  global w_city
  if event == lv.EVENT.CLICKED:
    list_btn = lv.list.__cast__(obj)
    otv=list_btn.get_btn_text()
    if "[" in otv:
      otv=otv[otv.rfind("[")+1:otv.rfind("]")]
      w_city=int(otv)
      label_c.set_text("Loading...")
      _thread.start_new_thread(getWeatherSc,())
      vibrating()
      lv.disp_load_scr(root)
      subscreen.delete()
      subscreen=None

def loadCity(city_sch):
  global run
  try:
    if city_sch!="":
      otv=weather.SeachCity(city_sch)
      if len(otv)==0:
        otv=["City not found"]
      for l in otv:
        btn_new=list_f.add_btn(lv.SYMBOL.GPS,l)
        btn_new.set_event_cb(event_handler)
    vibrating()
  except Exception as e: 
    run=False
    label.set_pos(0,0)
    label.set_text(str(e))
    lv.disp_load_scr(rootLoading)
  
def event_keybHandler(obj, event):
  obj.def_event_cb(event)
  if event == lv.EVENT.CANCEL:
    keyb.set_hidden(True)
    list_f.set_hidden(False)
  elif event == lv.EVENT.APPLY:
    city_sch=str(obj.get_textarea().get_text())
    keyb.set_hidden(True)
    try:
      list_f.clean()
    except Exception as e: 
      pass
    list_f.set_hidden(False)
    _thread.start_new_thread(loadCity,(city_sch, ))
   
def event_handler_hiden(obj,evt):
  if evt == lv.EVENT.CLICKED:
    keyb.set_hidden(False)
    list_f.set_hidden(True)

keyb=None
list_f=None
def showKeyb():
  global subscreen
  global keyb
  global list_f
  subscreen=lv.obj()
  lbl = lv.label(subscreen)
  lbl.set_pos(10,5)
  lbl.set_text("Enter city name:")
  label_cl = lv.label(subscreen)
  label_cl.set_pos(238,220)
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
  list_f = lv.list(subscreen)
  list_f.set_size(320, 150)
  list_f.set_pos(0,65)
  list_f.set_hidden(True)
  ta=lv.textarea(subscreen,None)
  ta.set_accepted_chars("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_- ")
  ta.set_size(300,35)
  ta.set_pos(10,22)
  ta.set_text("")
  ta.set_event_cb(event_handler_hiden)
  keyb = lv.keyboard(subscreen,None)
  keyb.set_cursor_manage(True)
  keyb.set_event_cb(event_keybHandler)
  keyb.set_textarea(ta)
  keyb.set_pos(0,70)
  keyb.set_size(320,170)
  lv.disp_load_scr(subscreen)

def getWeatherSc():
  w_data=weather.GetForecastWeather(w_city)
  label_c.set_text(w_data[0])
  label_s.set_text(w_data[1])
  label_t.set_text(w_data[2])
  img_w.set_src(openPNG(w_data[3]))
  label_d.set_text(w_data[4][:w_data[4].rfind(":")])
  label2_s.set_text(w_data[5])
  label2_t.set_text(w_data[6])
  img2_w.set_src(openPNG(w_data[7]))
  label2_d.set_text(w_data[8][:w_data[7].rfind(":")])
  if w_city==-1:
    label_sub.set_text(lv.SYMBOL.PLUS+" add")
    label_sub.set_pos(130,220)
  else:
    label_sub.set_text(lv.SYMBOL.LOOP+" change")
    label_sub.set_pos(120,220)
    vibrating()

w_city=weather.getCity()                     
root = lv.obj()
subscreen=None
def openPNG(path):
  with open(path,'rb') as f: data = f.read()
  return lv.img_dsc_t({'data_size': len(data),'data': data })
img_logo = lv.img(root)
img_logo.set_pos(5,5)
img_logo.set_src(openPNG("/flash/res/weather/openweathermap_logo.png"))
label_shadow_style = lv.style_t()
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
label_cl = lv.label(root)
label_cl.set_pos(238,220)
label_cl.add_style(lv.label.PART.MAIN, label_shadow_style)
label_cl.set_text(lv.SYMBOL.CLOSE+" close")
label_sub = lv.label(root)
label_sub.add_style(lv.label.PART.MAIN, label_shadow_style)
label_sub.set_text("")
page = lv.obj(root)
page.set_pos(0,60)
page.set_style_local_text_color(0,0,lv.color_hex(0xa0a0a0))
page.set_style_local_bg_color(0,0,lv.color_hex(0x48484a))
page.set_size(320,150)
label_c = lv.label(page)
label_c.set_pos(25,20)
label_c.set_style_local_text_font(0,0,lv.font_montserrat_26)
label_c.set_text("Loading...")
img_w = lv.img(page)
img_w.set_pos(25,50)
img_w.set_src(openPNG("/flash/res/weather/error.png"))
label_t = lv.label(page)
label_t.set_pos(80,65)
label_t.set_style_local_text_font(0,0,lv.font_montserrat_18)
label_t.set_text("?")
label_s = lv.label(page)
label_s.set_pos(25,90)
label_s.set_style_local_text_font(0,0,lv.font_montserrat_18)
label_s.set_text("")
label_d = lv.label(page)
label_d.set_text("")
label_d.set_pos(25,120)
label_d.set_style_local_text_font(0,0,lv.font_montserrat_14)
label_d.set_style_local_text_color(0,0,lv.color_hex(0x909090))
img2_w = lv.img(page)
img2_w.set_pos(25+140,50)
img2_w.set_src(openPNG("/flash/res/weather/error.png"))
label2_t = lv.label(page)
label2_t.set_pos(80+140,65)
label2_t.set_style_local_text_font(0,0,lv.font_montserrat_18)
label2_t.set_text("?")
label2_s = lv.label(page)
label2_s.set_pos(25+140,90)
label2_s.set_style_local_text_font(0,0,lv.font_montserrat_18)
label2_s.set_text("")
label2_d = lv.label(page)
label2_d.set_text("")
label2_d.set_pos(25+140,120)
label2_d.set_style_local_text_font(0,0,lv.font_montserrat_14)
label2_d.set_style_local_text_color(0,0,lv.color_hex(0x909090))
lv.disp_load_scr(root)
_thread.start_new_thread(getWeatherSc,())
vibrating()
run=True
touched_time = 0
touched_cord = None
label.set_text('')
while run:
  try:
    if touch.status():
      if (touch.read()[1]) > 230:
        if touched_time==0:
          touched_time=time.ticks_ms()
          touched_cord = touch.read()
        elif touched_time!=-1:
          if time.ticks_ms()-touched_time>500:
            if distance(touched_cord,touch.read())<3:
              touched_time=-1
              if (touch.read()[0])<315 and (touch.read()[0])>225:
                if subscreen!=None:
                  if not keyb.is_visible():
                    vibrating()
                    lv.disp_load_scr(root)
                    subscreen.delete()
                    subscreen=None
                else:
                  vibrating()
                  run=False
              elif (touch.read()[0])<215 and (touch.read()[0])>115:
                if subscreen==None:
                  vibrating()
                  showKeyb()
    else:
      touched_time=0
    wait(0.2)
  except Exception as e: 
    run=False
    label.set_pos(0,0)
    label.set_text(str(e))
    lv.disp_load_scr(rootLoading)
saveWeather()
lv.disp_load_scr(rootLoading)