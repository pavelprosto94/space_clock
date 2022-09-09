from m5stack import *
from m5stack_ui import *
from uiflow import *

url="https://api.github.com/repos/pavelprosto94/uHome/git/trees/master?recursive=1"

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

image0 = M5Img("img/wifi_config_ap_connect.png", x=110, y=47, parent=None)
label0 = M5Label('Check wifi connection.', x=78, y=193, color=0x000, font=FONT_MONT_14, parent=None)
bar0 = M5Bar(x=64, y=164, w=192, h=12, min=0, max=100, bg_c=0xa0a0a0, color=0x08A2B0, parent=None)


#image0.set_network_img_src('')