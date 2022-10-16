from m5stack import touch,lv
from uiflow import wait
import os, sys, time, deviceCfg, _thread, machine
sys.path.append("/flash/sys")
from helper import vibrating, distance, fileExist
if not 'body_font' in dir(): body_font=lv.font_montserrat_14
if not 'title_font' in dir(): title_font=lv.font_montserrat_18
def loadPNG(path):
  with open(path,'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  return img_dsc
def event_slider_handler(obj,evt):
  if evt == lv.EVENT.VALUE_CHANGED:
    if obj==sw1:
      for l in arr_hide:
        l.set_hidden(not st_sw1==obj.get_state())
      btn1.set_hidden(st_sw1==obj.get_state())
    elif obj==sw2:
      deviceCfg.set_power_led(obj.get_state())
def applyAndRestart():
  btn1.set_hidden(True)
  wait(0.1)
  if st_sw1:
    with open("/flash/deamon.py", 'r') as file :
      filedata = file.read()
    filedata = filedata.replace("from gadgetbridge import ESP32_BLE\nESP32_BLE(NotifyUpdate)\n", "")
    with open("/flash/deamon.py", 'w') as file:
      file.write(filedata)
  else:
    with open("/flash/deamon.py", "a") as file_object:
      file_object.write("from gadgetbridge import ESP32_BLE\nESP32_BLE(NotifyUpdate)\n")
  machine.reset()
def event_handler(obj,evt):
  if evt == lv.EVENT.CLICKED:
    _thread.start_new_thread(applyAndRestart,()) 
root,label_shadow_style,arr_hide = lv.obj(),lv.style_t(),[]
root.set_style_local_text_font(0,0,body_font)
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
page,label_close = lv.page(root),lv.label(root)
label_close.set_pos(238,220)
label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
label_close.set_text(lv.SYMBOL.CLOSE+" close")
page.set_size(320,215)
page.set_click(False)
label,sw1,sw2=lv.label(page,None),lv.switch(page, None),lv.switch(page, None)
label.set_text('Enable Bluetooth service:')
label.set_pos(0, 10)
sw1.set_pos(230, 5)
sw1.set_event_cb(event_slider_handler)
st_sw1="from gadgetbridge import ESP32_BLE\nESP32_BLE(NotifyUpdate)\n" in open("/flash/deamon.py","r").read()
label=lv.label(page,None)
label.set_text('Bluetooth LED indicator:')
label.set_pos(0, 45)
sw2.set_pos(230, 40)
sw2.set_event_cb(event_slider_handler)
btn1 = lv.btn(page,None)
btn1.set_event_cb(event_handler)
btn1.set_pos(20, 90)
btn1.set_size(255,35)
label=lv.label(btn1,None)
label.set_text(lv.SYMBOL.REFRESH+'Apply and Restart')
btn1.set_hidden(True)
if deviceCfg.get_power_led_mode():
  sw2.on(lv.ANIM.OFF)
if st_sw1:
  sw1.on(lv.ANIM.OFF)
  label,label1,lbl,lbl1,qr0,qr1=lv.label(page),lv.label(page),lv.label(page),lv.label(page),lv.img(page),lv.img(page)
  arr_hide=[label,label1,lbl,lbl1,qr0,qr1]
  label.set_pos(0, 80)
  label.set_recolor(True)
  label.set_long_mode(lv.label.LONG.BREAK)
  label.set_text('Use {}08a2b0 Gadgetbridge{} to link your device and receive notifications.\nGet it on {}08a2b0 F-Droid{}:'.format(chr(35),chr(35),chr(35),chr(35)))
  label.set_width(lv.page.get_width_fit(page))
  qr0.set_src(loadPNG("res/qrcode1.png"))
  qr0.set_pos(60,130)
  lbl.set_pos(0, 285)
  lbl.set_long_mode(lv.label.LONG.BREAK)
  lbl.set_style_local_text_font(0,0,lv.font_montserrat_10)
  lbl.set_style_local_text_color(0,0,lv.color_hex(0x034c76))
  lbl.set_text('https://f-droid.org/en/packages/nodomain.freeyourgadget.gadgetbridge')
  lbl.set_width(lv.page.get_width_fit(page))
  label1.set_pos(0, 320)
  label1.set_recolor(True)
  label1.set_long_mode(lv.label.LONG.BREAK)
  label1.set_text('You can learn more about how to set up {}08a2b0 Bluetooth notifications{} on the project\'s {}08a2b0 github{}:'.format(chr(35),chr(35),chr(35),chr(35)))
  label1.set_width(lv.page.get_width_fit(page))
  qr1.set_src(loadPNG("res/qrcode2.png"))
  qr1.set_pos(60,370)
  lbl1.set_pos(0, 525)
  lbl1.set_long_mode(lv.label.LONG.BREAK)
  lbl1.set_style_local_text_font(0,0,lv.font_montserrat_10)
  lbl1.set_style_local_text_color(0,0,lv.color_hex(0x034c76))
  lbl1.set_text('https://github.com/pavelprosto94/space_clock')
  lbl1.set_width(lv.page.get_width_fit(page))
else:
  label=lv.label(page)
  arr_hide=[label]
  label.set_pos(0, 80)
  label.set_recolor(True)
  label.set_long_mode(lv.label.LONG.BREAK)
  label.set_text('Using this service, you will be able to connect your {}08a2b0 M5Stack{} via {}08a2b0 Bluetooth{} and receive notifications on it.'.format(chr(35),chr(35),chr(35),chr(35)))
  label.set_width(lv.page.get_width_fit(page))
lv.disp_load_scr(root)

run,touched_time,touched_cord=True,0,[0,0]
while run:
  if touch.status():
    if touched_time==0: touched_time,touched_cord=time.ticks_ms(),touch.read()
    elif (touch.read()[1]) > 240:
      if touched_time!=-1:
        if time.ticks_ms()-touched_time>250:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[0])<315 and (touch.read()[0])>225:
              vibrating()
              run=False
  elif touched_time!=0: touched_time=0
  wait(0.1)