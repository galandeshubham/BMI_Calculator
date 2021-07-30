from tkinter import *
from tkinter.messagebox import *
import datetime as d
import time
from tkinter.scrolledtext import *
import pymysql as p
import re

root = Tk()
root.title("welcome")
root.geometry("750x500+300+100")
f = ("Calibri", 20, "normal")

def getConnection():
        return p.Connect(user="root",host="localhost",password="abc123",database="db_shubham")

def f1():
        add_window.deiconify()
        root.withdraw()

def f2():
        cal_window.deiconify()
        add_window.withdraw()

def f3():
        con_window.deiconify()
        cal_window.withdraw()

def f4():
        add_window.deiconify()
        cal_window.withdraw()

def f5():
        cal_window.deiconify()
        con_window.withdraw()

def f6():
        view_window_bmi_data.delete(1.0, END)
        view_window.deiconify()
        add_window.withdraw()
        info = ""
        db = None
        try:
                db = getConnection()
                sql = "select * from bmi"
                cr = db.cursor()
                cr.execute(sql)
                data = cr.fetchall()
                for d in data:
                        info = info + " name = " + str(d[1]) + "\nage = " + str(d[2]) + "\nphone " + str(d[3]) + "\ngender = " + str(d[4]) + "\nbmi = " + str(d[5]) + "\n*****************\n"
                view_window_bmi_data.insert(INSERT, info)
        except Exception as e:
                showerror("Issue",e)
        finally:
                if db is not None:
                        db.close()

def f7():
        add_window.deiconify()
        view_window.withdraw()
        

def exp():
        try:
                db = p.Connect(user="root",host="localhost",password="abc123",database="db_shubham")
                x = time.strftime("%Y_%m_%d_%H_%M_%S")
                file = str(x)
                sql = """select 'pid','name','age','phone','gender','bmi','date' 
                        union all
                        select * into outfile 'D:\\person_{}.csv'
                        fields terminated by ','
                        from bmi""".format(file)
                cr = db.cursor()
                cr.execute(sql)
                db.commit()
                showinfo("success","exported successfully")
        except Exception as e:
                showerror("issue",e)
        finally:
                cr.close()
                db.close()
def cont():
        try:
                db = getConnection()
                sql = 'select count(*) from bmi'
                cr = db.cursor()
                cr.execute(sql)
                co = cr.fetchone()
                x = "count = " + str(co[0])
        except Exception as e:
                db.rollback()
                print("issue",e)
        else:
                add_window_lbl_count.config(text=x)
                add_window_lbl_count.after(200,cont)
        finally:
                db.close()
                
                
def cal():
        try:
                db = getConnection()
                x = d.date.today()
                name = cal_window_ent_name.get()
                age = cal_window_ent_age.get()
                phone = cal_window_ent_phone.get()
                h = float(cal_window_ent_height.get())
                w = cal_window_ent_weight.get()
                if h < 1 or h == None:
                        raise ValueError("plz enter valid weight")
                
                if ge.get() == 1:
                        gen = 'm'
                elif ge.get() == 2:
                        gen = 'f'
                else:
                        gen = 'o'
                print(gen)
                if re.search('^[A-Za-z]+$',name):
                        if re.search('^([1-9]|[1-9][0-9]|100)$',age):
                                if re.search('^[0-9]+$',phone):
                                        if re.search('(100)|[1-9]\d?',w):
                                                h = h / 100
                                                w = float(w)
                                                bm = w / (h * h)
                                                t = (None,name,age,phone,gen,bm,x)
                                                sql = "insert into bmi(pid,name,age,phone,gender,bmi,date) values(IFNULL(%s, DEFAULT(pid)),%s,%s,%s,%s,%s,%s)"
                                                cr = db.cursor()
                                                cr.execute(sql,t)
                                                db.commit()
                                                info = "name =" + name + "\nage = " + str(age) + "\nphone = " + str(phone) + "\ngender = " + gen + "\nbmi = " + str(bm)
                                                if bm < 18.5:
                                                        info = info + "\nAap patle ho"
                                                elif bm > 18.5 and bm < 24.9:
                                                        info = info + "\nAap Normal ho"
                                                else:
                                                        info = info + "\nAap Mote ho"
                                                cal_window_ent_name.delete(0, END)
                                                cal_window_ent_age.delete(0, END)
                                                cal_window_ent_phone.delete(0, END)
                                                cal_window_ent_height.delete(0, END)
                                                cal_window_ent_weight.delete(0, END)
                                                cal_window_ent_name.focus()
                                                showinfo("BMI", info)
                                        else:
                                                showerror("Mistake","plz enter weight in digits")
                                                
                                else:
                                        showerror("Mistake","phone no should contain only numbers")
                        else:
                                showerror("Mistake","age must be between 0-100")
                else:
                        showerror("Mistake","name should only contain alphabetes")
                
        except ValueError:
                db.rollback()
                showerror("issue","plz enter height in digits")
        except Exception as e:
                db.rollback()
                showerror("issue",e)
        finally:
                db.close()
        

lbl_name = Label(root, text="BMI Calci By Shubham Galande", font=('Calibri', 40, 'bold'), foreground='red')
btn_close = Button(root, text="close", font=('Calibri', 13, 'normal'), width=5, command=f1)
lbl_name.pack(pady=20)
btn_close.pack(pady=20)

add_window = Toplevel(root, background='pink')
add_window.title("BMI calculator")
add_window.geometry("750x500+300+100")

