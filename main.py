from tkinter import *
from PIL import ImageTk ,Image
import mysql.connector
import random

def datainsert(d):
    mydb = mysql.connector.connect(host="localhost",
                                   user="root",
                                   password="Chandu@2003",
                                   database="heritage")
    cursor = mydb.cursor()
    ins = ("INSERT INTO account( Accountno, Name, Accounttype, deposit)"
           "VALUES (%s,%s,%s,%s)")
    x = tuple(d.keys())
    z = x[0]
    y = d[z]
    data = (z, y[0], y[1], y[2])
    cursor.execute(ins, data)
    mydb.commit()

def create_account():
    def save_account():
        accholder = name_entry.get()
        acc_type = account_type_var.get()
        account_num = random.randrange(10*11, 10*12)
        if acc_type == 1 or acc_type == 2:
            result_label.config(
                text=f"Dear {accholder}, your {choices[acc_type]} account is successfully created. Your Account Number is {account_num}"
            )
            initial_deposit = int(deposit_entry.get())
            balance_label.config(text=f"Your Balance is {initial_deposit}")
            dict1 = {account_num: (accholder, choices[acc_type], initial_deposit)}
            datainsert(dict1)
        else:
            result_label.config(text="Please Enter either 1 for savings account or 2 for current account")

    win = Tk()
    win.title("Create Account")

    choices = {1: "Savings", 2: "Current"}

    # Account Holder's Name
    label_name = Label(win, text="Account Holder's Name:")
    label_name.pack()
    name_entry = Entry(win)
    name_entry.pack()

    # Account Type
    label_type = Label(win, text="Account Type:")
    label_type.pack()

    account_type_var = IntVar()
    account_type_var.set(1)  # Default value
    radio_savings = Radiobutton(win, text="Savings", variable=account_type_var, value=1)
    radio_savings.pack()
    radio_current = Radiobutton(win, text="Current", variable=account_type_var, value=2)
    radio_current.pack()

    # Initial Deposit
    label_deposit = Label(win, text="Initial Deposit:")
    label_deposit.pack()
    deposit_entry = Entry(win)
    deposit_entry.pack()

    # Save Account Button
    save_button = Button(win, text="Save Account", command=save_account)
    save_button.pack()

    # Display Result
    result_label = Label(win, text="")
    result_label.pack()

    balance_label = Label(win, text="")
    balance_label.pack()

    win.mainloop()

def check_balance():
    def check():
        acc_num = int(acc_num_entry.get())
        acc_holder_name = name_entry.get()

        for i in result:
            if i[1] == acc_num:
                balance = i[3]
                result_label.config(text=f"Dear {acc_holder_name}, Your Balance is {balance}.")
                break
        else:
            result_label.config(text='''This account does not exist:
                   Do you want to create a new Account?
                   1. Yes 
                   2. No''')

    win1 = Tk()
    win1
    mydb = mysql.connector.connect(host="localhost",
                                   user="root",
                                   password="Chandu@2003",
                                   database="heritage")
    cursor = mydb.cursor()
    query = 'SELECT Name, Accountno, Accounttype, deposit FROM account'
    cursor.execute(query)
    result = cursor.fetchall()

    label_name = Label(win1, text="Account Holder's Name:")
    label_name.pack()
    name_entry = Entry(win1)
    name_entry.pack()

    label_acc_num = Label(win1, text="Account Number:")
    label_acc_num.pack()
    acc_num_entry = Entry(win1)
    acc_num_entry.pack()

    check_button = Button(win1, text="Check Balance", command=check)
    check_button.pack()

    result_label = Label(win1, text="")
    result_label.pack()

    win1.mainloop()

