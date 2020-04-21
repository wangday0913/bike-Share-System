# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 13:53:56 2019

@author: 2489279K
"""

#Imports
from tkinter import *
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
import sqlite3 
import time
import datetime  
from datetime import timedelta  
import matplotlib.dates as mdates
import random

userid = ""
rbikeid = ""
journeyID = 0
startTime = datetime.datetime.now()

#update map
def update_map():
    cursor.execute("SELECT * FROM bikes")
    
    bikes = cursor.fetchall()
    markers = gen_marker(bikes)
    
    path = """https://maps.googleapis.com/maps/api/staticmap?center=Glasgow
    &zoom=13
    &size=500x500"""+markers+"""
    &key=""" + apikey
    #print(path) #debug
    
    response = requests.get(path)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    panel2.configure(image = img)
    panel2.image = img
    
#update map in transit
def update_map_transit(x):
    cursor.execute("SELECT * FROM bikes WHERE bike_id = " + str(x))
    
    bikes = cursor.fetchall()
    markers = gen_marker_transit(bikes)
    
    path = """https://maps.googleapis.com/maps/api/staticmap?center=Glasgow
    &zoom=13
    &size=500x500"""+markers+"""
    &key=""" + apikey
    #print(path) #debug
    
    response = requests.get(path)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    panel2.configure(image = img)
    panel2.image = img    

#Generate markers
def gen_marker_transit(x):
    path = ""
    for i in x:
        path = path + "&markers=color:blue%7Clabel:T%7C"+ str(i[3])+","+str(i[4])
    return path

#Generate marker for transit bike
def gen_marker(x):
    path = ""
    for i in x:
        if i[1] == "parked":
            path = path + "&markers=color:green%7Clabel:P%7C"+ str(i[3])+","+str(i[4])
    return path

def add_funds():
    add10_button.place(x=350,y=625)
    add20_button.place(x=390,y=625)
    add30_button.place(x=430,y=625)
    addFunds_Label.place_forget()
    
    #addFunds_button.place_forget()

#Add 10 pounds to balance
def add_10():
    global userid
    global db
    add10_button.place_forget()
    add20_button.place_forget()
    add30_button.place_forget()
    addFunds_Label.place(x=360,y=625)
    totalfunds = float(funds_label['text']) + 10
    funds_label.configure(text=totalfunds)
    cursor.execute("UPDATE users SET balance = " + str(totalfunds) + " WHERE user_id = '" + str(userid) + "'")
    db.commit()

#Add 20 pounds to balance    
def add_20():
    global userid
    global db
    add10_button.place_forget()
    add20_button.place_forget()
    add30_button.place_forget()
    addFunds_Label.place(x=360,y=625)
    totalfunds = float(funds_label['text']) + 20
    funds_label.configure(text=totalfunds)
    cursor.execute("UPDATE users SET balance = " + str(totalfunds) + " WHERE user_id = '" + str(userid) + "'")
    db.commit()

#Add 20 pounds to balance
def add_30():
    global userid
    global db
    add10_button.place_forget()
    add20_button.place_forget()
    add30_button.place_forget()
    addFunds_Label.place(x=360,y=625)
    totalfunds = float(funds_label['text']) + 30
    funds_label.configure(text=totalfunds)
    cursor.execute("UPDATE users SET balance = " + str(totalfunds) + " WHERE user_id = '" + str(userid) + "'")
    db.commit()

#Initialise main interface
def init_main():
    global userid
    userName_label.place(x=30,y=600)    
    userName.place(x=150,y=600)
    wallet_label.place(x=30,y=625)
    funds_label.place(x=150,y=625)
    addFunds_button.place(x=230,y=625)
    startJourney_button.place(x=110,y=850)
    w.place(x=30,y=680)    
    reportFaultButton.place(x=220,y=960)

#Check if login credentials are valid
def login():
    global userid
    cursor.execute("SELECT * FROM users WHERE name = '" + loginEntry.get() + "' AND password = '" + loginPEntry.get() +"'")
    loginR = cursor.fetchall()
    if len(loginR)>0:
        userName.config(text=loginEntry.get())
        userid = loginR[0][0]
        funds_label.configure(text = loginR[0][6])
        print(userid)
        loginEntry.place_forget()
        loginPassword.place_forget()
        loginPEntry.place_forget()
        loginButton.place_forget()
        newUserButton.place_forget()
        init_main()
    else:
        messagebox.showinfo("Error", "The username/password combination does not exist")
        
def register():
    global userid

#Start a journey using a random bikeid
def start_journey():
    global userid
    global journeyID
    global startTime
    global rbikeid
    cursor.execute("SELECT bike_id,bikex,bikey FROM bikes WHERE bike_state = 'parked'")
    tempx = cursor.fetchall()
    randres = random.randrange(len(tempx))
    rbikeid = str(tempx[randres][0])
    rbikex = str(tempx[randres][1])
    rbikey = str(tempx[randres][2])
    startTime = datetime.datetime.now()
    cursor.execute("INSERT INTO journeys(bike_id,user_id, start_time,startx,starty,endx) VALUES("+rbikeid+","+str(userid)+",'" + str(startTime) + "',"+rbikex+","+rbikey+",-4.286210)")
    cursor.execute("SELECT last_insert_rowid()")
    journeyID = cursor.fetchall()[0][0]
    cursor.execute("UPDATE bikes SET bike_state = 'transit' WHERE bike_id = '" + rbikeid + "'")
    startJourney_button.place_forget()
    stopJourney_button.place(x=110,y=850)
    TimeLabel.place(x=30,y=700)
    TimeLabel2.place(x=150,y=700)
    TimeLabel2.configure(text=str(datetime.datetime.now()))
    update_map_transit(rbikeid)
    #db.commit()

#Stop the journey and update database
def stop_journey():
    global userid
    global journeyID
    global startTime
    global endTime
    global rbikeid
    endTime = datetime.datetime.now() + timedelta(minutes=15)
    price = endTime - startTime
    price = float(price.total_seconds()/60)
    price = price*0.5
    TimeLabel3.place(x=30,y=725)
    TimeLabel4.place(x=150,y=725)
    TimeLabel4.configure(text=str(endTime))
    priceLabel.place(x=30,y=750)
    priceLabel1.place(x=150,y=750)
    priceLabel1.configure(text=str(price))
    totalfunds = float(funds_label['text']) + 20
    funds_label.configure(text=totalfunds)
    cursor.execute("UPDATE users SET balance = " + str(funds_label['text']) + " WHERE user_id = " + str(userid))
    cursor.execute("SELECT startx, starty FROM journeys WHERE journey_id = " + str(journeyID))
    tempc = cursor.fetchall()
    cursor.execute("UPDATE journeys SET endx = " + str(tempc[0][0] + 0.003) + ", endy = " + str(tempc[0][1]-0.003) + ", price = " + str(price) + " WHERE journey_id = " + str(journeyID))
    cursor.execute("UPDATE bikes SET bikex = " + str(tempc[0][0] + 0.003) + ", bikey = " + str(tempc[0][1]-0.003) + " WHERE bike_id = " + str(rbikeid))
    stopJourney_button.place_forget()
    faultLabel.place(x=110,y=850)
    faultYesButton.place(x=140,y=875)
    faultNoButton.place(x=190,y=875)
    
#finish journey without a fault
def stop_fault_no():
    cursor.execute("UPDATE bikes SET bike_state = 'parked' WHERE bike_id = '" + rbikeid + "'")
    update_map()    
    faultLabel.place_forget()
    faultYesButton.place_forget()
    faultNoButton.place_forget()
    TimeLabel3.place_forget()
    TimeLabel4.place_forget()
    priceLabel.place_forget()
    priceLabel1.place_forget()
    TimeLabel.place_forget()
    TimeLabel2.place_forget()
    startJourney_button.place(x=110,y=850)
    
def stop_fault_yes():    
    faultLabel.place_forget()
    faultYesButton.place_forget()
    faultNoButton.place_forget()
    faultLabel2.place(x=110,y=850)
    submitFaultButton2.place(x=200,y=875)
    bikeFault.place(x=110,y=875)

def stop_fault_submit():
    cursor.execute("UPDATE bikes SET bike_state = 'faulty', bike_broken = '" + status_var.get() + "' WHERE bike_id = '" + rbikeid + "'")
    update_map()
    faultLabel2.place_forget()
    submitFaultButton.place_forget()
    bikeFault.place_forget()
    TimeLabel3.place_forget()
    TimeLabel4.place_forget()
    priceLabel.place_forget()
    priceLabel1.place_forget()
    TimeLabel.place_forget()
    TimeLabel2.place_forget()
    startJourney_button.place(x=110,y=850)
    
def fault_submit():
    cursor.execute("UPDATE bikes SET bike_state = 'faulty', bike_broken = '" + status_var.get() + "' WHERE bike_id = '" + rbikeid + "'")
    update_map()
    faultLabel2.place_forget()
    submitFaultButton2.place_forget()
    bikeFault.place_forget()
    TimeLabel3.place_forget()
    TimeLabel4.place_forget()
    priceLabel.place_forget()
    priceLabel1.place_forget()
    TimeLabel.place_forget()
    TimeLabel2.place_forget()
    startJourney_button.place(x=110,y=850)   
    reportFaultButton.place(x=220,y=960)

def report_fault():
    global rbikeid
    faultLabel2.place(x=110,y=850)
    submitFaultButton2.place(x=200,y=875)
    startJourney_button.place_forget()
    reportFaultButton.place_forget()
    bikeFault.place(x=110,y=875)
    cursor.execute("SELECT bike_id FROM bikes WHERE bike_state = 'parked'")
    tempx = cursor.fetchall()
    randres = random.randrange(len(tempx))
    rbikeid = str(tempx[randres][0])
    
#initialise main TK window
window = Tk()
window.title("BikeCycle - User Interface")
window.configure(background='white')
window.geometry("562x1000")

img = ImageTk.PhotoImage(Image.open("images/SBG.png"))
panel = Label(image = img)
panel.place(x=1,y=1) 


with sqlite3.connect("bikecycle.db") as db:
    cursor=db.cursor()

#definitions
apikey = "AIzaSyDdgEWGzjCXzTEm-EXr66fDmmraPtJ-qqU"

#*************
#
#Initialise map
#
#*************
cursor.execute("SELECT * FROM bikes")
bikes = cursor.fetchall()
markers = gen_marker(bikes)
    
path = """https://maps.googleapis.com/maps/api/staticmap?center=Glasgow
&zoom=13
&size=500x500"""+markers+"""
&key=""" + apikey
#print(path) #debug

response = requests.get(path)
img_data = response.content
img2 = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
panel2 = Label(image = img2)
panel2.place(x=30,y=60)            

#*************
#
#Create interface items
#
#*************

#Main interface
userName_label = Label(text='Username:',bg='white',font=("Helvetica", 12))
userName = Label(text='Bob',bg='white',font=("Helvetica", 12))
wallet_label = Label(text='Balance (£):',bg='white',font=("Helvetica", 12))
funds_label = Label(text='22',bg='white',font=("Helvetica", 12))
addFunds_button = Button(text="Add funds to wallet",command=add_funds)
add10_button = Button(text="10",command=add_10)
add20_button = Button(text="20",command=add_20)
add30_button = Button(text="30",command=add_30)
addFunds_Label = Label(text='Funds added successfully',bg='white',font=("Helvetica", 12))

#Draw line
w = Canvas(window,width=500,height=10,bg='white',highlightthickness=0,relief='ridge')
w.create_line(0,5,500,5)

#MISC interface items
startJourney_button = Button(text='Start Journey', command=start_journey,bg='#ffb0ff',font=("Helvetica", 40))
stopJourney_button = Button(text='Stop Journey', command=stop_journey,bg='#ffb0ff',font=("Helvetica", 40))
TimeLabel = Label(text='Time started:',bg='white',font=("Helvetica", 12))
TimeLabel2 = Label(text='...',bg='white',font=("Helvetica", 12))      
TimeLabel3 = Label(text='Time ended:',bg='white',font=("Helvetica", 12))
TimeLabel4 = Label(text='...',bg='white',font=("Helvetica", 12))          
priceLabel = Label(text='Price (£):',bg='white',font=("Helvetica", 12))
priceLabel1 = Label(text='...',bg='white',font=("Helvetica", 12))
faultLabel = Label(text='Did you stop due to a fault?',bg='white',font=("Helvetica", 12))
faultYesButton = Button(text='Yes', command=stop_fault_yes,bg='white',font=("Helvetica", 12))
faultNoButton = Button(text='No', command=stop_fault_no,bg='white',font=("Helvetica", 12))
faultLabel2 = Label(text='What is the fault?',bg='white',font=("Helvetica", 12))          
submitFaultButton = Button(text='Submit', command=stop_fault_submit,bg='white',font=("Helvetica", 12))    
submitFaultButton2 = Button(text='Submit', command=fault_submit,bg='white',font=("Helvetica", 12))    
reportFaultButton = Button(text='Report Faulty Bike', command=report_fault,bg='white',font=("Helvetica", 12))    

#create fault dropdown
status_var = StringVar(window)
status_var.set("") 
bikeFault = OptionMenu(window,status_var,"handle","saddle","wheel","axle","chain")  

#Login interface
loginName = Label(text='Username:',bg='white',font=("Helvetica", 12))
loginName.place(x=30,y=600)    

loginEntry = Entry(bg='white')
loginEntry.place(x=150,y=600)    

loginPassword = Label(text='Password:',bg='white',font=("Helvetica", 12))
loginPassword.place(x=30,y=625)    

loginPEntry = Entry(bg='white')
loginPEntry.place(x=150,y=625)    

loginButton = Button(text="Login",command=login)
loginButton.place(x=100,y=650)

newUserButton = Button(text="Register",command=register)
#newUserButton.place(x=150,y=650)

window.mainloop()    
db.close()        


