try:
  if str(__file__) == "menu/app.py":
    import machine
    fileA = open('/flash/apps/apps_explorer.py', 'rb')
    fileB = open('/flash/main.py', 'wb')
    fileB.write(fileA.read())
    fileA.close()
    fileB.close()
    machine.reset()
except Exception as e:
  print("run list apps")
from m5stack import touch, lv
rootLoading = lv.obj()
label = lv.label(rootLoading)
label.align(rootLoading,lv.ALIGN.CENTER, -20, 0)
label.set_text('Loading...')
lv.disp_load_scr(rootLoading)
from uiflow import wait
wait(0.01)
if not 'body_font' in dir():
  body_font=lv.font_montserrat_14
if not 'title_font' in dir():
  title_font=lv.font_montserrat_18
import os, sys, time
sys.path.append("/flash/sys")
from helper import vibrating, distance, fileExist
root = lv.obj()
root.set_style_local_text_font(0,0,body_font)
label_shadow_style = lv.style_t()
label_shadow_style.init()
label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
label_close = lv.label(root)
label_close.set_pos(238,220)
label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
label_close.set_text(lv.SYMBOL.CLOSE+" close")
ind_run=-1
page = lv.page(root,None)
page.set_size(320,220)
apps=os.listdir("/flash/apps")
ignore=["_clock","apps_explorer"]
for l in ignore:
  i=0
  while i<len(apps):
    if l in apps[i]: apps.pop(i)
    i+=1 
for i,l in enumerate(apps):
  app_icon="/flash/res/programm.png"
  if fileExist("/flash/res/{}.png".format(l)):
    app_icon="/flash/res/{}.png".format(l)
  img = lv.img(page)
  img.set_pos(3+74*(i%4),5+int(i/4)*94)
  with open(app_icon,'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  img.set_src(img_dsc)
  lbl = lv.label(page)
  lbl.set_hidden(True)
  lbl.set_pos(3+74*(i%4),74+int(i/4)*94)
  lbl.set_long_mode(lv.label.LONG.SROLL_CIRC)
  lbl.set_align(lv.label.ALIGN.CENTER)
  lbl.set_hidden(False)
  txt=l[:l.rfind(".")]
  if "_explorer" in txt:
    txt=txt[:txt.rfind("_explorer")]
  lbl.set_text(txt)
  lbl.set_size(64,18)
lv.disp_load_scr(root)
run=True
touched_time = 0
touched_cord = [0,0]
protect_mode=False
while run:
  if ind_run>-1:
    lv.disp_load_scr(rootLoading)
    wait(0.01)
    vibrating()
    if apps[ind_run]=="Alarm_explorer.py":
      sys.path.append("/flash/apps")
      from Alarm_explorer import alarmExplorer
      subscreen=alarmExplorer(None)
      lv.disp_load_scr(root)
      subscreen.delete()
    elif apps[ind_run]=="Notify_explorer.py":
      sys.path.append("/flash/apps")
      from Notify_explorer import notificationsExplorer
      subscreen=notificationsExplorer()
      lv.disp_load_scr(root)
      subscreen.delete()
    else:
      fdata = open("/flash/apps/{}".format(apps[ind_run]), 'r')
      data=fdata.read()
      fdata.close()
      if not "while run:" in data:
        protect_mode=True
        label_close.set_parent(rootLoading)
      try:
        exec(data,{"__file__":"Apps",'body_font':body_font, 'title_font':title_font})
      except Exception as e:
        rootLoading = lv.obj()
        label = lv.label(rootLoading)
        label.set_text(str(e))
        label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
        lv.disp_load_scr(rootLoading)
    if not protect_mode:
      lv.disp_load_scr(root)
    ind_run=-1
  elif touch.status():
    if touched_time==0:
      touched_time=time.ticks_ms()
      touched_cord = touch.read()
    if (touch.read()[1]) > 240:
      if touched_time!=-1:
        if time.ticks_ms()-touched_time>500:
          if distance(touched_cord,touch.read())<3:
            touched_time=-1
            if (touch.read()[0])<315 and (touch.read()[0])>225:
              vibrating()
              if not protect_mode:
                run=False
              else:
                protect_mode=False
                rootLoading = lv.obj()
                label = lv.label(rootLoading)
                label.set_text('Loading...')
                label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
                label_close = lv.label(root)
                label_close.set_pos(238,220)
                label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
                label_close.set_text(lv.SYMBOL.CLOSE+" close")
                lv.disp_load_scr(root)
  else:
    if touched_time!=0:
      if distance(touched_cord,touch.read())<5:
        ind_run=int((touched_cord[0]-3)/74)
        if ind_run>=0:
          ind_run+=int((touched_cord[1]-page.get_scrollable().get_y()-5)/94)*4
        if ind_run>=len(apps):
          ind_run=-1
      touched_time=0
  wait(0.1)
label.set_text('')
lv.disp_load_scr(rootLoading)