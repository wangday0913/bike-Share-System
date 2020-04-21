import tkinter as tk
from tkinter import ttk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from dateutil.relativedelta import relativedelta

import datetime

import sqlite3

with sqlite3.connect("bikecycle.db")as db:
    cursor = db.cursor()


# lineChart
class LineChart(tk.Tk):

    def __init__(self, master=None):
        super().__init__()
        self.title("LineChart")
        self.geometry("1000x600")
        self.initFilter()
        self.initLineChart()

    #start-end time
    def initFilter(self):
        self.filterArea1 = tk.Frame(self)
        self.filterArea1.pack(fill=tk.X, expand=0)
        startTimeLabel = tk.Label(self.filterArea1, text="Start time")
        startTimeLabel.pack(side="left")

        self.startYearEntry = tk.Entry(self.filterArea1, bd=1)
        self.startYearEntry.pack(side="left")
        self.startYearEntry.insert(0, 2019)
        startYearLabel = tk.Label(self.filterArea1, text="Year")
        startYearLabel.pack(side="left")

        self.startMonthEntry = tk.Entry(self.filterArea1, bd=1)
        self.startMonthEntry.pack(side="left")
        self.startMonthEntry.insert(0, 1)
        startMonthLabel = tk.Label(self.filterArea1, text="Month")
        startMonthLabel.pack(side="left")

        self.startDayEntry = tk.Entry(self.filterArea1, bd=1)
        self.startDayEntry.pack(side="left")
        self.startDayEntry.insert(0, 1)
        startDayLabel = tk.Label(self.filterArea1, text="Day")
        startDayLabel.pack(side="left")

        self.filterArea2 = tk.Frame(self)
        self.filterArea2.pack(fill=tk.X, expand=0, pady=5)

        endTimeLabel = tk.Label(self.filterArea2, text="End time  ")
        endTimeLabel.pack(side="left")
        self.endYearEntry = tk.Entry(self.filterArea2, bd=1)
        self.endYearEntry.pack(side="left")
        self.endYearEntry.insert(0, 2019)
        endYearLabel = tk.Label(self.filterArea2, text="Year")
        endYearLabel.pack(side="left")

        self.endMonthEntry = tk.Entry(self.filterArea2, bd=1)
        self.endMonthEntry.pack(side="left")
        self.endMonthEntry.insert(0, 12)
        endMonthLabel = tk.Label(self.filterArea2, text="Month")
        endMonthLabel.pack(side="left")

        self.endDayEntry = tk.Entry(self.filterArea2, bd=1)
        self.endDayEntry.pack(side="left")
        self.endDayEntry.insert(0, 30)
        endDayLabel = tk.Label(self.filterArea2, text="Day")
        endDayLabel.pack(side="left")

    # visualisation report (Initialise)
    def initLineChart(self):

        self.filterArea3 = tk.Frame(self)
        self.filterArea3.pack(fill=tk.X, expand=0)

        self.msgLabel = tk.Label(self.filterArea3, text="", fg='red')
        self.msgLabel.pack(side="top")

        self.btn = tk.Button(self.filterArea1)
        self.btn["text"] = "Bike Amount-time"
        self.btn["command"] = self.showLineChart2
        self.btn.pack(side="top")

        self.btn = tk.Button(self.filterArea2)
        self.btn["text"] = "income-time"
        self.btn["command"] = self.showLineChart
        self.btn.pack(side="top")

        self.lineChart = tk.Frame(self)
        self.lineChart.pack(fill=tk.X, expand=0)

        f = plt.figure(figsize=(8, 5), dpi=100)
        self.f_plot = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, self.lineChart)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    #chose data to show in limited time
    def limitTime(self, start, end, option):

        period = end - start

        if period.days <= 60:
            tperiod = '%d'
        else:
            tperiod = '%m'

        if option == 1:
            cursor.execute("SELECT sum(journeys.price),journeys.start_time FROM journeys "
                           "WHERE journeys.start_time>=? AND journeys.start_time<=? "
                           "GROUP BY strftime(?,journeys.start_time)", [start, end, tperiod])
        else:
            cursor.execute("SELECT count(*),journeys.start_time FROM journeys "
                           "WHERE journeys.start_time>=? AND journeys.start_time<=? "
                           "GROUP BY strftime(?,journeys.start_time)", [start, end, tperiod])

        # put time,price in dictionary
        time_item = {}
        for i in cursor.fetchall():
            t = i[1]
            # transfer value to "datetime" type
            t = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
            time_item[t] = i[0]

        mintime = min(time_item.keys()).date()
        maxtime = max(time_item.keys()).date()

        # make a dictionary contain time-price in limited time
        valuexy = {}

        if tperiod=='%m':
            mintime = datetime.date(year=mintime.year, month=mintime.month, day=start.day)
            temp=mintime
            while temp >= mintime and temp < maxtime:

                for t in time_item.keys():
                    if t.year == temp.year and t.month == temp.month:
                        valuexy[temp] = time_item[t]
                if temp not in valuexy.keys():
                    valuexy[temp] = 0

                temp = temp + relativedelta(months=1)

        elif tperiod=='%d':
            temp = mintime
            while temp >= mintime and temp < maxtime:

                for t in time_item.keys():
                    if t.year == temp.year and t.month == temp.month and t.day==temp.day:
                        valuexy[temp] = time_item[t]
                if temp not in valuexy.keys():
                    valuexy[temp] = 0

                temp = temp + relativedelta(days=1)

        return(valuexy)

    # check whether the value of date is correct
    def checkDate(self):

        startyear = self.startYearEntry.get()
        startmonth = self.startMonthEntry.get()
        startday = self.startDayEntry.get()

        endyear = self.endYearEntry.get()
        endmonth = self.endMonthEntry.get()
        endday = self.endDayEntry.get()

        start = startyear + "-" + startmonth + "-" + startday
        end = endyear + "-" + endmonth + "-" + endday

        try:

            if startyear == "" or startmonth == "" or startday == "" or \
                    endyear == "" or endmonth == "" or endday == "":
                tk.messagebox.showinfo(title='Error', message="tha blanks shouldn't be empty")
                return

            else:
                startTime = datetime.datetime.strptime(start, "%Y-%m-%d")
                endTime = datetime.datetime.strptime(end, "%Y-%m-%d")
                if startTime > endTime:
                    tk.messagebox.showinfo(title='Error', message='endTime should bigger than startTime')
                    return
        except:
            tk.messagebox.showinfo(title='Error', message='please enter the right date number in the blank')
            return

        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%d")
            end = datetime.datetime.strptime(end, "%Y-%m-%d")
        except Exception:
            tk.messagebox.showinfo(title='Error', message='please enter the right date number in the blank')
            return

        return(start,end)

    #time-price line chart
    def showLineChart(self):
        self.f_plot.clear()

        # put the time and price value in list to show x-y label
        start,end = self.checkDate()
        value=self.limitTime(start,end,1)
        timex = []
        pricey = []
        for i in value.keys():
            t = i.isoformat()
            timex.append(t)
            pricey.append(value[i])

        self.f_plot.plot(timex, pricey)

        plt.title("Trend Chart of Income Change")
        plt.xlabel("Date", )
        plt.ylabel("Amount(dollars)")
        plt.gcf().autofmt_xdate()  # Rotate the x-label automatically

        message = "Within the period you chose:Data from " + str(min(value.keys())) + " and " + str(max(value.keys())) \
                  + " in database can be accessed."
        self.msgLabel.config(text=message)

        self.canvas.draw()

    # time-usage amount line chart
    def showLineChart2(self):
        self.f_plot.clear()

        # put the time and amount value in list to show x-y label
        start,end = self.checkDate()
        value=self.limitTime(start,end,2)

        timex = []
        amounty = []
        for i in value.keys():
            t = i.isoformat()
            timex.append(t)
            amounty.append(value[i])

        self.f_plot.plot(timex, amounty)

        plt.title("Trend Chart of Amount of Bike Usage Change")
        plt.xlabel("Date", )
        plt.ylabel("Amount(bikes)")
        plt.gcf().autofmt_xdate()  # Rotate the x-label automatically

        message = "Within the period you chose:Data from " + str(min(value.keys())) + " and " + str(max(value.keys())) \
                  + " in database can be accessed."
        self.msgLabel.config(text=message)

        self.canvas.draw()


