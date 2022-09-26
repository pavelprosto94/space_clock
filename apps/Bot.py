def showMessage(text):
  import lvgl as lv
  def event_close_handler(obj, event):
    if event == lv.EVENT.VALUE_CHANGED:
      obj.start_auto_close(0)
  btns = ["Close", ""]
  mbox1 = lv.msgbox(lv.scr_act())
  mbox1.set_text(text)
  mbox1.add_btns(btns)
  mbox1.set_width(280)
  mbox1.set_event_cb(event_close_handler)
  mbox1.align(None, lv.ALIGN.CENTER, 0, 0)

def BotDeamon():
  import sys
  sys.path.append("/flash/sys")
  
  def readToken():
    import nvs
    _botToken=""
    try:
      _botToken=str(nvs.read_str('telegram_bot'))
    except Exception as e:
      _botToken=""
    if _botToken=="None":
      _botToken=""
    return _botToken
  botToken=readToken()
  import utelegram, wifiCfg
  from uiflow import wait
  def get_message(message):
    from_text="Telegram"
    body_text="{}: {}".format(
      str(message['message']['from']['first_name']),
      str(message['message']['text'])
      )
    showMessage(body_text)
    print(body_text)
  print("Telegram bot starting")
  run=True
  while run:
    if wifiCfg.wlan_sta.isconnected():
      bot = utelegram.ubot(botToken)
      bot.set_default_handler(get_message) 
      print("Telegram bot run")
      showMessage("Telegram bot run")
      wait(0.01)
      try:
        bot.listen()
      except Exception as e:
        print(str(e))
        showMessage("Telegram bot error:\n"+str(e))
    wait(60*10)
    showMessage("Telegram bot restart")
    print("Telegram bot restart")
  print("Telegram bot stop")

if str(__file__) == "Deamon":
  BotDeamon() # 0xff end deamon
