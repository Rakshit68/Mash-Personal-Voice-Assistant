from tkinter import *
from tkinter import ttk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import filedialog
import platform
import psutil
import Backend

#brightness
import screen_brightness_control as pct


#audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume


#weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz


#clock
from time import strftime


#calendar
from tkcalendar import *


#open google
import pyautogui
import subprocess
import webbrowser as wb
import random


root=Tk()
root.title('Mash')
root.geometry("1170x500+300+170")
root.resizable (False, False)
root.configure (bg='#111111')#292e2e
#root.wm_attributes("-transparentcolor","white")
#root.configure(background='white')

#icon
image_icon=PhotoImage(file=r"D:\Mash\Icons\icon.png")
root.iconphoto (False, image_icon)

Body=Frame (root, width=1200,height=600, bg="#ffffff")#d6d6d6
Body.pack(pady=20, padx=20)


#############################################################################################################################################################################


LHS=Frame (Body, width=310,height=435, bg="#111111", highlightbackground="#adacb1", highlightthickness=2)
LHS.place(x=10,y=10)

#logo
photo=PhotoImage(file=r"D:\Mash\Icons\laptop2.png")
photo=photo.subsample(2,2)
myimage=Label(LHS, image=photo, background="#111111")
myimage.place(x=2,y=20)

my_system=platform.uname()

l1=Label(LHS, text=my_system.node,bg="#111111",fg="#ffa31a", font=("Acumin Variable Concept", 15, 'bold'), justify="center")
l1.place(x=20,y=200)

l2=Label(LHS, text=f"Version: {my_system.version}",bg="#111111",fg="#ffa31a", font=("Acumin Variable Concept", 9), justify="center")
l2.place(x=20,y=225)

l3=Label(LHS, text=f"Operating System: {my_system.system}",bg="#111111",fg="white", font=("Acumin Variable Concept", 15), justify="center")
l3.place(x=20,y=250)

l4=Label(LHS, text=f"Machine: {my_system.machine}",bg="#111111",fg="white", font=("Acumin Variable Concept", 15), justify="center")
l4.place(x=20,y=280)

l5=Label(LHS, text=f"Total RAM: {round(psutil.virtual_memory().total/1000000000,2)} GB",bg="#111111",fg="white", font=("Acumin Variable Concept", 15), justify="center")
l5.place(x=20,y=310)

l6=Label(LHS, text=f"Processor:{my_system.processor}",bg="#111111",fg="white", font=("Acumin Variable Concept", 7), justify="center")
l6.place(x=20,y=340)


#############################################################################################################################################################################

RHS=Frame (Body, width=470, height=230, bg="#111111", highlightbackground="#adacb1", highlightthickness=1)
RHS.place(x=330,y=10)

system=Label (RHS, text='System__________________________________', font=("Acumin Variable Concept", 15,'bold'), bg="#111111",fg="#ffa31a")
system.place(x=10,y=10)

####Battery######################################################################
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def none():
    global battery_png
    global battery_label

    battery=psutil. sensors_battery()
    percent=battery.percent
    time=convertTime (battery.secsleft)
    
    lbl.config(text=f" {percent}%")
    lbl_plug.config(text=f'Plug in: {str(battery.power_plugged)}')
    lbl_time.config(text=f'{time} remaining')

    battery_label=Label (RHS, background= '#111111')
    battery_label.place(x=15,y=50)
    lbl.after (1000, none)

    if battery.power_plugged==True:
        battery_png=PhotoImage(file=r"D:\Mash\Icons\battery_carging.png")
        battery_png=battery_png.subsample(6,6)
        battery_label.config(image=battery_png)
    else:
        battery_png=PhotoImage(file=r"D:\Mash\Icons\battery.png")
        battery_png=battery_png.subsample(6,6)
        battery_label.config(image=battery_png)


lbl=Label(RHS, font=("Acumin Variable Concept", 40, 'bold'), bg='#111111',fg="#ffa31a")
lbl.place(x=250,y=80)

lbl_plug=Label (RHS, font=("Acumin Variable Concept",10),bg='#111111',fg="white")
lbl_plug.place(x=20,y=100)

lbl_time=Label (RHS, font=("Acumin Variable Concept", 15),bg='#111111',fg="white")
lbl_time.place(x=250,y=140)

none()

####Speaker######################################################################
lbl_speaker=Label (RHS, text="Speaker:", font=('arial', 10, 'bold'), bg='#111111',fg="white")
lbl_speaker.place(x=10,y=150)
volume_value=tk.DoubleVar()
def get_current_volume_value():
    return '{: .2f}'.format(volume_value.get())
