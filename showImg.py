__author__ = 'yem'

from tkinter import *
from PIL import ImageTk
from PIL import Image
from PIL.ExifTags import TAGS
import os
import math
import mimetypes
import sys


FILE_FILTER = [".jpg",".png",".jpeg",".bmp",".gif",".JPG"]



from tkinter.filedialog import askdirectory

import tkinter

def makeThumbs(imgdir,size=(100,100),subdir='thumbs',offset = 0,nums = 0):

    thumdir = os.path.join(imgdir,subdir)

    if not os.path.exists(thumdir):
        os.makedirs(thumdir)

    thumbs = []

    for imgfile in os.listdir(imgdir):

        name,ext = os.path.splitext(imgfile)

        if ext not in FILE_FILTER:
            continue

        thumbpath = os.path.join(thumdir,imgfile)

        if os.path.exists(thumbpath):
            thumbobj = Image.open(thumbpath)
            print(ImageTk.PhotoImage(thumbobj))
            thumbs.append((thumbobj,imgfile))

        else:
            imgpath = os.path.join(imgdir,imgfile)

            try:
                print(imgpath)
                imgobj = Image.open(imgpath)
                imgobj.thumbnail(size,Image.ANTIALIAS)
                imgobj.save(thumbpath)
                thumbs.append((imgobj,imgfile))
            except Exception as e:
                print("skip: ",imgpath)
                print(e)

    return thumbs



def get_os():

    os_ver = sys.platform
    print(os_ver)
    if os_ver.find("win") > 0:
        return 1

    if os_ver.find("linux") > 0:
        return 2

    return 3


def getimgfiles(imgdir):

    if not os.path.exists(imgdir) :
        return []

    imglist  = []
    for file in os.listdir(imgdir):

            name,ext = os.path.splitext(file)

            if ext in FILE_FILTER:
                imglist.append(os.path.join(imgdir,file))
    return imglist

class ShowLargeImg(Toplevel):

    def __init__(self,imgdir,index = 0):

        Toplevel.__init__(self)


        self.imglist = []


        self.imglist = getimgfiles(imgdir)

        if len(self.imglist) == 0:

            return
        self.imgobj  = []
        for  i in range(len(self.imglist)):
            self.imgobj.append(None)

        self.w,self.h = self.wm_maxsize()


        imgobj = Image.open(self.imglist[index])

        self.curphoto = ImageTk.PhotoImage(imgobj)
        self.index    = index

        if self.curphoto.height() > self.h or self.curphoto.width() > self.w:
            max_x = self.w - 150

            max_y = self.h - 150

            imgobj.thumbnail((max_x,max_y),Image.ANTIALIAS)
            self.curphoto = ImageTk.PhotoImage(imgobj)

        self.lab = Label(self,image = self.curphoto)
        self.lab.config(width=self.w,height=self.h,bg='white')
        self.lab.pack(side=TOP)
        self.bind('<Left>',self.pre_event)
        self.bind('<Right>',self.next_event)

        self.l = Frame(self)
        self.r = Frame(self)
        self.l.pack(side = LEFT,expand=YES,fill=BOTH)
        self.r.pack(side = RIGHT,expand=YES,fill=BOTH)


        self.pre_bt = Button(self.l,text="前一张",command=self.pre_img)
        #self.pre_bt.pack(side =RIGHT)


        self.next_bt = Button(self.r,text="后一张",command=self.next_img)
        #self.next_bt.pack(side = LEFT)
        self.config(width=self.w,height=self.h)
        self.focus()


    def updata_img(self):


        if self.imgobj[self.index] == None:

            self.imgobj[self.index] = Image.open(self.imglist[self.index])


        self.curphoto = ImageTk.PhotoImage(self.imgobj[self.index])


        print(self.curphoto.width())
        print(self.curphoto.height())



        print(self.imgobj[self.index]._getexif())
        #self.lab.config(width=wh[0],height=wh[1])

        exif = self.imgobj[self.index]._getexif()

        if exif is not None:
            for tag,value in exif.items():
                print(TAGS.get(tag,tag))
                print(value)



        if self.curphoto.height() > self.h or self.curphoto.width() > self.w:
            self.thumbnail_img()

        self.lab.config(image=self.curphoto)

    def thumbnail_img(self):

        if self.curphoto.height() > self.h or  self.curphoto.width() > self.w:
            max_y = self.h - 150
            max_x = self.w - 150
            # resize 返回一个imageobj 使用新的imgobj
            #self.imgobj = self.imgobj.resize((max_x,max_y),Image.ANTIALIAS)
            self.imgobj[self.index].thumbnail((max_x,max_y),Image.ANTIALIAS)
            #self.imgobj.save()
            self.curphoto = ImageTk.PhotoImage(self.imgobj[self.index])



    def pre_event(self,event):
        print("event")

        self.pre_img()

    def pre_img(self):

        if len(self.imglist) == 0:
            return

        if self.index == 0:
            self.index = len(self.imglist) - 1
        else:
            self.index -= 1


        self.updata_img()


    def next_event(self,event):
        self.next_img()

    def next_img(self):

        if len(self.imglist) == 0:
            return

        if self.index == (len(self.imglist) - 1):
            self.index = 0
        else:
            self.index += 1

        self.updata_img()

