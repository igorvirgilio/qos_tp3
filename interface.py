from tkinter import *
from tkinter import messagebox
from pingtest import *
from speed import *
from network_capture import *
from traff_analy_qos import *
import pingtest
import tkinter
import network_capture
import time
import traff_analy_qos


class Gui():
    def __init__(self, root):
        # Interface structure start here.
        btn_capture = Button(root, text='1 - Capture Packet',
                             command=self.btncapture)
        btn_ping = Button(root, text='2 - Ping Test', command=self.windowping)
        btn_speed = Button(root, text='3 - SpeedTest', command=self.btnspeed)
        btn_nfstream = Button(root, text='4 - NFStream', command=self.btnnfstream)

        btn_capture.grid(column=0, row=0)
        btn_ping.grid(column=1, row=0)
        btn_speed.grid(column=2, row=0)
        btn_nfstream.grid(column=3, row=0)

        self.frame = Frame(root).grid(columnspan=4)
        self.txtArea = Text(self.frame, width=80, height=25)
        self.txtArea.grid(columnspan=4)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def btnteste(self):
        print("teste")

    def on_closing(self):
        #root.destroy()
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
           root.destroy()

    def btnspeed(self):
        try:
            fnspeed = Speed()
            self.txtArea.delete(1.0, END)
            d, u, p, s, c = fnspeed.main()
            self.txtArea.insert(END, 'Result SpeedTest:\n')
            self.txtArea.insert(END, 'Download: {} Mbps\n'.format(str(d)[:2]))
            self.txtArea.insert(END, 'Upload: {} Mbps\n'.format(str(u)[:2]))
            self.txtArea.insert(END, 'Latency: {:.0f} ms\n\n'.format(p))
            self.txtArea.insert(END, 'Server Information:\n')
            self.txtArea.insert(END, 'Local: {} \n'.format(s["name"]))
            self.txtArea.insert(END, 'Country: {} \n'.format(s["country"]))
            self.txtArea.insert(END, 'Sponsor: {} \n'.format(s["sponsor"]))
            self.txtArea.insert(END, 'Host: {} \n'.format(s["host"]))
            self.txtArea.insert(
                END, 'Download: {} Mbps\n\n'.format(str(d)[:2]))
            self.txtArea.insert(END, 'Client Information: \n')
            self.txtArea.insert(END, 'IP: {} \n'.format(c["ip"]))
            self.txtArea.insert(END, 'ISP: {} \n'.format(c["isp"]))
            self.txtArea.insert(
                END, 'ISP Rating: {} \n'.format(c["isprating"]))
            print("fim")
        except:
            self.txtArea.delete(1.0, END)
            self.txtArea.insert(END, 'Error!')

    def btncapture(self):
        try:
            self.txtArea.delete(1.0, END)
            fncapture = network_capture.network_capture()
            fncapture.main()
            self.txtArea.insert(END, 'End capture packet.')
        except:
            self.txtArea.delete(1.0, END)
            self.txtArea.insert(END, 'Error!')

    def btnping(self, newwindowping, entry_ping):
        try:
            self.txtArea.delete(1.0, END)
            info = []
            fnping = Ping()
            fnping.main(entry_ping, info)
            for i in fnping.info:
                self.txtArea.insert(END, i + '\n')
            newwindowping.destroy()
        except:
            self.txtArea.delete(1.0, END)
            self.txtArea.insert(END, 'Error!')

    def btnpingdefault(self, newwindowping, entry_ping):
        try:
            self.txtArea.delete(1.0, END)
            entry_ping.insert(END, 'www.google.com')
            info = []
            fnping = Ping()
            fnping.main(entry_ping, info)
            for i in fnping.info:
                self.txtArea.insert(END, i + '\n')
            newwindowping.destroy()
        except:
            self.txtArea.delete(1.0, END)
            self.txtArea.insert(END, 'Error!')

    def windowping(self):
        newwindowping = Toplevel(root)
        newwindowping.geometry('470x55')
        btn_window = Button(newwindowping, text='Ping Server',
                            command=lambda: self.btnping(newwindowping, entry_ping))
        btn_window.grid(column=0, row=0)
        btn_default = Button(newwindowping, text='Default',
                            command=lambda: self.btnpingdefault(newwindowping, entry_ping))
        btn_default.grid(column=3, row=0)
        label_ping = Label(
            newwindowping, text='Select the server or select default ping button.')
        label_ping.grid(column=1, row=1)
        entry_ping = Entry(newwindowping)
        entry_ping.grid(column=1, row=0)
        #server = entry_ping

    def btnnfstream(self):
        self.txtArea.delete(1.0, END)
        fnstream = Traff_Analy()
        fnstream.main()

# def newwindowtest():
#    nextwindow = Toplevel(root)
#    nextwindow.geometry('300x50')
#    btn_window = Button(nextwindow, text='Ping', command= lambda: btnping(nextwindow))
#    btn_window.grid(column=0, row=0)
#    label_ping = Label(nextwindow, text = 'What\'s the server do you want to ping?')
#    label_ping.grid(column=1, row=1)
#    entry_ping = Entry(nextwindow)
#    entry_ping.grid(column=1, row=0)
#    return nextwindow


if __name__ == '__main__':
    # Program start here
    root = Tk()
    root.title('TP - QOS')
    Gui(root)
    root.mainloop()
