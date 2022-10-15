from m5stack import lv, touch
import _thread
class SliderTime():
  def __init__(self,parent,x=0,y=0,start_value=0,max_value=10,val_font=lv.font_montserrat_18,sub_font=lv.font_montserrat_14, onValueChange=None):
    self.__root = lv.obj(parent)
    self.__root.set_hidden(True)
    self.__root.set_pos(0,y)
    self.__root.set_width(parent.get_width())
    self.__root.set_event_cb(self.event_handler)
    self.__root.set_style_local_text_color(0,0,lv.color_hex(0x788290))
    self.__root.set_style_local_text_font(0,0,sub_font)
    self.value,self.__num_max,self.__freeze,self.__numbo,self.__numbx,self.__numbi,self.__numbv,self.__old_x=start_value,max_value,False,[],[],[],[],-1
    self.__lbl_val=lv.label(self.__root)
    self.__lbl_val.set_style_local_text_color(0,0,lv.color_hex(0x000000))
    self.__lbl_val.set_style_local_text_font(0,0,val_font)
    self.__lbl_val.set_text(str("{:02d}").format(self.value))
    self.__ws=self.__lbl_val.get_width()
    pws,hs,col_el=self.__root.get_width(),self.__lbl_val.get_height(),int((parent.get_width())/int(self.__ws*1.5))
    self.__root.set_height(hs+16)
    self.__cache_ofs_w,cache_ofs_h=None,None
    if col_el%2==0: col_el-=1
    for i in range(0,col_el):
      self.__numbo.append(lv.label(self.__root, None))
      self.__numbo[-1].set_long_mode(lv.label.LONG.BREAK)
      tmp_val=self.value+(i-int(col_el/2))
      if tmp_val<0: tmp_val=self.__num_max+tmp_val+1
      elif tmp_val>self.__num_max: tmp_val=tmp_val-self.__num_max-1
      self.__numbi.append(tmp_val)
      self.__numbo[-1].set_text(str("{:02d}").format(tmp_val))
      if self.__cache_ofs_w==None: 
        self.__cache_ofs_w=int((self.__numbo[-1].get_width()-self.__ws)/2)
        self.__cache_ofs_w=int((pws-(int(self.__ws*1.5)*(col_el)+self.__cache_ofs_w)+self.__numbo[-1].get_width())/2)
      if cache_ofs_h==None: cache_ofs_h=int((hs-self.__numbo[-1].get_height())/2)
      self.__numbx.append(int(self.__ws*1.5)*i)
      self.__numbo[-1].set_pos(self.__numbx[-1]+self.__cache_ofs_w,cache_ofs_h+8)
      self.__numbv.append(i!=int(col_el/2))
      self.__numbo[-1].set_hidden(not self.__numbv[-1])
    self.__lbl_val.set_pos(int(self.__ws*1.5)*int(col_el/2)+self.__cache_ofs_w-int((self.__numbo[-1].get_width()-self.__ws)/2),8)
    self.__onValueChange=onValueChange
    self.__root.set_hidden(False)

  def __reDraw(self):
    self.__freeze=True
    alfa_x=touch.read()[0]-self.__old_x
    self.__old_x=touch.read()[0]
    for i in range(0,len(self.__numbo)):
      new_x,vec=self.__numbx[i]+alfa_x,0
      while new_x<-self.__cache_ofs_w/2:
        new_x+=int(self.__ws*1.5)*len(self.__numbo)
        vec=+1
      while new_x>int(self.__ws*1.5)*len(self.__numbo)-self.__cache_ofs_w/2:
        new_x-=int(self.__ws*1.5)*len(self.__numbo)
        vec=-1
      self.__numbx[i]=new_x
      self.__numbo[i].set_x(self.__numbx[i]+self.__cache_ofs_w)
      if vec!=0:
        ind=i-vec
        if ind>=len(self.__numbo): ind=0
        elif ind<0: ind=len(self.__numbo)-1
        self.__numbi[i]=self.__numbi[ind]+vec
        if self.__numbi[i]<0: self.__numbi[i]=self.__num_max
        elif self.__numbi[i]>self.__num_max: self.__numbi[i]=0
        self.__numbo[i].set_text(str("{:02d}").format(self.__numbi[i]))
      self.__numbv[i]=new_x>self.__lbl_val.get_x()-self.__cache_ofs_w*1.25 and new_x<(self.__lbl_val.get_x()+self.__ws)-self.__cache_ofs_w
      self.__numbo[i].set_hidden(self.__numbv[i])
      if (self.__numbv[i]):
        self.value=self.__numbi[i]
        self.__lbl_val.set_text(str("{:02d}").format(self.value))
    if self.__old_x!=-1: self.__freeze=False
    else: self.__finalDraw()
  
  def __finalDraw(self):
    self.__freeze=True
    for i in range(0,len(self.__numbo)):
      tmp_val=self.value+(i-int(len(self.__numbo)/2))
      if tmp_val<0: tmp_val=self.__num_max+tmp_val+1
      elif tmp_val>self.__num_max: tmp_val=tmp_val-self.__num_max-1
      self.__numbo[i].set_text(str("{:02d}").format(tmp_val))
      self.__numbx[i]=int(self.__ws*1.5)*i
      self.__numbo[i].set_x(self.__numbx[i]+self.__cache_ofs_w)
      self.__numbi[i]=tmp_val
      self.__numbv[i]=(i != int(len(self.__numbo)/2))
      self.__numbo[i].set_hidden(not self.__numbv[i])
    self.__freeze=False
    if self.__onValueChange!=None: self.__onValueChange(self.value)
  
  def set_pos(self,x,y):
    self.__root.set_pos(0,y)
  
  def set_hidden(self,v):
    self.__root.set_hidden(v)
    
  def event_handler(self,obj,evt):
    if evt==lv.EVENT.PRESSED:
      self.__old_x=touch.read()[0]
    elif evt==lv.EVENT.PRESSING:
      if not self.__freeze:
        _thread.start_new_thread(self.__reDraw,())
    elif evt==lv.EVENT.RELEASED or evt==lv.EVENT.DEFOCUSED:
      if self.__old_x!=-1:
        self.__old_x=-1
        if not self.__freeze:
          _thread.start_new_thread(self.__finalDraw,())