def mywatch():
        x = time.strftime("%Y-%m-%d %H-%M-%S")
        y = d.datetime.today()
        h = int(y.strftime("%H"))
        if h < 12:
                x = x + "\nGood Morning"
        elif h < 17:
                x = x + "\nGood Afternoon"
        elif h < 21:
                x = x + "\nGood Evening"
        else:
                x = x + "\nGood Night"
        clock.config(text=x)
        clock.after(200,mywatch)
        

clock = Label(add_window, font=f)
add_window_btn_calculate = Button(add_window, text="Calculate BMI", font=f, width=25, command=f2)
add_window_btn_view = Button(add_window, text="View History", font=f, width=25, command=f6)
add_window_btn_export = Button(add_window, text="Export Data", font=f, width=25, command=exp)
add_window_lbl_count = Label(add_window, font=f)
clock.pack(pady=10)
add_window_btn_calculate.pack(pady=10)
add_window_btn_view.pack(pady=10)
add_window_btn_export.pack(pady=10)
add_window_lbl_count.pack(pady=10)
mywatch()
cont()

cal_window = Toplevel(root, background='pink')
cal_window.title("Calculate")
cal_window.geometry("750x500+300+100")

ge = IntVar()
ge.set(1)

cal_window_lbl_name = Label(cal_window, text="enter name", font=f)
cal_window_ent_name = Entry(cal_window, bd=5, font=f)
cal_window_lbl_age = Label(cal_window, text="enter age", font=f)
cal_window_ent_age = Entry(cal_window, bd=5, font=f)
cal_window_lbl_phone = Label(cal_window, text="enter phone", font=f)
cal_window_ent_phone = Entry(cal_window, bd=5, font=f)
cal_window_lbl_gender = Label(cal_window, text="Gender", font=f)
cal_window_lbl_height = Label(cal_window, text="enter height in cm", font=f)
cal_window_ent_height = Entry(cal_window, bd=5, font=f)
cal_window_lbl_weight = Label(cal_window, text="enter weight in kg", font=f)
cal_window_ent_weight = Entry(cal_window, bd=5, font=f)
cal_window_btn_convert = Button(cal_window, text="Convert", font=f, width=8, command=f3)
cal_window_btn_calculate = Button(cal_window, text="Calculate", font=f, width=8, command=cal)
cal_window_btn_back = Button(cal_window, text="Back", font=f, width=8, command=f4)
cal_window_rb_male = Radiobutton(cal_window, text="Male", font=f, variable=ge, value=1)
cal_window_rb_female = Radiobutton(cal_window, text="Female", font=f, variable=ge, value=2)
cal_window_rb_other = Radiobutton(cal_window, text="Other", font=f, variable=ge, value=3)

cal_window_lbl_name.place(x=10, y=10)
cal_window_ent_name.place(x=260, y=10)
cal_window_lbl_age.place(x=10, y=70)
cal_window_ent_age.place(x=260, y=70)
cal_window_lbl_phone.place(x=10, y=130)
cal_window_ent_phone.place(x=260, y=130)
cal_window_lbl_gender.place(x=10, y=190)
cal_window_lbl_height.place(x=10, y=250)
cal_window_ent_height.place(x=260, y=250)
cal_window_lbl_weight.place(x=10, y=310)
cal_window_ent_weight.place(x=260, y=310)
cal_window_btn_convert.place(x=580, y=250)
cal_window_btn_calculate.place(x=20, y=370)
cal_window_btn_back.place(x=150, y=370)
cal_window_rb_male.place(x=260, y=190)
cal_window_rb_female.place(x=365, y=190)
cal_window_rb_other.place(x=500, y=190)
cal_window.withdraw()

con_window = Toplevel(root, background='green')
con_window.title("Height Converter")
con_window.geometry("750x500+300+100")

def fe():
        try:
                feet = con_window_ent_feet.get()
                inch = con_window_ent_inches.get()
                print(type(feet))
                if re.search('^[0-6]$',str(feet)):
                        if re.search('^[0-9]{2}$',str(inch)):
                                if int(inch) < 12:
                                        f = int(feet)
                                        i = int(inch)
                                        res = (f * 0.3048 + i * 0.0254) * 100
                                        showinfo("Centi-Meters", res)
                                else:
                                        showerror("Mistake","inch must be between 0 to 11")
                        else:
                                showerror("Mistake","inch must be between 0 to 11")
                else:
                        showerror("Mistake","Height must be between 0-6 feet")
        except Exception as e:
                showerror("Mistake", e)
                
con_window_lbl_name = Label(con_window, text="Enter your height", font=f)
con_window_lbl_feet = Label(con_window, text="Feet", font=f)
con_window_ent_feet = Entry(con_window, bd=5, font=f)
con_window_lbl_inches = Label(con_window, text="Inches", font=f)
con_window_ent_inches = Entry(con_window, bd=5, font=f)
con_window_btn_convert = Button(con_window, text="Convert", font=f, width=8, command=fe)
con_window_btn_back = Button(con_window, text="Back", font=f, width=8, command=f5)

con_window_lbl_name.pack(pady=10)
con_window_lbl_feet.pack(pady=10)
con_window_ent_feet.pack()
con_window_lbl_inches.pack(pady=20)
con_window_ent_inches.pack()
con_window_btn_convert.pack(pady=10)
con_window_btn_back.pack(pady=10)
con_window.withdraw()

view_window = Toplevel(root, background='sky blue')
view_window.title("View")
view_window.geometry("750x500+300+100")

view_window_bmi_data = ScrolledText(view_window, width=30, height=10, font=f)
view_window_btn_back = Button(view_window, text="Back", font=f, command=f7)
view_window_bmi_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()

root.mainloop()
