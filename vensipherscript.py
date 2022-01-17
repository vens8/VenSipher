# Copyright (C) Ravens Enterprises - All Rights Reserved
# * Unauthorized copying of this file, via any medium is strictly prohibited
# * Proprietary and confidential
# * Written by Rahul Maddula <vensr.maddula@gmail.com>, June 2020

import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import random
from tkinter import messagebox
import mysql.connector
from datetime import date
import urllib
from urllib.error import URLError
from urllib.request import urlopen
import sys  # for sys.exit(0)

root = tk.Tk()
root.iconbitmap("images/VenSipherLogo.ico")
root.grid_columnconfigure(0, weight=200)
root.grid_rowconfigure(0, weight=200)

# Menu
menu1 = Menu(root)
root.config(menu=menu1)


def homemenu():
    frame2.place_forget()
    frame3.place_forget()
    frame1.grid(pady=0, padx=0)
    frame1.place(width=root.winfo_screenwidth(), height=root.winfo_screenheight())


def aboutmenu():
    frame1.place_forget()
    frame3.place_forget()
    frame2.grid(pady=0, padx=0)
    frame2.place(relwidth=1, relheight=1, relx=0, rely=0)


def helpmenu():
    frame1.place_forget()
    frame2.place_forget()
    frame3.grid(pady=0, padx=0)
    frame3.place(relwidth=1, relheight=1, relx=0, rely=0)


# Menu items
home = Menu(menu1)
about = Menu(menu1)
helptab = Menu(menu1)
menu1.add_cascade(label="Home", menu=home)
home.add_command(label="Go to VenSipher", command=homemenu)
menu1.add_cascade(label="About", menu=about)
about.add_command(label="About VenSipher", command=aboutmenu)
menu1.add_cascade(label="Help", menu=helptab)
helptab.add_command(label="Contact", command=helpmenu)

# Canvas
canvas = tk.Canvas(root, height=root.winfo_screenwidth(), width=root.winfo_screenheight(), bg="#043000")
canvas.grid(sticky=N+E+W+S, column=0, pady=0, padx=0)
canvas.grid_rowconfigure(0, weight=1)
canvas.grid_columnconfigure(0, weight=1)

# Mainframe
frame1 = tk.Frame(root, bg="#043000")  # Frame placed inside the canvas. Same colour as canvas so invisible.
frame1.grid(sticky=N+E+W+S, row=0, column=0, pady=0, padx=0)
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_columnconfigure(0, weight=1)
frame1.place(width=canvas.winfo_screenwidth(), height=canvas.winfo_screenwidth())

# About frame
frame2 = Frame(root, bg="black")
frame3 = Frame(root, bg="black")

root.title('VenSipher')  # Text to display on the title bar of the application
root.state('zoomed')  # Opens the maximised version of the window by default

characters = '''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[]{}|;':",./<>? '''
charlist = list(characters)
characters2 = '''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[]{}|;':",./<>? '''
characters3 = '''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'''
charlist3 = list(characters3)
charlist2 = list(characters2)

swap = False  # Switch of scroll texts is false by default


def internet_on(host='https://www.google.com/'):
    try:
        urllib.request.urlopen(host, timeout=1)
        return True
    except urllib.error.URLError as err:
        return False


def insert(rand, code):
    dates = str(date.today().strftime('%Y-%m-%d'))
    if internet_on():
        print("Connection Successful")
        mydb = mysql.connector.connect(host="remotemysql.com", user="username", passwd="password",
                                       database="database")
        sqlform = "INSERT INTO `Secure` (Randcombination, Hash, Date) VALUES(%s, %s, %s)"
        list1 = [(rand, code, dates)]
        mycursor = mydb.cursor()
        mycursor.executemany(sqlform, list1)
        mydb.commit()

    else:
        messagebox.showinfo("Network Error", "Could not establish connection to the database")
        sys.exit(0)


def search(incode):
    if internet_on():
        count = None
        mydb = mysql.connector.connect(host="remotemysql.com", user="usename", passwd="password",
                                       database="database")
        mycursor = mydb.cursor()
        print("Connection Successful")
        sqlform1 = "SELECT COUNT(*) FROM `Secure` WHERE Hash=" + "'" + incode + "'"
        mycursor.execute(sqlform1)
        record1 = mycursor.fetchone()
        for row1 in record1:
            count = row1

        if count == 0:
            return "0"

        else:
            sqlform2 = "SELECT Randcombination FROM `Secure` WHERE Hash=" + "'" + incode + "'"
            mycursor.execute(sqlform2)
            record = mycursor.fetchone()
            for row2 in record:
                return row2

    else:
        messagebox.showinfo("Network Error", "Could not establish connection to the database")
        sys.exit(0)


