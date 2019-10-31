# import modules
import pyautogui as pg
import time
import tkinter as tk
from tkinter import filedialog
from pynput import mouse, keyboard

# initial value
filelist = []
recordStatus = False
specialKeys = False

# main:
window = tk.Tk()
window.title("MI Path") 
window.geometry("500x500")
window.configure(background="black")

# program name
tk.Label(window, text="MI Path", bg="black", fg="white", width=45, height=0,
      font="Helvetica 19 bold", justify="center").grid(row=0, column=0, sticky=tk.W)

output = tk.Text(window, width=65, height=10, wrap=tk.WORD, background="white")
output.place(x=20, y=50)

def saveCmd():
    global output, filelist
    filesave = filedialog.asksaveasfile(filetypes=[('Text Files', ['.txt'])]).name
    f = open(filesave, 'w')
    filestring = " \n".join(str(x) for x in filelist)
    f.write(filestring)
    f.close()

# save button
saveBtn = tk.Button(window, text="เซฟไฟล์", width=12, command=saveCmd)
saveBtn.place(x=200, y=200)

def loadCmd():
    global output
    fileinfo = filedialog.askopenfile(filetypes=[('Text Files', ['.txt'])])
    readtext = fileinfo.read()
    print(readtext)
    output.insert(tk.END, f"{readtext}")

# load button
loadBtn = tk.Button(window, text="โหลดไฟล์", width=12, command=loadCmd)
loadBtn.place(x=350, y=200)

# selection action
def doAct(action):
    keys = action.split(",")
    skeys = action.split(" ")
    time.sleep(0.50)
    if action.find('Button.left') != -1:
        x = float(keys[0])
        y = float(keys[1].split(" ")[1])
        pg.mouseDown(x, y)
        time.sleep(0.15)
        pg.mouseUp(x, y)
    elif action.find('Button.right') != -1:
        x = float(keys[0])
        y = float(keys[1].split(" ")[1])
        pg.mouseDown(x, y, button='right')
        time.sleep(0.15)
        pg.mouseUp(x, y)
    elif action.find('Key.cmd') != -1:
        pg.hotkey('command', skeys[1])
    elif action.find('Key.alt') != -1:
        pg.hotkey('alt', skeys[1])
    elif action.find('Key.ctrl') != -1:
        pg.hotkey('ctrl', skeys[1])
    elif action.find('Key.shift') != -1:
        pg.hotkey('shift', skeys[1])
    elif action.find('Key.enter') != -1:
        pg.press('enter')
    elif action.find('Key.space') != -1:
        pg.press('space')
    elif action.find('Key.backspace') != -1:
        pg.press('backspace')
    else: 
        pg.press(action)

# record function
def recordFn(): 
    global recordStatus 
    recordStatus = True

# stop function
def stopRecordCmd(): 
    global recordStatus 
    recordStatus = False

# play function
def playCmd(): 
    global recordStatus, filelist
    if recordStatus==False:
        for x in filelist:
            doAct(x)

# clear function
def clearCmd(): 
    global recordStatus, filelist
    if recordStatus==False:
        filelist = []
        output.delete('1.0', tk.END)

# record button
recordBtn = tk.Button(window, text="บันทึกปุ่ม", width=12, command=recordFn)
recordBtn.place(x=40, y=280)

# stop button
stopRecordBtn = tk.Button(window, text="หยุดบันทึกปุ่ม", width=12, command=stopRecordCmd)
stopRecordBtn.place(x=185, y=280)

# clear button
clearBtn = tk.Button(window, text="ล้างบันทึก", width=12, command=clearCmd)
clearBtn.place(x=330, y=280)

# play button
playBtn = tk.Button(window, text="เล่น", width=12, command=playCmd)
playBtn.place(x=185, y=350)

# exit function
def closeFn():
    window.destroy()
    exit()

# exit button
closeBtn = tk.Button(window, text="ออกการใช้งาน", width=12, command=closeFn)
closeBtn.place(x=185,y=420)

# pynput listener
def on_click(x, y, button, pressed):
    global recordStatus, filelist
    if pressed:
        if recordStatus:
            output.insert(tk.END, f"{x}, {y} {button}\n")
            filelist.append(f"{x}, {y} {button}")

def on_press(key):
    global recordStatus, specialKeys, filelist
    filelen = len(filelist) 
    try:
        if recordStatus:
            if not specialKeys:
                output.insert(tk.END, f"{key.char} \n")
                filelist.append(f"{key.char}")
            elif filelen > 0:
                specialKeys = False
                output.insert(tk.END, f"{key.char} \n")
                filelist[filelen - 1] = f"{filelist[filelen - 1]}{key.char}"
    except AttributeError:
        if recordStatus:
            if str(key) == "Key.space" and filelen > 0 and not specialKeys:
                output.insert(tk.END, f"{key} \n")
                filelist.append(f"{key}")
            elif str(key) == "Key.enter" and filelen > 0 and not specialKeys:
                output.insert(tk.END, f"{key} \n")
                filelist.append(f"{key}")
            elif str(key) == "Key.backspace" and filelen > 0 and not specialKeys:
                output.insert(tk.END, f"{key} \n")
                filelist.append(f"{key}")
            elif str(key).find("Key.shift") or str(key).find("Key.cmd") or str(key).find("Key.alt") or str(key).find("Key.ctrl") and not specialKeys and filelen > 0:
                specialKeys = True
                output.insert(tk.END, f"{key} ")
                filelist.append(f"{key} ")
            elif filelen > 0:
                output.insert(tk.END, f"{key} ")
                filelist[filelen - 1] = f"{key} "

mouse_listener = mouse.Listener(
    on_click=on_click
)
mouse_listener.start()
keyboard_listener = keyboard.Listener(
    on_press=on_press
)
keyboard_listener.start()

# run the main loop
window.mainloop()
