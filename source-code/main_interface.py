
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:26:14 2019

@author: mgram
"""
import manager
from tkinter import *

from PIL import ImageTk, Image
import os
import sqlite3 



def launchManager():
    with sqlite3.connect("bikecycle.db") as db:
        cursor=db.cursor()   
    cursor.execute("INSERT INTO users(name,age,gender,password,permission,balance) VALUES('Maria',20,'female','a123456','manager',2333.33)")
    cursor.execute("SELECT * FROM users WHERE name = '" + loginEntry.get() + "' AND password = '" + loginPEntry.get() +"' AND permission = 'manager'")
    loginR = cursor.fetchall()
    if len(loginR)>0:
         db.close()    
         manager1 = manager.Manager()
         manager1.mainloop()
    else:
        messagebox.showinfo("Error", "The username/password combination does not exist or does not have the required permission")        
        db.close()    
        
def launchOperator():
    with sqlite3.connect("bikecycle.db") as db:
        cursor=db.cursor()   
        cursor.execute("INSERT INTO users(name,age,gender,password,permission,balance) VALUES('Bob',20,'female','a123456','operator',2333.33)")
        
    cursor.execute("SELECT * FROM users WHERE name = '" + loginEntry.get() + "' AND password = '" + loginPEntry.get() +"' AND permission = 'operator'")
    loginR = cursor.fetchall()
    if len(loginR)>0:
         db.close()    
         os.system('python operator.py')
    else:
        messagebox.showinfo("Error", "The username/password combination does not exist or does not have the required permission")        
        db.close()    
    

    

def launchUser():
    
    os.system('python user.py')

window = Tk()
window.title("BikeCycle - Operator Portal")
window.configure(background='white')
window.geometry("555x300")


loginName = Label(text='Username:',bg='white',font=("Helvetica", 12))
loginEntry = Entry(bg='white')
loginPassword = Label(text='Password:',bg='white',font=("Helvetica", 12))
loginPEntry = Entry(bg='white')    
loginName.place(x=100,y=140)
loginEntry.place(x=190,y=140)
loginPassword.place(x=100,y=165)
loginPEntry.place(x=190,y=165)

btn = Button()
btn["text"] = "Manager Interface"
btn["command"] = launchManager
btn.place(x=140,y=200)

btn2 = Button()
btn2["text"] = "Operator Interface"
btn2["command"] = launchOperator
btn2.place(x=280,y=200)

btn3 = Button()
btn3["text"] = "User Interface app simulation"
btn3["command"] = launchUser
btn3.place(x=140,y=230)

img = ImageTk.PhotoImage(Image.open("images/Logo.png"))
panel = Label(image = img)
panel.place(x=1,y=1) 

window.mainloop()   