def delete(incode, checkvar):  # receives the one-time pass and the checkbutton value
    mydb = mysql.connector.connect(host="remotemysql.com", user="username", passwd="password",
                                   database="database")
    mycursor = mydb.cursor()

    if checkvar == 0:
        if mydb:
            print("Connection Successful")
            sqlform = "Delete FROM `Secure` WHERE DATEDIFF(DATE_FORMAT(SYSDATE(), '%Y-%m-%d'), Date) > 0"  # DATEDIFF(date1, date2) in days
            mycursor.execute(sqlform)
            mydb.commit()
            print("Record deleted")

        else:
            print("Connection unsuccessful")

    else:
        if mydb:
            print("Connection Successful")
            sqlform = "Delete FROM `Secure` WHERE Hash=" + "'" + incode + "'"  # Deletes the record immediately after use
            mycursor.execute(sqlform)
            mydb.commit()
            print("Record deleted")

        else:
            print("Connection unsuccessful")


def loading():
    label6.place_forget()


# idea for assigning random values to each letter
# Do random.sample and create a list of random characters. then assign each letter to respective list part.
# Example ['!', '@', '#] and so on, list of characters becomes a = !, b = @, c = #
# Convert Function
def convert():
    label6.place(x=35, y=610)
    if swap == False:
        input1 = scr1.get('1.0',
                          'end-1c')  # 1.0 means first character, end-1c means last character and get() takes between
        inputlist1 = list(input1)
        randcharlist = random.sample(charlist, 94)
        rand = listToString(randcharlist)
        codelist = random.sample(charlist3, 12)
        code = listToString(codelist)
        if scr1.compare("end-1c", "==", "1.0"):
            messagebox.showinfo("Error", "Input text is empty")
            loading()

        else:
            output = None
            for element in range(0, len(input1)):
                if inputlist1[element] not in randcharlist:
                    inputlist1[element] = inputlist1[element]
                    output = "".join(inputlist1)

                else:
                    index = charlist2.index(inputlist1[element])
                    inputlist1[element] = randcharlist[index]
                    output = "".join(inputlist1)  # strings in python are immutable hence this.
            insert(rand, code)
            scr2.config(state='normal')
            scr2.delete(1.0, END)
            scr2.insert(tk.INSERT, output)
            scr2.config(state='disabled')
            tb1.delete(1.0, END)
            tb1.insert(tk.INSERT, code)
            loading()

    else:
        if scr1.compare("end-1c", "==", "1.0"):
            messagebox.showinfo("Error", "Secret text input is empty")
            loading()

        else:
            input2 = scr1.get('1.0', 'end-1c')
            inputlist2 = list(input2)
            if tb1.compare("end-1c", "==", "1.0"):
                messagebox.showinfo("Error", "Please enter the code")
                loading()

            else:
                incode = tb1.get('1.0', 'end-1c')
                search(incode)
                randchar = search(incode)
                if randchar == "0":
                    messagebox.showinfo("Error", "Invalid code, please try again.")
                    loading()

                else:
                    output = None
                    randcharlist = list(randchar)
                    for element in range(0, len(input2)):
                        if inputlist2[element] not in randcharlist:
                            inputlist2[element] = inputlist2[element]
                            output = "".join(inputlist2)

                        else:
                            index = randcharlist.index(inputlist2[element])
                            inputlist2[element] = charlist2[index]
                            output = "".join(inputlist2)  # strings in python are immutable hence this.
                    loading()
                    scr2.config(state='normal')
                    scr2.delete(1.0, END)
                    scr2.insert(tk.INSERT, output)
                    scr2.config(state='disabled')
                    delete(incode, var1.get())
    loading()


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


def clear():
    scr2.config(state='normal')
    scr1.delete(1.0, END)
    scr2.delete(1.0, END)
    scr2.config(state='disabled')
    tb1.delete(1.0, END)


def copy():
    root.clipboard_clear()
    scr2.config(state='normal')
    root.clipboard_append(scr2.get('1.0', 'end-1c'))
    scr2.config(state='disabled')
    root.update()  # now it stays on the clipboard after the window is closed


def paste():
    result = root.selection_get(selection="CLIPBOARD")
    scr1.delete(1.0, END)
    scr1.insert(tk.INSERT, result)


def copypaste():
    if tb1.compare("end-1c", "==", "1.0"):
        result = root.selection_get(selection="CLIPBOARD")
        tb1.insert(tk.INSERT, result)

    else:
        root.clipboard_clear()
        root.clipboard_append(tb1.get('1.0', 'end-1c'))
        root.update()  # now it stays on the clipboard after the window is closed


