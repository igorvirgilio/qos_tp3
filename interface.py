from tkinter import *
from tkinter import messagebox
from pingtest import *
from speed import *
from network_capture import *
import pingtest
import tkinter
import network_capture
import time


def btnteste():
    print("teste")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def btnspeed():
    try:
        fnspeed = Speed()
        txtArea.delete(1.0, END)
        d, u, p, s, c = fnspeed.main()
        txtArea.insert(END, 'Result SpeedTest:\n')
        txtArea.insert(END, 'Download: {} Mbps\n'.format(str(d)[:2]))
        txtArea.insert(END, 'Upload: {} Mbps\n'.format(str(u)[:2]))
        txtArea.insert(END, 'Latency: {:.0f} ms\n\n'.format(p))
        txtArea.insert(END, 'Server Information:\n')
        txtArea.insert(END, 'Local: {} \n'.format(s["name"]))
        txtArea.insert(END, 'Country: {} \n'.format(s["country"]))
        txtArea.insert(END, 'Sponsor: {} \n'.format(s["sponsor"]))
        txtArea.insert(END, 'Host: {} \n'.format(s["host"]))
        txtArea.insert(END, 'Download: {} Mbps\n\n'.format(str(d)[:2]))
        txtArea.insert(END, 'Client Information: \n')
        txtArea.insert(END, 'IP: {} \n'.format(c["ip"]))
        txtArea.insert(END, 'ISP: {} \n'.format(c["isp"]))
        txtArea.insert(END, 'ISP Rating: {} \n'.format(c["isprating"]))
        print("fim")
    except:
        txtArea.delete(1.0, END)
        txtArea.insert(END, 'Error!')


def btncapture():
    try:
        txtArea.delete(1.0, END)
        fncapture = network_capture.network_capture()
        fncapture.main()
        txtArea.insert(END, 'End capture packet.')
    except:
        txtArea.delete(1.0, END)
        txtArea.insert(END, 'Error!')


def btnping(newwindowping):
    fnping = Ping()
    fnping.main()
    newwindowping.destroy()
    txtArea.delete(1.0, END)

#    except:
#        txtArea.delete(1.0, END)
#        txtArea.insert(END, 'Error!')



def windowping():
    newwindowping = Toplevel(root)
    newwindowping.geometry('300x50')
    btn_window = Button(newwindowping, text='Ping', command= lambda: btnping(newwindowping))
    btn_window.grid(column=0, row=0)
    label_ping = Label(newwindowping, text = 'What\'s the server do you want to ping?')
    label_ping.grid(column=1, row=1)
    entry_ping = Entry(newwindowping)
    entry_ping.grid(column=1, row=0)
    return newwindowping

def newwindowtest():
    nextwindow = Toplevel(root)
    nextwindow.geometry('300x50')
    btn_window = Button(nextwindow, text='Ping', command= lambda: btnping(nextwindow))
    btn_window.grid(column=0, row=0)
    label_ping = Label(nextwindow, text = 'What\'s the server do you want to ping?')
    label_ping.grid(column=1, row=1)
    entry_ping = Entry(nextwindow)
    entry_ping.grid(column=1, row=0)
    return nextwindow
    
    



root = Tk()
root.title('TP - QOS')

btn_capture = Button(root, text='Capture Packet', command=btncapture)
btn_ping = Button(root, text='Ping Test', command=windowping)
btn_speed = Button(root, text='SpeedTest', command=btnspeed)
btn_nfstream = Button(root, text='NFStream', command=btnteste)


btn_capture.grid(column=0, row=0)
btn_ping.grid(column=1, row=0)
btn_speed.grid(column=2, row=0)
btn_nfstream.grid(column=3, row=0)


frame = Frame(root).grid(columnspan=4)
txtArea = Text(frame, width=80, height=35)
txtArea.grid(columnspan=4)


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
