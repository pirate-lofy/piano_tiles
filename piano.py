import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv   
import d3dshot 
import time
import pyautogui
from pynput import mouse

flag=False
score=0
limit=600
    
def on_click(x, y, button, pressed):
    global flag
    if button == mouse.Button.left:
        print('clicked')
        flag=True
        return False 
    
def listener():
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

def process(img):
    global score
    img2=img[150:670,300:680,:]
    h,w,_=img2.shape
    iw=w//4
    indxs=[(i*iw)+iw//2 for i in range(4)]
    cs=[0,1,2,3]
    points=[]
    for c in cs:
        mn=256
        slc=img2[:,indxs[c]-5:indxs[c]+5]
        slc=cv.cvtColor(slc,cv.COLOR_BGR2GRAY)
        slc=np.sum(slc,1)/10
        for i in range(h-1,-1,-1):
            if slc[i]<40 and slc[i]<mn:
                score+=1
                mn=slc[i]
                y=indxs[c]+300
                x=i+150
                if score>limit:
                    m=(score-limit)//10
                    y-=m
                points.append((y,x))
                break
    return points


d = d3dshot.create(capture_output="numpy")
listener()
while 1:
    if flag:
        img=d.screenshot()  
        points=process(img)
        points.sort(key=lambda x:x[1],reverse=True)
        if len(points):
            print('location= ',points[0],
                  'score= ',score)
            pyautogui.click(points[0][0],points[0][1])
            if score<600:
                time.sleep(0.1)
    