def switch():
    global swap  # accesses swap which has been declared at the beginning (out of local scope)
    if swap:
        label3.place_forget()
        label1.grid(sticky=N+E+W+S, column=0, pady=0.5, padx=0.5)
        label1.grid_columnconfigure(0, weight=100)
        label1.grid_rowconfigure(0, weight=100)
        label1.place(x=35, y=85)
        label4.place_forget()
        label2.grid(sticky=N+E+W+S, column=0, pady=0.5, padx=0.5)
        label2.grid_columnconfigure(0, weight=100)
        label2.grid_rowconfigure(0, weight=100)
        label2.place(x=1150, y=85)
        swap = False

    else:
        label1.place_forget()
        label3.grid(sticky=N+E+W+S, column=0, pady=0.5, padx=0.5)
        label3.grid_columnconfigure(0, weight=100)
        label3.grid_rowconfigure(0, weight=100)
        label3.place(x=35, y=85)
        label2.place_forget()
        label4.grid(sticky=N+E+W+S, column=0, pady=0.5, padx=0.5)
        label4.grid_columnconfigure(0, weight=100)
        label4.grid_rowconfigure(0, weight=100)
        label4.place(x=1150, y=85)
        swap = True


# Scrolled Text1
scr1 = scrolledtext.ScrolledText(frame1, wrap=tk.WORD, width=62, height=20, font=("Times New Roman", 15), bg="#000000",
                                 fg="yellow")
scr1.configure(insertbackground="yellow")
scr1.grid(sticky=N+E+W+S, column=0, pady=5, padx=5)  # area widget
scr1.grid_columnconfigure(0, weight=100)
scr1.grid_rowconfigure(0, weight=100)
scr1.place(x=35, y=140)
scr1.focus()  # Placing cursor in the text area

# Scrolled Text2
scr2 = scrolledtext.ScrolledText(frame1, wrap=tk.WORD, width=62, height=20, font=("Times New Roman", 15), bg="#000000",
                                 fg="yellow")
scr2.grid(sticky=N+E+W+S, column=0, pady=5, padx=5)  # area widget
scr2.grid_columnconfigure(0, weight=100)
scr2.grid_rowconfigure(0, weight=100)
scr2.place(x=685, y=140)
scr2.config(state='disabled')

# Label3
img6 = PhotoImage(file="images/inputsecrettext.png")  # add "/" not "\"
label3 = Label(frame1, image=img6, borderwidth=0, bg="#043000")
label3.grid_columnconfigure(0, weight=100)
label3.grid_rowconfigure(0, weight=100)

# Label4
img7 = PhotoImage(file="images/outputtext.png")  # add "/" not "\"
label4 = Label(frame1, image=img7, borderwidth=0, bg="#043000")
label4.grid_columnconfigure(0, weight=100)
label4.grid_rowconfigure(0, weight=100)

# Label1
img3 = PhotoImage(file="images/inputtext.png")  # add "/" not "\"
label1 = Label(frame1, image=img3, borderwidth=0, bg="#043000")
label1.grid(sticky=N+E+W+S, column=0, pady=0.5, padx=0.5)
label1.grid_columnconfigure(0, weight=100)
label1.grid_rowconfigure(0, weight=100)
label1.place(x=35, y=85)

# Label2
img4 = PhotoImage(file="images/secrettext.png")  # add "/" not "\"
label2 = Label(frame1, image=img4, borderwidth=0, bg="#043000")
label2.grid(sticky=N+E+W+S, column=0, pady=0.5, padx=0.5)
label2.grid_columnconfigure(0, weight=100)
label2.grid_rowconfigure(0, weight=100)
label2.place(x=1150, y=85)

# Label5
abouttext = '''Copyright (C) Ravens Enterprises - All Rights Reserved
* Unauthorized copying of this file, via any medium is strictly prohibited
* Proprietary and confidential
* Written by Rahul Maddula <vensr.maddula@gmail.com>, June 2020

VenSipher is a free-of-cost proprietary software which is designed to convert any input text into an unrecognisable
secret code which can only be deciphered by the person having the auto-generated code. VenSipher works from any part
of the world as long as you are connected to the internet. 

VenSipher was designed using Python programming language and was released in June 2020.

About the author
VenSipher was designed and programmed by Rahul Maddula (born 3 June 2002)
You can interact or contact me for any information through my email and social media handles. Visit Help>>Contact.
'''

label7 = Label(frame2, text=abouttext, font=('Times New Roman', 18), borderwidth=0, bg="black", fg="yellow")
label7.grid(sticky=N+E+W+S)
label7.grid_rowconfigure(0, weight=100)
label7.grid_columnconfigure(0, weight=100)
label7.place(relheight=1, relwidth=1)

