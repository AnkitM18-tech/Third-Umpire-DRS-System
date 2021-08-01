#Importing Libraries
import tkinter
import cv2
import PIL.Image,PIL.ImageTk
from functools import partial  #so that we can enter only the command name in button
import threading
import imutils
import time

#Getting the stream
stream = cv2.VideoCapture("sources/video.mp4")
flag =True

#functions for commands
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)    # variable reading the frame
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed,frame = stream.read()
    if not grabbed:
        exit()
        
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image = frame, anchor = tkinter.NW)
    if flag:
        canvas.create_text(335,25, fill="black", font = "Monsterrat 25 bold", text = "Decision Pending")
    
    flag = not flag

def pending(decision):
    #1 - Display Decision Pending
    frame = cv2.cvtColor(cv2.imread("sources/decision_pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image = frame, anchor = tkinter.NW)
    #2 - Wait for 1sec
    time.sleep(1)
    #3 - Show sponser
    frame = cv2.cvtColor(cv2.imread("sources/sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image = frame, anchor = tkinter.NW)
    #4 - Wait for 2sec
    time.sleep(2)
    #5 - Display Decision Image
    if decision == "out":
        decisionImage = "sources/out.png"
    else:
        decisionImage = "sources/not_out.png"

    frame = cv2.cvtColor(cv2.imread(decisionImage), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = SET_WIDTH, height = SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image = frame, anchor = tkinter.NW)

#Out Function
def out():
    thread = threading.Thread(target=pending, args = ("out",))     # making threads so that mainloop keeps running and don't hang
    thread.daemon = 1
    thread.start()
    print("Player is Out!")    #Terminal Log

#Not Out function
def notout():
    thread = threading.Thread(target=pending, args = ("not out",))  # making threads so that mainloop keeps running and don't hang
    thread.daemon = 1
    thread.start()
    print("Player is Not Out!")    #Terminal Log


#Dimension of Main Window
SET_WIDTH = 650
SET_HEIGHT = 368


#Tkinter Gui starts here
window = tkinter.Tk()
window.title("Third Umpire Decision Review System")  #Title Here
cv_image = cv2.cvtColor(cv2.imread("sources/welcome.png"), cv2.COLOR_BGR2RGB)    #Getting the Welcome Image
canvas = tkinter.Canvas(window, width = SET_WIDTH, height = SET_HEIGHT)          #Creating the canvas
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_image))              #Photo to show on canvas
iamge_canvas = canvas.create_image(0,0, ancho = tkinter.NW, image= photo)
canvas.pack()

#Buttons to control playback
btn = tkinter.Button(window, text = "<< Previous(Fast)", width = 50, command = partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text = "< Previous(Slow)", width = 50, command = partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text = "Next(Slow) >", width = 50, command = partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text = "Next(Fast) >>", width = 50, command = partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text = "Give Out", width = 50, command = out)
btn.pack()

btn = tkinter.Button(window, text = "Give Not Out", width = 50, command = notout)
btn.pack()

window.mainloop()        #running the loop for GUI