elif str(__file__) == "flow/m5ucloud.py" or str(__file__) == "Apps":
  import sys, time, wifiCfg, nvs
  import lvgl as lv
  from uiflow import wait
  botToken=""
  root=None
  subscreen=None
  btn1=None
  btn2=None
  btn3=None
  label_2=None
  label_st=None
  rootLoading = lv.obj()
  label = lv.label(rootLoading)
  label.set_text('Loading...')
  label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
  lv.disp_load_scr(rootLoading)
  wait(0.1)

  def readToken():
    import nvs
    global botToken
    try:
      botToken=str(nvs.read_str('telegram_bot'))
    except Exception as e:
      botToken=""
    if botToken=="None":
      botToken=""

  def BotScreen():
    global root
    global subscreen
    global btn1
    global label_st
    global btn2
    global btn3
    global label_2
    
    from m5stack import touch
    sys.path.append("/flash/sys")
    from helper import vibrating, distance
    import _thread
    
    def resetToken():
      global botToken
      btn2.set_hidden(True)
      label_reset.set_hidden(True)
      botToken=""
      label_2.set_text(botToken)
      btn2_label.set_text(" Try read token ")
      #nvs.write('telegram_bot', str(botToken))
      btn2.set_hidden(False)

    def showStat():
      if not wifiCfg.wlan_sta.isconnected():
        label_st.set_text("{} WiFi not connected".format(lv.SYMBOL.WIFI))
        btn1.set_hidden(False)
      else:
        label_st.set_text("{} Connected to:\n          {}".format(lv.SYMBOL.WIFI, str(wifiCfg._connect_ssid)))
        btn1.set_hidden(True)

    def readSDToken():
      global botToken
      sys.path.append("/flash/sys")
      from helper import fileExist
      oldbotToken=botToken
      wait(0.1)
      btn2.get_child(None).set_text(" Reading... ")
      label_reset.set_hidden(True)
      wait(0.5)
      try:
        if fileExist("/sd/bot.txt"):
          with open("/sd/bot.txt", 'r') as f:
            my_lines = f.readlines()
            botToken=my_lines[0]
      except Exception as e:
        botToken=""
      label_2.set_text(botToken)
      if botToken=="":
        btn2.set_hidden(False)
        btn2.get_child(None).set_text(" Error read ")
        wait(2)
        btn2_label.set_text(" Try read token ")
      else:
        btn2.set_hidden(True)
        label_reset.set_hidden(False)

    def showStatToken():    
      readToken()
      label_2.set_text(botToken)
      if botToken=="":
          btn2.set_hidden(False)
          btn2_label.set_text(" Try read token ")
      else:
          btn2.set_hidden(True)
          label_reset.set_hidden(False)

    def event_handler(obj,evt):
      if evt == lv.EVENT.CLICKED:
        if str(type(obj)) == "<class 'btn'>":
          if obj == btn1:
            _thread.start_new_thread(autoConnect,())
          elif obj == btn2:
            _thread.start_new_thread(readSDToken,())
          else:
            l=obj.get_child(None).get_text()
            if l=="?":
              showMessage("You can read more about\nhow to set up a bot on GitHub.\nhttps://github.com/pavelprosto94/space_clock")
            elif l=="Add to boot":
              _thread.start_new_thread(addToDeamon,())
            elif l=="Remove from boot":
              _thread.start_new_thread(removeFromDeamon,())
              
    def autoConnect():
      wait(0.1)
      btn1.get_child(None).set_text(" Connect... ")
      wifiCfg.autoConnect()
      wait(0.5)
      btn1.get_child(None).set_text(" Try autoConnect ")
      lv.disp_load_scr(root)
      showStat()
    
    def removeFromDeamon():
      sys.path.append("/flash/sys")
      from helper import fileExist
      btn3.set_hidden(True)
      wait(0.1)
      vibrating()
      my_lines=[]
      try:
        if fileExist("/flash/deamon.py"):
          with open("/flash/deamon.py", 'r') as f:
            my_lines = f.readlines()
      except Exception as e:
        label.set_text(str(e))
        label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
        lv.disp_load_scr(rootLoading)
      try:
        my_lines.remove("/flash/apps/Bot.py\n")
      except Exception as e:
        pass
      with open("/flash/deamon.py", 'w') as f: 
        for l in my_lines:
          if l!="" and l!="\n":
            f.write(l)
      checkDeamon()

    def addToDeamon():
      sys.path.append("/flash/sys")
      from helper import fileExist
      btn3.set_hidden(True)
      wait(0.1)
      vibrating()
      my_lines=[]
      try:
        if fileExist("/flash/deamon.py"):
          with open("/flash/deamon.py", 'r') as f:
            my_lines = f.readlines()
        with open("/flash/deamon.py", 'w') as f: 
            for l in my_lines:
              if l!="" and l!="\n":
                f.write(l)
            f.write("/flash/apps/Bot.py\n")
      except Exception as e:
        label.set_text(str(e))
        label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
        lv.disp_load_scr(rootLoading)
      checkDeamon()

    def checkDeamon():
      sys.path.append("/flash/sys")
      from helper import fileExist
      ans=False
      try:
        if fileExist("/flash/deamon.py"):
          with open("/flash/deamon.py", 'r') as f:
            my_lines = f.readlines()
            for l in my_lines:
              if l == "/flash/apps/Bot.py\n":
                ans=True
                break
      except Exception as e:
        ans=False
      if ans:
        btn3_label.set_text("Remove from boot")
      else:
        btn3_label.set_text("Add to boot")
      btn3.set_hidden(False)

    root = lv.obj()
    label_shadow_style = lv.style_t()
    label_shadow_style.init()
    label_shadow_style.set_text_color(lv.STATE.DEFAULT, lv.color_hex(0xd84949))
    label_close = lv.label(root)
    label_close.set_pos(240,220)
    label_close.add_style(lv.label.PART.MAIN, label_shadow_style)
    label_close.set_text(lv.SYMBOL.CLOSE+" close")
    label_reset = lv.label(root)
    label_reset.set_pos(5,220)
    label_reset.add_style(lv.label.PART.MAIN, label_shadow_style)
    label_reset.set_text(lv.SYMBOL.TRASH+" reset token")
    label_reset.set_hidden(True)
    label_save = lv.label(root)
    label_save.set_pos(110,220)
    label_save.add_style(lv.label.PART.MAIN, label_shadow_style)
    label_save.set_text(lv.SYMBOL.SAVE+" save and reset")
    label_st = lv.label(root)
    label_st.set_style_local_text_font(0,0,lv.font_montserrat_18)
    label_st.set_pos(5,5)
    label_st.set_text("init...")
    btn1 = lv.btn(root,None)
    btn1.set_event_cb(event_handler)
    btn1_label=lv.label(btn1,None)
    btn1_label.set_text(" Try autoConnect ")
    btn1.align(None,lv.ALIGN.IN_TOP_MID,0,30)
    showStat()
    label_1 = lv.label(root)
    label_1.set_style_local_text_font(0,0,lv.font_montserrat_18)
    label_1.set_pos(5,75)
    label_1.set_text("{} Telegram Bot Token:".format(lv.SYMBOL.SETTINGS))
    btn4 = lv.btn(root,None)
    btn4.set_event_cb(event_handler)
    btn4_label=lv.label(btn4,None)
    btn4_label.set_text("?")
    btn4.set_size(32,32)
    btn4.align(label_1,lv.ALIGN.OUT_RIGHT_BOTTOM,5,5)
    label_2 = lv.label(root)
    label_2.set_style_local_text_font(0,0,lv.font_montserrat_14)
    label_2.set_pos(5,105)
    label_2.set_text("")
    btn2 = lv.btn(root,None)
    btn2.set_event_cb(event_handler)
    btn2_label=lv.label(btn2,None)
    btn2_label.set_text(" Try read token ")
    btn2.align(None,lv.ALIGN.IN_TOP_MID,0,100)
    btn2.set_hidden(True)
    showStatToken()
    label_3 = lv.label(root)
    label_3.set_style_local_text_font(0,0,lv.font_montserrat_18)
    label_3.set_pos(5,145)
    label_3.set_text("{} Starting on boot:".format(lv.SYMBOL.CHARGE))
    btn3 = lv.btn(root,None)
    btn3.set_event_cb(event_handler)
    btn3_label=lv.label(btn3,None)
    btn3_label.set_text("Add to boot")
    btn3.set_size(160,42)
    btn3.align(None,lv.ALIGN.IN_TOP_MID,0,170)
    btn3.set_hidden(True)
    checkDeamon()
    lv.disp_load_scr(root)
    vibrating()
    run=True
    touched_time = 0
    touched_cord = None
    while run:
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
                  run=False
                elif (touch.read()[0])<215 and (touch.read()[0])>115:
                  if label_save.is_visible():
                    nvs.write('telegram_bot', str(botToken))
                    label.set_text('RESET DEVICE')
                    label.align(rootLoading,lv.ALIGN.CENTER, 0, 0)
                    lv.disp_load_scr(rootLoading)
                    run=False
                    wait(1)
                    import machine
                    machine.reset()
                elif (touch.read()[0])<105 and (touch.read()[0])>5:
                  if label_reset.is_visible():
                    vibrating()
                    resetToken()
      else:
        touched_time=0
      wait(0.2)
    vibrating()
  
  BotScreen()
  label.set_text('')
  lv.disp_load_scr(rootLoading)