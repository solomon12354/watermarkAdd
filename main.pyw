import cv2
import numpy as np
import os
from PIL import Image
import imghdr
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from functools import partial

global origin
origin = ''
global watermarks
watermarks = ''
global final
final = 'C:\\newPhoto'

def onOK():
    msg = ''
    try:
        msg = "已處理完畢\nHave finished.\nSaved in " + C
    except:
        msg = "已處理完畢\nHave finished.\nSaved in " + final
    tk.messagebox.showinfo(title = 'Finished', # 視窗標題
                                message = msg)   # 訊息內容
def noPath():
    msg = '您沒有設定好路徑!\nYou have not set your path yet!'
    
    tk.messagebox.showinfo(title = 'Warning!!', # 視窗標題
                                message = msg)   # 訊息內容

def sel():
   global mode
   mode = int(var.get())
   return mode
   
def open_new(pathDisplay):
   global C
   file = filedialog.askdirectory()
   
   if file:
      C = file
      
      pathDisplay3.config(text="新照片放於(The new photo's path is located at) : " + str(C))
      return C

def open_file(pathDisplay):
   global A
   file = filedialog.askdirectory()
   
   if file:
      A = file
      
      pathDisplay.config(text="圖片資料夾位於(The folder of pictures's path is located at) : " + str(A))
      return A

def open_picture(pathDisplay):
    global B
    file = filedialog.askopenfile(filetypes=[
                                            
                                            ("jpeg files","*.jpg"),
                                            ("png files","*.png"),
                                            ("gif files","*.gif"),('All Files','*')])
    if file:
      B = file.name
      pathDisplay.config(text="浮水印放在(The watermark is set on) : " + str(B))
      return B
      

def process(originPath,watermark,heightMode,widthMode,fin):

    if not os.path.exists(fin):
        os.mkdir(fin)
    print(origin,watermarks)
    try:
        originPath = A
    except:
        noPath()
        return

    try:
        watermark = B
    except:
        noPath()
        return
    heightMode = 0
    widthMode = 0
    global mode
    mode = int(var.get())
    if(mode):
        print(mode)
        heightMode = int(mode//3)
        widthMode = mode%3
    print(heightMode,widthMode)
    try:
        fin = C
    except:
        fin = 'C:\\newPhoto'
    for i in os.listdir(originPath):
        
        if(i.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
            img1 = cv2.imread(originPath + '\\' + i)
            img2 = cv2.imread(watermark)

            

            h1, w1, c1 = img1.shape
            h2, w2, c2 = img2.shape

            rate = h2/w2

            
            w2 = int(w1 * 0.2) 
            h2 = int(w2 * rate)

            img1 = cv2.resize(img1,(w1,h1))
            img2 = cv2.resize(img2,(w2,h2))
            # I want to put logo on top-left corner, So I create a ROI
            rows,cols,channels = img2.shape

            leftL = 0
            leftR = rows
            midL = int(h1/2 - rows/2)
            midR = int(h1/2 + rows/2)
            rightL = h1 - rows - 1
            rightR = h1 - 1

            topT = 0
            topB = cols
            corT = int(w1/2 - cols/2)
            corB = int(w1/2 + cols/2)
            botT = w1 - cols - 1
            botB = w1 - 1

            heightSet = [[leftL,leftR],[midL,midR],[rightL,rightR]]
            widthSet  = [[topT,topB],[corT,corB],[botT,botB]]

            roi = img1[heightSet[heightMode][0]:heightSet[heightMode][1], widthSet[widthMode][0]:widthSet[widthMode][1] ]

            # Now create a mask of logo and create its inverse mask also
            img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)

            # Now black-out the area of logo in ROI
            img1_bg = cv2.bitwise_and(roi,roi,mask = mask)

            # Take only region of logo from logo image.
            img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)

            # Put logo in ROI and modify the main image
            dst = cv2.add(img1_bg,img2_fg)
            img1[heightSet[heightMode][0]:heightSet[heightMode][1], widthSet[widthMode][0]:widthSet[widthMode][1] ] = dst

            cv2.imwrite(fin + '\\' + i,img1)
            #cv2.imshow('res',img1)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
    onOK()
        
if __name__ == '__main__':
    window = tk.Tk()
    window.title('WaterMark!')
    window.geometry('800x700')
    window.resizable(False, False)
    
    #startAdd.grid(padx=350, pady=600)
    label = Label(window, text="為您的照片增加浮水印!\nLet your pictures add your watermark!", font=('Georgia 13'))
    label.pack(pady=10)

    pathDisplays = Label(window, text="圖片資料夾位於(The folder of pictures's path is located at) : ", font=('Aerial 11'))
    pathDisplays.place(relx=0.01, rely=0.2)
    browse = tk.Button(text="Browse", command=partial(open_file,pathDisplays),height=1,width=10)
    browse.place(relx=0.8, rely=0.2)

    pathDisplay2 = Label(window, text="浮水印位於(The watermark's path is located at) : ", font=('Aerial 11'))
    pathDisplay2.place(relx=0.01, rely=0.3)
    browse2 = tk.Button(text="Browse", command=partial(open_picture,pathDisplay2),height=1,width=10)
    browse2.place(relx=0.8, rely=0.3)

    pathDisplay3 = Label(window, text="新照片放於(The new photo's path is located at) : ", font=('Aerial 11'))
    pathDisplay3.place(relx=0.01, rely=0.4)
    browse3 = tk.Button(text="Browse", command=partial(open_new,pathDisplay2),height=1,width=10)
    browse3.place(relx=0.8, rely=0.4)

    var = IntVar()
    var.set(0)

    waterLabel = Label(window, text="浮水印放在(The watermark is set on) : ", font=('Aerial 11'))
    waterLabel.place(relx=0.3, rely=0.5)

    myName = Label(window, text="Made by Shao-Lei Wang\n王少雷製作", font=('Aerial 11'))
    myName.place(relx=0.75, rely=0.9)

    R1 = Radiobutton(window, text="左上(top left)", variable=var, value=0,
                  command=sel)
    R1.place(relx=0.15, rely=0.6)

    R2 = Radiobutton(window, text="中上(top middle)", variable=var, value=1,
                  command=sel)
    R2.place(relx=0.4, rely=0.6)

    R3 = Radiobutton(window, text="右上(top right)", variable=var, value=2,
                  command=sel)
    R3.place(relx=0.65, rely=0.6)

    R4 = Radiobutton(window, text="左中(middle left)", variable=var, value=3,
                  command=sel)
    R4.place(relx=0.15, rely=0.7)

    R5 = Radiobutton(window, text="中間(center)", variable=var, value=4,
                  command=sel)
    R5.place(relx=0.4, rely=0.7)

    R6 = Radiobutton(window, text="右中(middle right)", variable=var, value=5,
                  command=sel)
    R6.place(relx=0.65, rely=0.7)

    R7 = Radiobutton(window, text="左下(bottom left)", variable=var, value=6,
                  command=sel)
    R7.place(relx=0.15, rely=0.8)

    R8 = Radiobutton(window, text="中下(bottom middle)", variable=var, value=7,
                  command=sel)
    R8.place(relx=0.4, rely=0.8)

    R9 = Radiobutton(window, text="右下(bottom right)", variable=var, value=8,
                  command=sel)
    R9.place(relx=0.65, rely=0.8)

    startAdd = tk.Button(text="開始加入浮水印\nStart to add watermark", command=partial(process,origin,watermarks,int(var.get()/3),var.get()%3,final),height=3,width=20)
    startAdd.place(relx=0.5, rely=0.99, anchor='s')
    window.mainloop()
    #process(origin,watermarks,1,2,final)