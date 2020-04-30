from tkinter import *
import _sqlite3
import os
con = _sqlite3.connect("oneblood.db")
blood = ['Select Blood Type','A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("250x300")

    global username
    global password
    global username_entry
    global password_entry
    global address_entry
    global phone_no_entry
    global variable
    global phone_no
    global address
    global l
    username = StringVar()
    password = StringVar()
    phone_no = StringVar()
    address = StringVar()

    Label(register_screen, text="Please enter details below", fg="red").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    variable = StringVar(register_screen)
    variable.set(blood[0])
    opt = OptionMenu(register_screen, variable, *blood)
    opt.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    address_lable = Label(register_screen, text="Address * ")
    address_lable.pack()
    address_entry = Entry(register_screen, textvariable=address)
    address_entry.pack()
    phone_no_lable = Label(register_screen, text="Contact No. * ")
    phone_no_lable.pack()
    phone_no_entry = Entry(register_screen, textvariable=phone_no)
    phone_no_entry.pack()
    l = Label(register_screen, text="")
    l.pack()
    Button(register_screen, text="Register", width=10, height=1, bg="red", command=register_user).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("350x250")
    Label(login_screen, text="Please enter details below to login",fg="red").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10,bg="red", height=1, command=login_verify).pack()


# Implementing event on register button

def register_user():
    cname = username.get()
    btyp = variable.get()
    add = address.get()
    phone = phone_no.get()
    pas = password.get()
    if(len(cname)> 0 and btyp != 'Select blood type' and len(add)>0 and len(pas)>=6 and len(phone) == 10):
        with con:
            cursor = con.cursor()
        #cursor.execute("Create table customer(name TEXT,bloodtyp TEXT,password TEXT,address TEXT,phoneno TEXT)")
        cursor.execute("Insert into customer(name,bloodtyp,password,address,phoneno) values(?,?,?,?,?)",
                       (cname, btyp, pas, add, phone))
        con.commit()
        register_screen.destroy()
    else:
        print('error')
        l.config(text='Incorrect form values', fg='red')

# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    checku = ""
    checkp = ""
    with con:
        cursor = con.cursor()
    cursor.execute("select * from customer")
    rows = cursor.fetchall()
    for i in rows:

        if username1 in i and password1 in i:
            checku = username1
            checkp = password1

    if checkp == password1 and checku == username1:
        login_sucess()

    elif username1 == "admin" and password1 == "admin":
        import admin

    else:
        user_not_found()

    con.commit()



# Designing popup for login success

def login_sucess():
    import Customer
# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="OneBlood", bg="red", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()


main_account_screen()