def volume_changed(event):
    device=AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-float(get_current_volume_value()),None)

style= ttk.Style()
style.configure("TScale", background='#111111')

volume=ttk.Scale (RHS, from_=60, to=0, orient='horizontal', command=volume_changed, variable=volume_value)
volume.place(x=90,y=150)
volume.set(0)


####Brightness######################################################################
lbl_brightness=Label (RHS, text='Brightness', font=('arial', 10, 'bold'),bg='#111111',fg="white")
lbl_brightness.place(x=10,y=190)

current_value=tk.DoubleVar()

def get_current_value():
    return '{: .2f}'.format(current_value.get())
def brightness_changed(event):
    pct.set_brightness(get_current_value())
brightness=ttk. Scale (RHS, from_=0, to=100, orient='horizontal',command=brightness_changed, variable=current_value)
brightness.place(x=90,y=190)


#############################################################################################################################################################################


RHB=Frame (Body, width=470, height=190, bg="#111111", highlightbackground="#adacb1", highlightthickness=1)
RHB.place(x=330,y=255)


####Apps#############################################################################
RHB=Frame (Body, width=470, height=190, bg="#111111", highlightbackground="#adacb1", highlightthickness=1)
RHB.place(x=330,y=255)

apps=Label(RHB, text='Quick Access Apps________________________', font=('Acumin Variable Concept', 15,'bold'), bg='#111111',fg="#ffa31a")
apps.place(x=10,y=10)

app1_image=PhotoImage(file=r"D:\Mash\Icons\App1.png")
app1_image=app1_image.subsample(10,10)
app1=Button (RHB, image=app1_image, bg='#111111', bd=0)
app1.place(x=15,y=50)

app2_image=PhotoImage(file=r"D:\Mash\Icons\App2.png")
app2_image=app2_image.subsample(9,9)
app2=Button (RHB, image=app2_image, bg='#111111', bd=0)
app2.place(x=100,y=50)

app3_image=PhotoImage(file=r"D:\Mash\Icons\App3.png")
app3_image=app3_image.subsample(10,10)
app3=Button(RHB, image=app3_image, bg='#111111', bd=0)
app3.place(x=185,y=50)

app4_image=PhotoImage(file=r"D:\Mash\Icons\App4.png")
app4_image=app4_image.subsample(16,16)
app4=Button (RHB, image=app4_image, bg='#111111',bd=0)
app4.place(x=270,y=50)

app5_image=PhotoImage(file=r"D:\Mash\Icons\App5.png")
app5_image=app5_image.subsample(12,12)
app5=Button (RHB, image=app5_image, bg='#111111',bd=0)
app5.place(x=355,y=50)

app6_image=PhotoImage(file=r"D:\Mash\Icons\App6.png")
app6_image=app6_image.subsample(10,10)
app6=Button (RHB, image=app6_image, bg='#111111', bd=0)
app6.place(x=15,y=120)

app7_image=PhotoImage(file=r"D:\Mash\Icons\App7.png")
app7_image=app7_image.subsample(10,10)
app7=Button(RHB, image=app7_image, bg='#111111', bd=0)
app7.place(x=100,y=120)

app8_image=PhotoImage(file=r"D:\Mash\Icons\App8.png")
app8_image=app8_image.subsample(10,10)
app8=Button (RHB, image=app8_image,bg='#111111', bd=0)
app8.place(x=185,y=120)

'''app9_image=Photo Image(file='Image/App9.png')
app9=Button(RHB, image=app9_image, bd=0)
app9.place(x=270,y=120)

app10_image=Photo Image(file='Image/App10.png')
app10-Button(RHB, image=app10_image, bd=0)
app10.place(x=355,y=120)'''

#############################################################################################################################################################################

RRHS=Frame (Body, width=310,height=435, bg="#111111", highlightbackground="#adacb1", highlightthickness=2)
RRHS.place(x=810,y=10)

def start_backend():
    Backend.main()

system=Label (RRHS, text='Mash_____________________', font=("Acumin Variable Concept", 15,'bold'), bg="#111111",fg="#ffa31a")
system.place(x=10,y=10)
####Mash###############################################################

mash_image=PhotoImage(file=r"D:\Mash\Icons\mash.png")
mash_image=mash_image.subsample(3,3)
mash=Button (RRHS,command=start_backend, image=mash_image, bg="#111111", bd=0)
mash.place(x=65,y=70)

text_widget = tk.Text(RRHS, height=10, width=40)
text_widget.place(x=30, y=260, width=250, height=150)

#Backend.set_text_widget(text_widget)


#root.overrideredirect(1)
root.mainloop()
