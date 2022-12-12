import subprocess
from tkinter import *
from tkinter import ttk
import time
import re
import tkinter.messagebox as tmsg
import ctypes as ct

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Application Wifi Automation")
        self.geometry("600x500+90+50")
        self.resizable(False,False)
        # self.iconbitmap("E:\Tkinter\Project\\abc.icon")
    def title_color(self):
        self.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(self.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 1
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
    def Tab(self):
        self.tab=ttk.Notebook(self)
    def Frame(self):
        self.f1=Frame(self,bg="grey",relief=SOLID)
        self.f2=Frame(self,bg="red",relief=FLAT,height=600,width=500)

        self.tab.add(self.f1,text="First Phase")
        self.tab.add(self.f2,text="Note")
        self.tab.pack()
        # self.tab.place(x=0,y=0)
    def Scroll(self):
        self.sc=Scrollbar(self.f1)
        self.sc.pack(side=RIGHT,fill=Y)

        self.sc2=Scrollbar(self.f2)
        self.sc2.pack(side=RIGHT,fill=Y)
    def Output(self):
        self.screen=Text(self.f1,yscrollcommand=self.sc.set,fg="green",font="arail 10 bold",wrap="word")
        self.screen.insert(END,f"It\'s working !...")
        self.screen.pack(side=LEFT,fill=BOTH)
        self.sc.config(command=self.screen.yview)

        #---------------------------

        self.screen2=Text(self.f2,yscrollcommand=self.sc2.set,wrap="word",bg="grey",fg="green",font=("crusial 15 underline"))
        self.screen2.pack(fill=BOTH)
        self.sc2.config(command=self.screen2.yview)
    def Automation(self,event):
        self.screen.config(state="normal")
        message=tmsg.askyesno("Congratulation!","Would you like to wait 1-2 min ")
        if not message:
            tmsg.showwarning("Abort","Process has been stopped")
        else:
            tmsg.showinfo("Wait","Kindly please wait process has been started")
            t=subprocess.check_output("netsh wlan show profile",shell=1).decode()
            # t=s.check_output("netsh wlan show profile",shell=1).decode()


            profiles = re.findall(r"(All User Profile.+:.)(.*)", t)
            # temp=[]
            dictionary1={}
            for ele in profiles:
                # temp.append(ele[1])
                # print(ele[1])
                try:
                    value=subprocess.check_output(f'netsh wlan show profile "{ele[1]}" key=clear',shell=1).decode()
                    set_value=re.findall(r"(Key Content.+:)(.*)",value)
                    print(set_value[0][1])
                    dictionary1[ele[1]]=set_value[0][1]
                except:
                    pass   
            # print(temp)
            self.screen.delete("1.0","end")
            i=1
            for ele,value in dictionary1.items():
                if i==1:
                    self.screen.insert(END,f"Wifi Name \t\t\t\t\t: Wifi password \n")
                    hr="_"*80
                    self.screen.insert(END,f"{hr} \n")
                self.screen.insert(END,f"{i}] {ele   }\t\t\t\t\t: { value} \n")
                i+=1
            self.screen.update()
            self.screen.config(state="disable")
            feedback=tmsg.askyesno("Feedback","Do you like the application..")
            if feedback:
                tmsg.showinfo("Feedback","Thank you!")
            else:
                tmsg.showinfo("Feedback","I will improve our application as per your suggestion..")
            
    def Button(self):

        b1=Button(self.f1,bg="green",text="Auto",font="arial 10 bold")
        b1.pack()
        
        b1.bind("<Button-1>",self.Automation)

    
    
if __name__=="__main__":

    window=App()
    window.title_color()
    window.Tab()
    window.Frame()
    window.Button()
    window.Scroll()
    # window.Automation("hi")
    window.Output()
    window.mainloop()