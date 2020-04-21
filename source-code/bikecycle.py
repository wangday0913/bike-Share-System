# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 15:36:35 2019

@author: 2454120G
"""

import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta


with sqlite3.connect("bikecycle.db") as db:
    cursor=db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS bikes(
    bike_id integer PRIMARY KEY, 
    bike_state text NOT NULL CHECK(bike_state=='faulty' or bike_state=='parked' or bike_state=='transit'), 
    bike_broken text CHECK(bike_broken=='handle' or bike_broken=='saddle' or bike_broken=='wheel' 
    or bike_broken=='axle'or bike_broken=='chain'),
    bikex float NOT NULL,
    bikey float NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id integer PRIMARY KEY, 
    name text NOT NULL, 
    age text, 
    gender text CHECK(gender=='male' or gender=='female'),
    password text NOT NULL,
    permission text NOT NULL CHECK(permission=='customer' or permission=='operator' or permission=='manager'),
    balance float NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS stations(
    station_id integer PRIMARY KEY, 
    station_name text NOT NULL, 
    stationx float NOT NULL,
    stationy float NOT NULL);""")


cursor.execute("""CREATE TABLE IF NOT EXISTS journeys(
    journey_id integer PRIMARY KEY, 
    bike_id integer, 
    user_id integer, 
    start_time datetime DEFAULT (datetime('now','localtime')),
    end_time datetime DEFAULT (datetime('now', 'localtime')),
    price float,
    startx float NOT NULL,
    starty float NOT NULL,
    endx float,
    endy float);""")




"""
#insert testdata into users
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
               "VALUES(2,'Mike',20,'female','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(9,'Caleb',34,'male','a123456','customer',2333.33)")

cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(10,'Adam',46,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(11,'Alva',47,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(12,'Ethan',29,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(13,'Zhao',27,'female','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(14,'Macus',37,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(15,'Alex',35,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(16,'Colin',30,'male','a123456','customer',2333.33)")

cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
               "VALUES(17,'Ann',17,'female','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(1,'Tom',34,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(3,'Mary',46,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(4,'Tommy',47,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(5,'Lily',28,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(6,'Danyu',27,'female','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(7,'Xiaoyu',39,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(8,'Emma',35,'male','a123456','customer',2333.33)")
cursor.execute("INSERT INTO users(user_id,name,age,gender,password,permission,balance)"
              "VALUES(18,'John',61,'male','a123456','customer',2333.33)")

          
#insert testdata into bikes
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(1,'faulty','handle',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bikex,bikey) VALUES(2,'parked',55.852300,-4.252354)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bikex,bikey) VALUES(3,'transit',55.850602,-4.258113)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bikex,bikey) VALUES(4,'parked',55.863091,-4.257114)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(5,'faulty','handle',55.875043,-4.231181)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bikex,bikey) VALUES(6,'transit',55.8722291,-4.228331)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(7,'faulty','handle',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(8,'faulty','handle',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bikex,bikey) VALUES(9,'transit',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(10,'faulty','axle',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(11,'faulty','handle',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(12,'faulty','saddle',55.852300,-4.252354)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(13,'faulty','handle',55.850602,-4.258113)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(14,'faulty','saddle',55.863091,-4.257114)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(15,'faulty','wheel',55.875043,-4.231181)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(16,'faulty','axle',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(17,'faulty','chain',55.8722291,-4.286210)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(18,'faulty','saddle',55.852300,-4.252354)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(19,'faulty','chain',55.850602,-4.258113)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(20,'faulty','saddle',55.863091,-4.257114)")
cursor.execute("INSERT INTO bikes(bike_id,bike_state,bike_broken,bikex,bikey) VALUES(21,'faulty','wheel',55.875043,-4.231181)")


#insert data into journeys
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(1,2,1,'2019-10-16 12:00',12,55.8722291,-4.286210,55.850602,-4.258113)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(2,3,9,'2019-10-16 13:00:00',55.850602,-4.258113,12,55.8722291,-4.2862103)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(3,5,10,'2019-10-15 19:00:00',40,55.8722291,-4.286210,55.852300,-4.252354)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(4,7,11,'2019-10-14 16:00:00',48,55.8722291,-4.286210,55.863091,-4.257114)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(5,10,12,'2019-10-16 13:00:00',8,55.8722291,-4.286210,55.850602,-4.258113)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(6,12,13,'2019-10-16 14:00:09',9.99,55.863091,-4.257114,55.850602,-4.258113)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(7,15,14,'2019-10-16 14:00:03',9.99,55.863091,-4.257114,55.850602,-4.258113)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(8,9,15,'2019-10-16 14:00:00',9.99,55.863091,-4.257114,55.850602,-4.258113)")
cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,price,startx,starty,endx,endy)"
               "VALUES(9,8,16,'2019-10-16 14:00:08',9.99,55.863091,-4.257114,55.850602,-4.258113)")



#insert data into journeys
import datetime,random

def randomtimes(start, end,frmt="%Y-%m-%d %H:%M:%S"):
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    time=random.random() * (etime - stime) + stime
    time=time.strftime(frmt)
    time=datetime.datetime.strptime(time,frmt)
    return time

id1=128
for i in range(111):

    id1=id1+1
    bike_id=random.randint(1,21)
    user_id=random.randint(1,18)
    start_time=randomtimes('2019-01-01 00:00:00','2019-12-01 00:00:00')
    #start_time=start_time-datetime.timedelta(seconds=start_time.seconds)
    m=random.randint(120,12000)
    end_time=start_time+datetime.timedelta(seconds=m)
    price=(end_time-start_time).seconds*0.05
    startx=random.uniform(55,56)
    starty=random.uniform(-4,-5)
    endx=random.uniform(55,56)
    endy=random.uniform(-4,-5)
    cursor.execute("INSERT INTO journeys(journey_id,bike_id,user_id, start_time,end_time,price,startx,starty,endx,endy)"
                   "VALUES(?,?,?,?,?,?,?,?,?,?)",[id1,bike_id,user_id,start_time,end_time,price,startx,starty,endx,endy])


"""


db.commit()
db.close()