# Label6
helptext = '''For any kind of bugs/issues/help/details please contact me (the owner) through the following:
Personal Email: vensr.maddula@gmail.com
Business Email: ravensenterprises8@gmail.com
Personal Instagram handle: @vens8
Personal Twitter handle: @vens_8
'''

label8 = Label(frame3, text=helptext, font=('Times New Roman', 18), borderwidth=0, bg="black", fg="yellow")
label8.grid(sticky=N+E+W+S)
label8.grid_rowconfigure(0, weight=100)
label8.grid_columnconfigure(0, weight=100)
label8.place(relheight=1, relwidth=1)

# Checkbox1
var1 = tk.IntVar()
cb1 = Checkbutton(frame1, text='Delete record after use', font=('Times New Roman', 16),
                  variable=var1, bg="black", fg="yellow", activebackground="black",
                  activeforeground="yellow", selectcolor="black", onvalue=1, offvalue=0)
cb1.grid(sticky=N+E+W+S)
cb1.grid_rowconfigure(0, weight=100)
cb1.grid_columnconfigure(0, weight=100)
cb1.place(x=925, y=600)
cb1.select()

# Button1
img = PhotoImage(file="images/convertbutton.png")  # add "/" not "\"
button1 = Button(frame1, image=img, command=convert, borderwidth=0, bg="#043000", relief=FLAT)
button1.grid(sticky=N+E+W+S)
button1.grid_rowconfigure(0, weight=100)
button1.grid_columnconfigure(0, weight=100)
button1.place(x=575, y=590)

# Button2
img2 = PhotoImage(file="images/clearalltext.png")  # add "/" not "\"
button2 = Button(frame1, image=img2, command=clear, borderwidth=0, bg="#043000", relief=FLAT)
button2.grid(sticky=N+E+W+S)
button2.grid_columnconfigure(0, weight=100)
button2.grid_rowconfigure(0, weight=100)
button2.place(x=1175, y=590)

# Button3
img5 = PhotoImage(file="images/switchtext.png")  # add "/" not "\"
button3 = Button(frame1, image=img5, command=switch, borderwidth=0, bg="#043000", relief=FLAT)
button3.grid(sticky=N+E+W+S)
button3.grid_rowconfigure(0, weight=100)
button3.grid_columnconfigure(0, weight=100)
button3.place(x=610, y=100)

# Button4
img9 = PhotoImage(file="images/clipboardtext.png")  # add "/" not "\"
button4 = Button(frame1, image=img9, command=copy, borderwidth=0, bg="#043000", relief=FLAT)
button4.grid(sticky=N+E+W+S)
button4.grid_columnconfigure(0, weight=100)
button4.grid_rowconfigure(0, weight=100)
button4.place(x=980, y=95)

# Button5
img10 = PhotoImage(file="images/pastetext.png")  # add "/" not "\"
button5 = Button(frame1, image=img10, command=paste, borderwidth=0, bg="#043000", relief=FLAT)
button5.grid(sticky=N+E+W+S)
button5.grid_rowconfigure(0, weight=100)
button5.grid_columnconfigure(0, weight=100)
button5.place(x=215, y=95)

# Button6
img8 = PhotoImage(file="images/codetext.png")  # add "/" not "\"
button6 = Button(frame1, image=img8, command=copypaste, borderwidth=0, bg="#043000", relief=FLAT)
button6.grid(sticky=N+E+W+S)
button6.grid_rowconfigure(0, weight=100)
button6.grid_rowconfigure(0, weight=100)
button6.place(x=1000, y=10)

# Textbox1
tb1 = Text(frame1, width=25, height=1, font=("Times New Roman", 12), fg="yellow", bg="#000000")
tb1.configure(insertbackground="yellow")
tb1.grid(sticky=N+E+W+S, column=0, pady=0.5, padx=0.5)
tb1.grid_columnconfigure(0, weight=100)
tb1.grid_rowconfigure(0, weight=100)
tb1.place(x=1125, y=15)

# Image1
img11 = PhotoImage(file="images/VenSipher2.png")
label5 = Label(frame1, image=img11, borderwidth=0, bg="#043000")
label5.grid(sticky=N+E+W+S, pady=0, padx=0)
label5.grid_columnconfigure(0, weight=100)
label5.grid_rowconfigure(0, weight=100)
label5.place(x=480, y=0)

# Image2
img12 = PhotoImage(file="images/loadingtext.png")
label6 = Label(frame1, image=img12, borderwidth=0, bg="#043000")

root.mainloop()