# piechart
class PieChart(tk.Tk):

    def __init__(self, master=None):
        super().__init__()

        self.title("PieChart")
        self.geometry("1000x600")
        self.initPieChart()

    def initPieChart(self):
        self.buttonArea = tk.Frame(self)
        self.buttonArea.pack(side="left", padx=5, pady=5, fill=tk.X, expand=0)
        self.btn1 = tk.Button(self.buttonArea)
        self.btn1["text"] = "gender"
        self.btn1["command"] = self.showPieChart1
        self.btn1.pack(side="top")
        # button of Pie Chart_age
        self.btn2 = tk.Button(self.buttonArea)
        self.btn2["text"] = "age"
        self.btn2["command"] = self.showPieChart2
        self.btn2.pack(side="top")
        # button of Pie Chart_broken part
        self.btn3 = tk.Button(self.buttonArea)
        self.btn3["text"] = "broken_part"
        self.btn3["command"] = self.showPieChart3
        self.btn3.pack(side="top")

        self.pieChart = tk.Frame(self)
        self.pieChart.pack(side="left", padx=5, pady=5, fill=tk.X, expand=0)
        f = plt.figure(figsize=(8, 5), dpi=100)
        self.f_plot = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, self.pieChart)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    # piechart-gender
    def showPieChart1(self):
        self.f_plot.clear()

        labels = ['male', 'female']
        cursor.execute("SELECT users.gender FROM users WHERE permission=='customer'")
        m = 0
        f = 0
        for x in cursor.fetchall():
            if x[0] == "male":
                m = m + 1
            else:
                f = f + 1

        sizes = [m, f]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
        plt.title("Ratio Distribution of User's Gender")
        self.canvas.draw()

    # piechart-age
    def showPieChart2(self):
        self.f_plot.clear()

        labels = ['below 20', 'between 20-30', 'between 30-40', 'over40']
        cursor.execute("SELECT users.age FROM users")
        a2 = 0
        a3 = 0
        a4 = 0
        a5 = 0
        for age in cursor.fetchall():
            age = int(age[0])
            if age <= 20:
                a2 = a2 + 1
            elif age <= 30:
                a3 = a3 + 1
            elif age <= 40:
                a4 = a4 + 1
            else:
                a5 = a5 + 1

        sizes = [a2, a3, a4, a5]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
        plt.title("Ratio Distribution of User's age")
        self.canvas.draw()

    # piechart-broken part
    def showPieChart3(self):
        self.f_plot.clear()

        labels = ['handle', 'saddle', 'wheel', 'axle', 'chain']
        cursor.execute("SELECT bikes.bike_broken FROM bikes")
        h = 0
        s = 0
        w = 0
        a = 0
        c = 0
        for part in cursor.fetchall():
            if part[0] == 'handle':
                h = h + 1
            elif part[0] == 'saddle':
                s = s + 1
            elif part[0] == 'wheel':
                w = w + 1
            elif part[0] == 'axle':
                a = a + 1
            else:
                c = c + 1

        sizes = [h, s, w, a, c]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
        plt.title("Ratio Distribution of Damaged Parts of the Vehicles")
        self.canvas.draw()


