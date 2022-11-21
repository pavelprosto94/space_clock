import lvgl as lv
import deviceCfg
import machine
def event_debug_handler(obj, event):
  if event == lv.EVENT.VALUE_CHANGED:
    if obj.get_active_btn_text()==lv.SYMBOL.WIFI+" WiFi":
      deviceCfg.set_device_mode(0) # debug WiFi
      machine.reset()
    elif obj.get_active_btn_text()==lv.SYMBOL.USB+" USB":
      deviceCfg.set_device_mode(1) # debug USB
      machine.reset()
    obj.start_auto_close(0)
btns = [lv.SYMBOL.WIFI+" WiFi", lv.SYMBOL.USB+" USB", lv.SYMBOL.CLOSE+" Close", ""]
mbox1 = lv.msgbox(lv.scr_act())
mbox1.set_text("Restart device in debug mode")
mbox1.add_btns(btns)
mbox1.set_event_cb(event_debug_handler)
mbox1.align(None, lv.ALIGN.CENTER, 0, 0)