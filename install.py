from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg, _thread, urequests, base64, os

def mkDir(path):
  try:
    os.mkdir("/flash/"+path[:path.find("/")+1])
  except Exception as e: 
    return ""
  return "/flash/"+path[:path.find("/")+1]

url="https://api.github.com/repos/pavelprosto94/space_clock/git/trees/main?recursive=1"
animation_enable = -1

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

M5Img("img/setup_bar_320_40.png", x=0, y=0, parent=None)
image0 = M5Img("img/wifi_config_ap_connect.png", x=128, y=64, parent=None)
label0 = M5Label('Checking Wi-Fi connection.', x=10, y=165, color=0x000, font=FONT_MONT_14, parent=None)
label1 = M5Label('', x=10, y=194, color=0xff0000, font=FONT_MONT_14, parent=None)
bar0 = M5Bar(x=64, y=145, w=192, h=12, min=0, max=100, bg_c=0xa0a0a0, color=0x08A2B0, parent=None)
if not wifiCfg.wlan_sta.isconnected():
  wait(0.5)
  screen0 = screen.get_act_screen()
  wait(0.5)
  wifiCfg.autoConnect()
  wait(1)
  screen.load_screen(screen0)

if wifiCfg.wlan_sta.isconnected():
  image0.set_network_img_src("https://raw.githubusercontent.com/pavelprosto94/space_clock/main/resources/install_download.png")
  label0.set_text("Initialization")
  def playAlarm():
    global animation_enable
    img=[]
    for i in range(0,3):
      img.append(M5Img("https://raw.githubusercontent.com/pavelprosto94/space_clock/main/resources/install_download_pr_{}.png".format(i), x=128, y=64, parent=None))
    wait(0.1)
    animation_enable = 3
    while animation_enable>-1:
      if animation_enable < 3:
        img[animation_enable].set_hidden(False)
        animation_enable+=1
      elif animation_enable<6:
        img[animation_enable-6].set_hidden(True)
        animation_enable+=1
      else:
        animation_enable=0
      wait(1)       
        
  _thread.start_new_thread(playAlarm,())
  while animation_enable==-1:
    wait(1)
  installing=False
  label0.set_text("Connecting to git...")
  try:
    ignore=[
      "README.md"
    ]
    data = urequests.request(method="GET", url=url, headers={ 'User-Agent': 'M5Stack'})
    data = data.json()
    if not "tree" in data:
      if "message" in data:
        label0.set_text(str(data["message"]))
      else:
        label0.set_text("Error 0")
    else:  
      for d in data["tree"]:
        if d["type"]=="blob":
          path=d["path"]
          if not path in ignore and path[0]!="." and path[:path.find("/")]!="resources":
            label0.set_text("Writing...\n{}".format(path))
            file_d = urequests.request(method="GET", url=d["url"], headers={ 'User-Agent': 'M5Stack'})
            file_d = file_d.json()
            if "/" in path:
              ans=mkDir(path)
              if ans!="":
                label0.set_text("Made path:\n{}".format(ans))
            file_str=file_d["content"]
            file_bytes = base64.b64decode(file_str)
            with open("/flash/"+path, 'wb') as f:
              f.write(file_bytes) 
            wait(0.1)
      installing=True
  except Exception as e: 
    label1.set_text(str(e))
  else:
    if installing:
      label0.set_text("Installation is complete\nRestart your device \nand run space_clock.py app")
  animation_enable = -1
else:
  image0.set_img_src("img/wifi_config_sta_fail.png")
  label0.set_text("No connection to Wi-Fi.\nRestart your device and try again")