# main page (contain journey table)
class Manager(tk.Tk):

    def __init__(self, master=None):
        super().__init__()
        LineChart.initFilter(self)
        self.title("Hello Bike")
        self.geometry("1000x600")
        self.initToolBar()

    # first page
    def initToolBar(self):
        self.butonArea = tk.Frame(self)
        self.butonArea.pack(side="right", padx=5, pady=5)

        # button of table
        self.testBtn = tk.Button(self.butonArea)
        self.testBtn["text"] = "showdata"
        self.testBtn["command"] = self.getJourney
        self.testBtn.pack(side="top")
        # button of Line charts
        self.testBtn1 = tk.Button(self.butonArea)
        self.testBtn1["text"] = "lineChart"
        self.testBtn1["command"] = self.showReportL
        self.testBtn1.pack(side="top")
        # button of Pie Chart_gender
        self.testBtn2 = tk.Button(self.butonArea)
        self.testBtn2["text"] = "pieChart"
        self.testBtn2["command"] = self.showReportP1
        self.testBtn2.pack(side="top")
        #massage label
        self.msgLabel = tk.Label(self.butonArea, text="", fg='white',width=25,height=5,wraplength=200)
        self.msgLabel.pack(side="top", pady=5)

        # initial table
        columns = ("Journey ID", "Time", "Price($)")
        self.treeview = ttk.Treeview(self, height=8, show="headings", columns=columns)
        for column in columns:
            self.treeview.column(column, width=255, anchor='center')
            self.treeview.heading(column, text=column,command=lambda _col=column: self.tree_sort_column(self.treeview, _col, False))
        self.treeview.pack(side="left", fill="both",padx=10)

        #self.filterArea3 = tk.Frame(self)
        #self.filterArea3.pack(side="right",fill=tk.X, expand=0)



    # tree_sort_column-can only sort by time correctly now
    def tree_sort_column(self, tv, colName, re):
        l = [(tv.set(itemID, colName), itemID) for itemID in tv.get_children('')]
        #print(l, tv.set('I001', '#1'))
        l.sort(reverse=re)
        # rearrange items in sorted positions
        for index, (val, itemID) in enumerate(l):
            # print(index,val,'itemID:',itemID)
            tv.move(itemID, '', index)
        re = not re
        tv.heading(colName, command=lambda: self.tree_sort_column(tv, colName, re))

    # showdata on table
    def getJourney(self):

        self.delJourney()
        start,end = LineChart.checkDate(self)
        self.dataList = []
        cursor.execute("SELECT journey_id, start_time, price from journeys "
                       "WHERE journeys.start_time>=? AND journeys.start_time<=? ",[start,end])
        totalprice=0
        for x in cursor.fetchall():
            x2=round(x[2],2)
            self.dataList.append([x[0], x[1], x2])
            totalprice=totalprice+x[2]

        for i in range(len(self.dataList)):
            self.treeview.insert('', i, values=(self.dataList[i][0], self.dataList[i][1], self.dataList[i][2]))

        totalprice=round(totalprice,2)
        message = "Toal income during the period:" + str(totalprice)+" dollars"
        self.msgLabel.config(text=message,bg='grey')

    # clear table
    def delJourney(self):
        temp = self.treeview.get_children()
        for i in temp:
            print(i)
        [self.treeview.delete(i) for i in temp]

    def showReportL(self):
        lineChart = LineChart()
        lineChart.mainloop()
        db.close()

    def showReportP1(self):
        pieChart = PieChart()
        pieChart.mainloop()
        db.close()


if __name__ == "__main__":
    manager = Manager()
    manager.mainloop()
    db.close()