from machine import Timer
from m5stack import power
import ubluetooth, sys, deviceCfg
from easyIO import map_value
sys.path.append("/flash/sys")
from notifications import addNotification
class ESP32_BLE():
  def showMessage(self,text):
    import lvgl as lv
    def event_close_handler(obj, event):
      if event == lv.EVENT.VALUE_CHANGED: obj.start_auto_close(0)
    btns, mbox1 = ["Close", ""], lv.msgbox(lv.scr_act())
    mbox1.set_text(text)
    mbox1.add_btns(btns)
    mbox1.set_width(280)
    mbox1.set_event_cb(event_close_handler)
    mbox1.align(None, lv.ALIGN.CENTER, 0, 0)
  
  def __init__(self,updateDr):
    self.timer0 = Timer(4)
    self.disconnected()
    self.__update_step,self.led,self.name,self.ble_msg = 0,False,"M5Stack Core2",""
    self.led_enabl,self.__addNotification,self.__updateDr,self.setPowerLED = deviceCfg.get_power_led_mode,addNotification,updateDr,power.setPowerLED
    self._connections = set()
    self.ble = ubluetooth.BLE()
    self.ble.active(True)
    self.register()
    self.ble.irq(self.ble_irq)
    self.advertiser()

  def __update__(self, Timer):
    if self.__update_step==1: self.send(self.getBatStatus())
    self.__update_step+=1
    if self.__update_step>6: self.__update_step=0
  
  def __do__(self):
    try:
      if "{t:\"notify\"" in self.ble_msg:
        mes=self.ble_msg
        from_name, body_text, metadata="","",""
        if ",id:" in mes:
          tmp=mes[mes.find(",id:")+4:]
          metadata=tmp[:tmp.find(",")]
        if ",body:\"" in mes:
          tmp=mes[mes.find(",body:\"")+7:]
          body_text=tmp[:tmp.find("\"")]
        if ",src:\"" in mes:
          tmp=mes[mes.find(",src:\"")+6:]
          from_name=tmp[:tmp.find("\"")]
        self.__addNotification(from_name, body_text, metadata)
        self.__updateDr()
    except Exception as e:
      print("gadgetbridge:{}".format(e))
  
  def setLed(self, Timer):
    if self.led_enabl():
      self.led = not self.led 
      self.setPowerLED(self.led)
    
  def connected(self):
    if self.led_enabl():
      self.led=True
      self.setPowerLED(self.led)
    self.timer0.deinit()
    self.timer0.init(period=10000, mode=Timer.PERIODIC, callback=self.__update__)

  def disconnected(self):
    self.timer0.deinit()
    self.timer0.init(period=500, mode=Timer.PERIODIC, callback=self.setLed)

  def ble_irq(self, event, data):
    if event == 1: #_IRQ_CENTRAL_CONNECT:
      conn_handle, _, _ = data
      self._connections.add(conn_handle)
      self.connected()
    elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
      conn_handle, _, _ = data
      if conn_handle in self._connections:
        self._connections.remove(conn_handle)
      self.advertiser()
      self.disconnected()
    elif event == 3: #_IRQ_GATTS_WRITE:
      conn_handle, value_handle = data
      if conn_handle in self._connections and value_handle == self.rx:
        buffer = self.ble.gatts_read(self.rx)
        buffer = buffer.decode('UTF-8').strip()
        if "GB({" in self.ble_msg and not "GB({" in buffer:
          self.ble_msg += buffer
          if "})" in buffer: self.__do__()
        else:
          self.ble_msg = buffer

  def register(self):        
    UART_UUID = ubluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
    UART_TX = (ubluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), ubluetooth.FLAG_NOTIFY,)
    UART_RX = (ubluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), ubluetooth.FLAG_WRITE,)
    UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)
    SERVICES = (UART_SERVICE,)
    ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

  def getBatStatus(self):
    chg,volt = 1 if power.getChargeState() else 0, float(power.getBatVoltage())
    return "{"+"t:\"status\", bat:{}, volt:{:.1f}, chg:{}".format(int(map_value((volt), 3.7, 4.1, 0, 100)), volt ,chg)+"}"
    
  def send(self, data):
    for conn_handle in self._connections:
      self.ble.gatts_notify(conn_handle, self.tx, "{:<127}\n".format(data))

  def advertiser(self):
    name = bytes(self.name, 'UTF-8')
    adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
    self.ble.gap_advertise(100, adv_data)