THUMB_WIDTH  = 200
THUMB_HEIGNT = 200
THUMB_DELTA  = 200

class ShowThumbImg(Toplevel):

    def __init__(self,imgdir):

        Toplevel.__init__(self)

        self.w,self.h = self.wm_maxsize()

        self.imgdir = imgdir

        self.imglist = []
        self.photo   = []

        self.imglist = getimgfiles(self.imgdir)

        self.imgnums = len(self.imglist)

        if self.imgnums == 0:
            return


        self.xnums = int (((self.w - THUMB_DELTA) / THUMB_WIDTH))
        self.ynums = int (math.ceil((self.imgnums * THUMB_WIDTH) / (self.w  - THUMB_DELTA)))

        print(self.xnums)
        print(self.ynums)

        self.cav = Canvas(self,width=self.w-THUMB_DELTA,height=self.h + THUMB_HEIGNT,bg="white")

        self.cav.config(scrollregion=(0,0,THUMB_HEIGNT,self.ynums * THUMB_HEIGNT + THUMB_HEIGNT))

        self.sbar = Scrollbar(self)
        self.sbar.config(command=self.cav.yview)
        self.cav.config(yscrollcommand = self.sbar.set)
        self.sbar.pack(side=RIGHT,fill=Y)
        self.cav.pack(side=LEFT,expand=YES,fill=BOTH)

        #self.config(width=self.w,height=self.h)
        self.geometry(str(self.w) + "x" + str(self.h))

        self.cur_post = 0

        os_ver = get_os()

        if os_ver == 1 or os_ver == 3:
            self.bind("<MouseWheel>",self.move_scrollbar)
        else:
            self.bind("",self.move_scrollbar)


        self.dispaly()


    def click_one(self,index):
        print(index)
        ShowLargeImg(self.imgdir,index = index)

    def dispaly(self,offset = 0,num = -1):

        self.thumbs = []

        self.thumbs = makeThumbs(self.imgdir,size=(THUMB_WIDTH,THUMB_HEIGNT))

        thumbstmp = self.thumbs

        rowspos = 0

        print(len(thumbstmp))

        id = 0
        while thumbstmp:
            thumbsrows, thumbstmp = thumbstmp[:self.xnums],thumbstmp[self.xnums:]

            clopos = THUMB_DELTA

            print(len(thumbstmp))
            for (imgobj,imgfile) in thumbsrows:

                print("KKK")
                photo = ImageTk.PhotoImage(imgobj)
                link  = Button(self.cav,image = photo)
                link.config(width=THUMB_WIDTH,height=THUMB_HEIGNT,bg='white',relief=FLAT,cursor="hand2")
                hanlder = lambda index = id: self.click_one(index)
                link.config(command=hanlder)
                link.pack(side=LEFT,expand=YES)
                self.cav.create_window(clopos,rowspos,anchor=NW,window=link,width=THUMB_WIDTH,height=THUMB_HEIGNT)

                clopos += THUMB_WIDTH

                self.photo.append(photo)
                id += 1
            rowspos += THUMB_HEIGNT

    def move_scrollbar(self,event):



        os_ver = get_os()

        if os_ver == 1: #win
            self.cav.yview_scroll(-1 * (event.delta//120),"units")
        elif os_ver == 3: #mac os
            self.cav.yview_scroll(-1 * event.delta,"units")
        else:
            print("linux")



D_PATH = "目录:"
class MainDlg(Frame):

    def __init__(self,parent=None):

        Frame.__init__(self,parent)

        self.pack()
        self.config(width=40,height=20)

        self.bt_dir = Button(self,text="目录",command = self.click_dir)
        self.bt_dir.pack(side=LEFT,expand=YES,fill=BOTH)
        self.bt_dir.config(width=10,height=5)


        self.bt_single = Button(self,text="单图浏览",command = self.click_singel)
        self.bt_single.pack(side=LEFT,expand=YES,fill=BOTH)
        self.bt_single.config(width=10,height=5)

        self.bt_thumb = Button(self,text="缩图浏览",command = self.click_thumbs)
        self.bt_thumb.pack(side=LEFT,expand=YES,fill=BOTH)
        self.bt_thumb.config(width=10,height=5)

        self.lab_dir = Label(text=D_PATH)
        self.lab_dir.pack(side=BOTTOM,expand=YES,fill=BOTH)
        self.lab_dir.config(width=20,height=5)

        self.imgdir = ""


    def click_dir(self):



        self.imgdir = askdirectory()

        print(self.imgdir)


        if len(self.imgdir) > 0:

            self.lab_dir.config(text=self.imgdir,fg="green")


    def click_singel(self):

        if len(self.imgdir) == 0:
            self.lab_dir.config(text="请先选择图片文件目录",fg = "red")
            return

        ShowLargeImg(self.imgdir)

    def click_thumbs(self):

        if len(self.imgdir) == 0:
            self.lab_dir.config(text="请先选择图片文件目录",fg = "red")
            return

        ShowThumbImg(self.imgdir)



if __name__ == "__main__":

    MainDlg().mainloop()

    #s = ShowLargeImg("C:\\Users\\Public\\Pictures\\Sample Pictures")





