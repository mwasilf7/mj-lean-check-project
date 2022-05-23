import PoseModule as pm
import cv2
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

win=Tk()
win.title("MJ Lean Check")
win.geometry("1280x720+0+0")
win.state("zoomed")
win.iconbitmap("MJ-lean-icon.ico")

frame_1 = Frame(win, width=1920, height=1080, bg='#210035').place(x=0, y=0)
widget = Label(win, text="Michael Jackson's Anti-Gravity Lean Check Program", font=("Helvetica", 35, ("bold")), bg="#40444a", fg="#DE9B16").pack(pady=20)

w = 820
h = 480

cap = cv2.VideoCapture(0)

label1 = Label(win, width=w, height=h)
label1.place(x=30, y=100)
    
back_btn = Button(win,text = "Exit",width=7, height=2, bg = "#FF9DAA", fg = "#D12A2A", font=("Calibri", 20,"bold"), command = win.destroy).place(x=980, y=550)

status_label = Label(win, text="Status: ", font=("Arial", 25, "bold"), bg="#40444a", fg="#49CFD1").place(x=880, y=130)
status_txt = StringVar()
status_txt_label = Label(win, textvariable=status_txt, font=("Arial", 25, "bold"), bg="#40444a", fg="#AA00FF").place(x=1000, y=130)

angle_label = Label(win, text="Angle: ", font=("Arial", 25, "bold"), bg="#40444a", fg="#49CFD1").place(x=880, y=200)
angle_txt = StringVar()
angle_txt_label = Label(win, textvariable=angle_txt, bg="#40444a", fg = "#FFEE00", font=("Arial", 25, "bold")).place(x=990, y=200)

# For Browsing Videos
def video_select():
    global video_path,cap
    video_path = filedialog.askopenfilename(filetypes=[("Video Files (*.mp4)","*.mp4"),("Image Files (*.jpg)","*.jpg"),("Image Files (*.png)","*.png"),("Image Files (*.gif)","*.gif")])
    if video_path=="":
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    else:    
        cap = cv2.VideoCapture(video_path)

# For Live feed
def cam_live():
    global video_path,cap
    video_path = 0
    cap = cv2.VideoCapture(video_path)

# _________________Live Button ____________________________

live_btn = Button(win, height = 1, width=8,font=("Calibri", 20, "bold"),  text="Live", fg="#114488", bg="#77FFD0", command=cam_live)
live_btn.place(x=900,y=450)

# _________________Browse Button___________________________

browse_btn = Button(win, height = 1, width=8,text="Browse",font=("Calibri", 20, "bold"), fg="#114488", bg='#77FFD0', command=video_select)
browse_btn.place(x=1050,y=450)

#__________________Pose Detection__________________________

detector = pm.PoseDetector()

while True:
    success, img = cap.read()
    if success:
        img=cv2.flip(img, 1)
        img=cv2.resize(img,(w,h))
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findPose(img)
        lmList=detector.findPosition(img)

        if len(lmList) != 0:
            if lmList[24][3] > lmList[23][3]:
            ##____________________Left side____________________##
                angle1,angle2,angle3=detector.findAngle(img, 11,23,25,27, side="left")
                
            elif lmList[24][3] < lmList[23][3]:
            ##____________________Right side___________________##
                angle1,angle2,angle3=detector.findAngle(img, 12,24,26,28, side="right")

            ## Angle Accuracy Determination
            if 170<=angle2<=190:
                if 170<=angle3<=190:
                    if 35<=angle1<=55:
                        status_txt.set("Correct")
                    elif 55<angle1<=70:
                        status_txt.set("Fairly Close")
                    elif angle1<35:
                        status_txt.set("Too Much Lean")
                    else:
                        status_txt.set("Wrong")
                else:
                    status_txt.set("Straighten Your Legs")
                    angle1='--'
            else:
                status_txt.set("Straighten Your Back")
                angle1='--'
            if type(angle1)==float:
                angle_txt.set(str(round(angle1))+'°')
            else:
                angle_txt.set(angle1)

        image = Image.fromarray(img)
        finalImage = ImageTk.PhotoImage(image)
        label1.configure(image=finalImage)
        label1.image = finalImage
        
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    win.update()    