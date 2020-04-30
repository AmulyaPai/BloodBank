import _sqlite3
import matplotlib.pyplot as plt
import dateutil.parser
from tkinter import *
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def donor():
    root = Tk()
    d = Label(root, text='Donors')
    d.pack()
    f = Frame(root)
    f.pack()


    import _sqlite3
    con = _sqlite3.connect("oneblood.db")
    with con:
        cursor = con.cursor()
    cursor.execute("select * from Donate")
    root.geometry("400x300")
    rows = cursor.fetchall()
    h=1
    Label(f,text ="name",relief='solid',width=10).grid(row=0,column=0)
    Label(f,text ="age",relief='solid',width=10).grid(row=0,column=1)
    Label(f,text ="weight",relief='solid',width=10).grid(row=0,column=2)
    Label(f,text ="date",relief='solid',width=10).grid(row=0,column=3)
    Label(f,text ="blood_grp",relief='solid',width=10).grid(row=0,column=4)

    for i,j,k,l,x in rows:

        Label(f,text = i,relief='groove',width=10).grid(row=h,column=0)
        Label(f,text = j,relief='groove',width=10).grid(row=h,column=1)
        Label(f,text = k,relief='groove',width=10).grid(row=h,column=2)
        Label(f,text = l,relief='groove',width=10).grid(row=h,column=3)
        Label(f,text = x,relief='groove',width=10).grid(row=h,column=4)
        h = h+1


    root.mainloop()

def req():
    def dell(name,qty,type):

        print(name,qty,type)
        import _sqlite3
        con = _sqlite3.connect('oneblood.db')
        with con:
            dec = con.cursor()
            delqty = con.cursor()
            getqty = con.cursor()
        getqty.execute('select qunatity from quantity where blood_group=?',(type,))
        existing_qty = getqty.fetchone()
        print(existing_qty)
        remaining_qty = int(existing_qty[0]) - int(qty)
        dec.execute('delete from Receive where uname = ?',(name,))
        delqty.execute('update quantity set qunatity=? where blood_group=?',(remaining_qty,type))
        con.commit()
        root.destroy()
        f.after(500,req())

    root = Tk()
    d = Label(root, text='Receiver')
    d.pack()
    f = Frame(root)
    f.pack()


    import _sqlite3
    con = _sqlite3.connect("oneblood.db")
    with con:
        cursor = con.cursor()
    cursor.execute("select * from Receive")
    root.geometry("500x300")
    rows = cursor.fetchall()
    h=1
    Label(f,text ="name",relief='solid',width=10).grid(row=0,column=0)
    Label(f,text ="age",relief='solid',width=10).grid(row=0,column=1)
    Label(f,text ="weight",relief='solid',width=10).grid(row=0,column=2)
    Label(f,text ="quantity",relief='solid',width=10).grid(row=0,column=3)
    Label(f,text ="bloodtype",relief='solid',width=10).grid(row=0,column=4)
    Label(f,text ="fill request",relief='solid',width=10).grid(row=0,column=5)

    for i,j,k,l,m in rows:

        Label(f,text = i,relief='groove',width=10).grid(row=h,column=0)
        Label(f,text = j,relief='groove',width=10).grid(row=h,column=1)
        Label(f,text = k,relief='groove',width=10).grid(row=h,column=2)
        Label(f,text = l,relief='groove',width=10).grid(row=h,column=3)
        Label(f,text = m,relief='groove',height=1,width=10).grid(row=h,column=4)
        b=Button(f,text="Fill",width=10,height=1,command= lambda:dell(i,l,m))
        b.grid(row=h,column=5)
        h = h+1
    f.after(300)
    root.mainloop()

from tkinter import *
main_screen1 = Tk()
Label(main_screen1,text="OneBlood", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
Label(main_screen1,text="").pack()
main_screen1.geometry("400x500")
main_screen1.title("Admin Dashboard")
Button(main_screen1,text="Doner", height="2", width="30",command=donor).pack()
Label(main_screen1,text="").pack()
Button(main_screen1,text="Receiver", height="2", width="30", command=req).pack()
Label(main_screen1,text="").pack()

tod = datetime.datetime.today()
today = dateutil.parser.parse(str(tod)).date()
con = _sqlite3.connect("oneblood.db")
with con:
    cursor = con.cursor()
    cursordel = con.cursor()
    cursorin = con.cursor()
    cursor1 = con.cursor()
    existing_val = con.cursor()
    addqty = con.cursor()
cursor.execute("select * from Donate")
rows = cursor.fetchall()
for i, j, k, l, x in rows:
    d = dateutil.parser.parse(l).date()
    n = str(d)
    a = n[0:10]
    print(a)
    if d < today:
        cursorin.execute("insert into donation_completed values(?,?,?,?,?)", (i, j, k, l, "A+"))
        existing_val.execute('select qunatity from quantity where blood_group=?',(x,))
        ext_qty = existing_val.fetchone()
        remaining = ext_qty[0]+100
        addqty.execute('update quantity set qunatity=? where blood_group=?',(remaining,x))
        cursordel.execute("delete from Donate where date = ?", (a,))
        print('deleted')
cursor1.execute("select * from quantity")
con.commit()
rows = cursor1.fetchall()
qty =[]
lbl =[]
for i,j in rows:
     qty.append(i)
     lbl.append(j)

figure1 = plt.Figure(figsize=(4,3), dpi=100)
subplot1 = figure1.add_subplot(111)
subplot1.bar(qty,lbl, color = 'red')
# plt.text(qty,lbl,str(qty))
bar1 = FigureCanvasTkAgg(figure1, main_screen1)
bar1.get_tk_widget().pack(expand=0)
main_screen1.mainloop()
