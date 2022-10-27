import lvgl as lv
from m5stack import touch
import sys
sys.path.append("/flash/sys")
def AboutScreen():
  root = lv.obj()
  img = lv.img(root)
  with open("/flash/res/space_clock/cosmonaut_0.png",'rb') as f: data = f.read()
  img_dsc = lv.img_dsc_t({'data_size': len(data),'data': data })
  img.set_src(img_dsc)
  img.set_pos(110,20)
  lbl=lv.label(root)
  lbl.set_text('Space clock')
  lbl.set_pos(95,129)
  lbl.set_style_local_text_font(0,0,lv.font_montserrat_22)
  lbl.set_style_local_text_color(0,0,lv.color_hex(0x000))
  lbl=lv.label(root)
  lbl.set_text('v1.5.0')
  lbl.set_pos(225, 129)
  lbl.set_style_local_text_font(0,0,lv.font_montserrat_14)
  lbl.set_style_local_text_color(0,0,lv.color_hex(0x0288fb))
  lbl=lv.label(root)
  lbl.set_text('Created by Pavel Prosto')
  lbl.set_pos(75, 158)
  lbl.set_style_local_text_font(0,0,lv.font_montserrat_14)
  lbl.set_style_local_text_color(0,0,lv.color_hex(0x000))
  lbl=lv.label(root)
  lbl.set_text('https://github.com/pavelprosto94/space_clock')
  lbl.set_pos(40, 182)
  lbl.set_style_local_text_font(0,0,lv.font_montserrat_10)
  lbl.set_style_local_text_color(0,0,lv.color_hex(0x034c76))
  label_cl = lv.label(root)
  label_cl.set_pos(238,220)
  label_cl.set_style_local_text_font(0,0,lv.font_montserrat_14)
  label_cl.set_style_local_text_color(0,0,lv.color_hex(0xd84949))
  label_cl.set_text(lv.SYMBOL.CLOSE+" close")
  lv.disp_load_scr(root)
  run=True
  touched_time=1
  while run:
    if touch.status():
      if touched_time==0:
        if (touch.read()[1]) > 240:
          touched_time=1
          run=False
    else:
      if touched_time>0:
        touched_time=0
  return root