def depositamount():
    def deposit():
        acc_num = int(acc_num_entry.get())
        deposit_amt = int(deposit_entry.get())
        final_deposit = 0

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Chandu@2003",
            database="heritage"
        )
        cursor = mydb.cursor()
        query = 'SELECT Name, Accountno, Accounttype, deposit FROM account'
        cursor.execute(query)
        result = cursor.fetchall()

        for i in result:
            if i[1] == acc_num:
                balance = i[3]
                final_deposit = deposit_amt + balance
                ins = """ UPDATE account SET deposit=%s WHERE Accountno=%s;"""
                data = (final_deposit, acc_num)
                cursor.execute(ins, data)
                mydb.commit()
                result_label.config(text=f"The balance in your account is {final_deposit}")
                break
        else:
            result_label.config(text='''This account does not exist:
                   Do you want to create a new Account?
                   1. Yes 
                   2. No''')

    win2 = Tk()
    win2.title("Deposit Amount")

    label_acc_num = Label(win2, text="Account Number:")
    label_acc_num.pack()
    acc_num_entry = Entry(win2)
    acc_num_entry.pack()

    label_deposit = Label(win2, text="Amount to Deposit:")
    label_deposit.pack()
    deposit_entry = Entry(win2)
    deposit_entry.pack()

    deposit_button = Button(win2, text="Deposit", command=deposit)
    deposit_button.pack()

    result_label = Label(win2, text="")
    result_label.pack()

    win2.mainloop()

def withdraw():
    def withdraw_func():
        acc_num = int(acc_num_entry.get())
        withdraw_amt = int(withdraw_entry.get())

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Chandu@2003",
            database="heritage"
        )
        cursor = mydb.cursor()
        query = 'SELECT Name, Accountno, Accounttype, deposit FROM account'
        cursor.execute(query)
        result = cursor.fetchall()

        for i in result:
            if i[1] == acc_num:
                initial = i[3]
                if initial >= withdraw_amt:
                    balance = initial - withdraw_amt
                    ins = """ UPDATE account SET deposit=%s WHERE Accountno=%s;"""
                    data = (balance, acc_num)
                    cursor.execute(ins, data)
                    mydb.commit()
                    result_label.config(text=f"You have withdrawn the amount of {withdraw_amt}. The balance in your account is {balance}")
                    break
                else:
                    result_label.config(text="Insufficient amount in your account")
                    break
        else:
            result_label.config(text='''This account does not exist:
                   Do you want to create a new Account?
                   1. Yes 
                   2. No''')

    win3 = Tk()
    win3.title("Withdraw Amount")

    label_acc_num = Label(win3, text="Account Number:")
    label_acc_num.pack()
    acc_num_entry = Entry(win3)
    acc_num_entry.pack()

    label_withdraw = Label(win3, text="Amount to Withdraw:")
    label_withdraw.pack()
    withdraw_entry = Entry(win3)
    withdraw_entry.pack()

    withdraw_button = Button(win3, text="Withdraw", command=withdraw_func)
    withdraw_button.pack()

    result_label = Label(win3, text="")
    result_label.pack()

    win3.mainloop()

def mainw():
 win4 = Tk()

 img = Image.open("1.jpg")
 img = img.resize((200, 200))  
 img = ImageTk.PhotoImage(img)

 t1 = Label(win4, image=img)
 t1.image = img  
 t1.pack()

 t2 = Label(win4, text='Welcome to Heritage Bank', font=('Algerian', 30), bg='white', fg='black')
 t2.pack()

 t3 = Label(win4, text='Please click on any one of the options', font=('SegoeUIBlack', 16))
 t3.pack(pady=40)

 t4 = Button(win4, text='Create Account', bg='lightblue', fg='black',command=create_account)
 t4.pack()

 t5 =Button(win4, text='Check Balance', bg='lightblue', fg='black',command=check_balance)
 t5.pack(pady=25)

 t6 = Button(win4, text='Deposit', bg='lightblue', fg='black',command=depositamount)
 t6.pack(pady=13)

 t7 = Button(win4, text='Withdraw', bg='lightblue', fg='black',command=withdraw)
 t7.pack(pady=13)

 win4.mainloop()
 
 

mainw()
