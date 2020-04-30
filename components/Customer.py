from tkinter import *
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
import _sqlite3
blood = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
############################
root = Tk()
root.geometry("200x200")
global variable
name = StringVar()
age = StringVar()
weight = StringVar()
###########################
def donate():
    var = []

    def example1():
        def print_sel():
            print(cal.selection_get())
            var.append(cal.selection_get())
            # cal.see(datetime.date(year=2016, month=2, day=5))
            var1 = str(var[0])
            l4.config(text= var1)
            top.destroy()

        top = Toplevel(donate)

        import datetime
        today = datetime.date.today()

        mindate = today
        maxdate = today + datetime.timedelta(days=5)

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1", year=2018, month=2, day=5)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="ok", command=print_sel ).pack()

    def submit():
        var1 = str(var[0])
        uname = e.get()
        ag = e1.get()
        wt = e2.get()
        bt = variable.get()
        if(len(uname)>0 and type(uname)==str):
            con = _sqlite3.connect("oneblood.db")
            with con:
                cursor = con.cursor()
            cursor.execute("Insert into Donate(uname,age,weight,date,blood_group) values(?,?,?,?,?)",
                           (uname, ag, wt, var1, bt,))
            con.commit()
            donate.destroy()
        else:
            lo.config(text='invalid values')

    donate = Tk()
    donate.geometry("220x200")
    donate.title("Donate Blood")
    l = Label(donate, text="Donor's Name:")
    l.grid(row=0, column=0)

    e = Entry(donate,textvariable=name)
    e.grid(row=0, column=1)

    l1 = Label(donate,text="Select Time:")
    l1.grid(row=1,column=0)
    ttk.Button(donate, text='Calendar', command=example1).grid(row=1, column=1)

    l2 = Label(donate,text="Enter Age:")
    l2.grid(row=2,column=0)

    e1 = Entry(donate,textvariable=age)
    e1.grid(row=2,column=1)

    l3 = Label(donate, text="Enter weight")
    l3.grid(row=3, column=0)

    e2 = Entry(donate,textvariable=weight)
    e2.grid(row=3,column=1)

    ln = Label(donate, text="Selected Time:")
    ln.grid(row=4, column=0)

    l4 = Label(donate, text="")
    l4.grid(row=4,column=1)

    l5 = Label(donate, text="Blood type:")
    l5.grid(row=5, column=0)

    variable = StringVar(donate)
    variable.set(blood[0])
    opt = OptionMenu(donate, variable, *blood)
    opt.grid(row=5, column=1)

    b = Button(donate, text="submit",fg="red", height="2", width="10", command=submit)
    b.grid(row=6,column=1)

    lo = Label(donate,text="",fg='red')
    lo.grid(row=7,column=1)
    donate.mainloop()

def request():
    def submit():
        name = e.get()
        ag = e1.get()
        wt = e2.get()
        bt = variable.get()
        qt = e3.get()
        con = _sqlite3.connect("oneblood.db")
        with con:
            cursor = con.cursor()
            getqty = con.cursor()
        getqty.execute('select qunatity from quantity where blood_group=?', (bt,))
        v = getqty.fetchone()
        v1 = v[0]

        if(len(name)>0 and type(name)==str):
            if (int(qt) < int(v1)):
                cursor.execute("Insert into Receive values(?,?,?,?,?)", (name, ag, wt, qt, bt))
                con.commit()
                request.destroy()
            else:
                lk.config(text='Sorry! This much blood is not available')
        else:
            lk.config(text='invalid values')

    request = Tk()
    request.geometry("250x200")

    l1 = Label(request, text="Name of the patient:")
    l1.grid(row=0, column=0)

    e = Entry(request,textvariable='')
    e.grid(row=0,column=1)

    l2 = Label(request, text="Patient's Age:")
    l2.grid(row=1, column=0)

    e1 = Entry(request,textvariable='')
    e1.grid(row=1, column=1)

    l3 = Label(request, text="Patient's weight")
    l3.grid(row=2, column=0)

    e2 = Entry(request,textvariable='')
    e2.grid(row=2, column=1)

    l4 = Label(request, text="Blood type:")
    l4.grid(row=3, column=0)

    variable = StringVar(request)
    variable.set(blood[0])
    opt = OptionMenu(request, variable, *blood)
    opt.grid(row=3, column=1)

    l5 = Label(request, text="Quantity Required(ml)")
    l5.grid(row=4, column=0)

    e3 = Entry(request,textvariable='')
    e3.grid(row=4, column=1)

    b = Button(request, text="Submit",height=2,width=10,fg='red', command=submit)
    b.grid(row=5, column=1)

    lk = Label(request,text="",fg='red')
    lk.grid(row=6,column=0)

    request.mainloop()


Label(root,text="OneBlood", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
Label(root,text="").pack()
root.geometry("300x300")
root.title("Customer Dashboard")
Button(root,text="Donate Blood", height="2", width="30",command=donate).pack()
Label(root,text="").pack()
Button(root,text="Request Blood", height="2", width="30", command=request).pack()
Label(root,text="").pack()
root.mainloop()
############################################################
