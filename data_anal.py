
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import customtkinter
from _tkinter import TclError

import Data_Analysis
from Data_Analysis import *

widgets = []

data_win = customtkinter.CTk()
data_win.title("Data Analysis")
data_win.geometry("1200x700")
data_win._set_appearance_mode("light")
data_win.resizable(False, False)
style = ttk.Style()
style.theme_use("classic")
style.map("Treeview")
def backtomain_dashboard():
    data_win.destroy()
def delete_wid():
    for i in widgets:
        i.destroy()
    widgets.clear()


def remove_dashboard():
    global widgets
    widgets.extend([frame3,frame4,frame5,frame6,frame7,frame8,frame9,frame10,welcum_lbl,admin_image_lbl,divider_lbl,hr_lbl,mm_lbl,min_lbl,date_lbl,bu_lbl,bu_logo_lbl,studImage_lbl,microscopeImage_lbl,calibLogo_lbl,studAnalysis_lbl,inventoryAnalysis_lbl,calibAnalysis,div1,div2,div3])
    delete_wid()
    print('remove dashboard')


def student_treeview():
    global tree_student
    global labels
    global sizes
    columns = ("Program", "Number of Student")
    print("Creating Treeview...")
    tree_student = ttk.Treeview(frame2, columns=columns, show='headings')

    # Set headings
    tree_student.heading('Program', text='Program')
    tree_student.heading('Number of Student', text='Number of Students')

    # Fetch courses from the database
    courses = fetch_courses()
    print("Courses:", courses)  # Print courses to debug

    # Tally the occurrences of each course and calculate total count
    course_counts = {}
    total_count = 0
    for course_data in courses:
        course = course_data[0]  # Extract the course name
        count = course_counts.get(course, 0) + 1
        course_counts[course] = count
        total_count += 1  # Increment total count for each course

    # Populate treeview with the tally of occurrences
    for course, count in course_counts.items():
        print("Course:", course, "Count:", count)  # Print each course and count to debug
        tree_student.insert("", "end", values=(course, count))

    # Add total row at the bottom
    total_row = ("Total", total_count)
    tree_student.insert("", "end", values=total_row)

    # Apply tags to headings and total row
    tree_student.tag_configure("headings", font=("Helvetica", 10, "bold"), background="#c0c0c0")
    tree_student.tag_configure("total", font=("Helvetica", 10, "bold"), background="#ffff00")



    # Place the treeview widget with specified dimensions
    tree_student.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

def inventory_treeview():
    global tree_inventory,total_label
    # Define columns for the treeview
    columns = ["Items", "Available Quantity"]

    # Create the treeview
    tree_inventory = ttk.Treeview(frame2, columns=columns, show='headings')

    # Set headings for the columns
    for col in columns:
        tree_inventory.heading(col, text=col)

    # Fetch data from the database
    data = fetch_inventory()

    # Insert data into the treeview
    for row in data:
        tree_inventory.insert("", "end", values=row)

    # Place the treeview within the frame
    tree_inventory.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)

    # Calculate total number of items
    total_items = sum(row[1] for row in data)

    # Create a label to display the total items
    total_label = ttk.Label(frame2, text=f"Total Items: {total_items}",background='white')
    total_label.place(relx=0.06, rely=0.9)


def treeview_calib():
    global tree_calib
    columns = ("Equipment", "Calibration Status")
    tree_calib= ttk.Treeview(frame2, columns=columns, show='headings')
    for col in columns:
        tree_calib.heading(col, text=col)

    calib = fetch_calibration()
    for row in calib:
        tree_calib.insert("", 'end', values=row)

    tree_calib.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)

def fetch_courses():
    conn = sqlite3.connect('Laboratory_Database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT course FROM Students')
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses

def fetch_inventory():
    conn = sqlite3.connect('Laboratory_Database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ItemName, Quantity FROM Inventory')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def fetch_calibration():
    conn = sqlite3.connect('Laboratory_Database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Equipment, CalibrationDone FROM Calibration')
    calib_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return calib_data

def create_pie_chart_course():
    fig, ax = plt.subplots(figsize=(6,4))
    courses = fetch_courses()
    course_counts = {}
    for course in courses:
        course_counts[course[0]] = course_counts.get(course[0], 0) + 1 #add if same course

    labels = course_counts.keys()
    sizes = course_counts.values()

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribution of Courses')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show() # Display the plot
    plt.close(fig) # Close the figure to avoid displaying empty plot
    return fig

def create_pie_calibration():
    fig, ax = plt.subplots(figsize=(6, 5))
    calib = fetch_calibration()
    calibrated_count = {}
    for equip in calib:
        calibrated_count[equip[1]] = calibrated_count.get(equip[1], 0) + 1

    labels = calibrated_count.keys()
    values = calibrated_count.values()

    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Calibration of Equipments')
    ax.axis('equal')
    plt.show()
    plt.close(fig)
    return fig

graph_inventory = False
graph_course = False
graph_calibration=False
tree_student = None
tree_calib = None
tree_inventory = None
total_label=None

def show_course_plot():
    global graph_course, graph_inventory,StudentAnalysis_bttn,Inventory_bttn,calibAnalysis_bttn
    reset_bttn(calibAnalysis_bttn)
    reset_bttn(Inventory_bttn)
    button_clicked(StudentAnalysis_bttn)
    remove_dashboard()
    delete_wid()# Remove the dashboard phase completely
    if graph_course:
        graph_course = False
    else:
        frame2.configure(fg_color="#005aff")
        frame2.configure(bg_color='#005aff')
        student_treeview()
        if graph_inventory:
            show_bar_inventory()
        fig = create_pie_chart_course()
        graph_course = True
        graph_inventory = False

def show_bar_inventory():
    global graph_inventory, graph_course,Inventory_bttn,StudentAnalysis_bttn,calibAnalysis_bttn
    reset_bttn(StudentAnalysis_bttn)
    reset_bttn(calibAnalysis_bttn)
    button_clicked(Inventory_bttn)
    remove_dashboard()
    delete_wid()# Remove the dashboard phase completely
    if graph_inventory:
        graph_inventory=False
    else:
        frame2.configure(fg_color="#ffa500")
        frame2.configure(bg_color='#ffa500')
        inventory_treeview()
        data_analysis.record()
        if graph_course:
            show_course_plot()
        graph_inventory=True
        graph_course=False

def show_bar_calibration():
    global graph_calibration, graph_course, graph_inventory, total_label, calibAnalysis_bttn, Inventory_bttn, StudentAnalysis_bttn

    # Reset other buttons to their default color
    reset_bttn(StudentAnalysis_bttn)
    reset_bttn(Inventory_bttn)

    # Highlight the calibration analysis button
    button_clicked(calibAnalysis_bttn)

    # Remove all existing widgets
    remove_dashboard()

    if graph_calibration:
        graph_calibration = False  # Hide the calibration graph if it is currently displayed
    else:
        # Configure the main frame color
        frame2.configure(fg_color='gray')
        frame2.configure(bg_color='gray')

        # Display the calibration treeview
        treeview_calib()  # Ensure this function is correctly defined and used

        # Check if other graphs are displayed and redraw them if needed
        if graph_course:
            show_course_plot()
        if graph_inventory:
            show_bar_inventory()

        # Clear the label displaying total items
        if total_label:
            total_label.destroy()  # Remove the total label if it exists

        # Create and display the calibration pie chart
        fig = create_pie_calibration()

        # Update the graph flags
        graph_calibration = True
        graph_inventory = False
        graph_course = False
def toggle_frame():
    global frame1
    global frame2
    if frame1 is not None:
        frame1.destroy()
        frame1 = None
        frame2.clear()
        frame2.configure(fg_color='white')
        widgets.extend([])
        delete_wid()
        dashboard()
    else:
        option()
def delete_treeview():
    global tree_student, tree_calib, tree_inventory
    if tree_calib:
        tree_calib.destroy()
    if tree_inventory:
        tree_inventory.destroy()
    if tree_student:
        tree_student.destroy()
    delete_wid()
    print("treeview deleted")

def button_clicked(button):
    button.configure(fg_color='#ffa500')

def reset_bttn(button):
    button.configure(fg_color='gray')

def option():
    global frame1
    global StudentAnalysis_bttn,Inventory_bttn,calibAnalysis_bttn
    frame1 = customtkinter.CTkFrame(master=data_win, width=220, height=700, fg_color="gray", bg_color="gray")
    frame1.place(relx=0, rely=0.0725)
    StudentAnalysis_bttn = customtkinter.CTkButton(master=frame1, width=230, height=40, text="Student Analysis",
                                                    font=("Helvetica", 17, 'bold'), fg_color="gray",text_color="white",
                                                    command=show_course_plot)
    StudentAnalysis_bttn.place(relx=-0.02, rely=0.01)
    Inventory_bttn = customtkinter.CTkButton(master=frame1, width=250, height=40, text="Inventory",
                                        font=("Helvetica", 17, 'bold'), fg_color="gray", command=show_bar_inventory,text_color="white")
    Inventory_bttn.place(relx=-0.1, rely=0.08)
    calibAnalysis_bttn = customtkinter.CTkButton(master=frame1, width=250, height=40, text="Calibration",
                                        font=("Helvetica", 17, 'bold'), fg_color="gray",text_color="white",command=show_bar_calibration)
    calibAnalysis_bttn.place(relx=-0.1, rely=0.16)







frame1 = None
frame = customtkinter.CTkFrame(master=data_win, width=1200, height=50, fg_color="#005aff", bg_color="#005aff")
frame.place(relx=0, rely=0)
dashboard_lbl = customtkinter.CTkLabel(master=frame, text="DATA ANALYSIS", font=("Helvetica", 19, "bold"),
                                           text_color="white")
dashboard_lbl.place(relx=0.005, rely=0.2)
dash_option_logo = customtkinter.CTkImage(dark_image=Image.open("menus.png"), size=(25,25))
home_logo=customtkinter.CTkImage(dark_image=Image.open("home_icon.png"),size=(30,30))
dash_opt = customtkinter.CTkButton(master=frame, text="", width=40, height=40, fg_color="#005aff",
                                       image=dash_option_logo, command=toggle_frame)
dash_opt.place(relx=0.14, rely=0.1)
home_bttn=customtkinter.CTkButton(master=frame,text="",width=30,height=15,fg_color="#005aff",image=home_logo,command=backtomain_dashboard)
home_bttn.place(relx=0.94,rely=0.15)

def dashboard():
    delete_treeview()
    frame3 = customtkinter.CTkFrame(master=frame2,width=600,height=200,fg_color="#005aff",corner_radius=30)#color blue frame
    frame3.place(relx=0.028,rely=0.04)
    frame4=customtkinter.CTkFrame(master=frame3,width=170,height=100,fg_color='#4d8cff',corner_radius=25)
    frame4.place(relx=0.66,rely=0.4)
    welcum_lbl=customtkinter.CTkLabel(master=frame3,text="Welcome Back Admin!",text_color="white",font=("Calibri",35,'bold'))
    welcum_lbl.place(relx=0.4,rely=0.15)
    admin_image = customtkinter.CTkImage(Image.open("admin.png"),size=(150,150))
    admin_image_lbl = customtkinter.CTkLabel(master=frame3,text="",image=admin_image)
    admin_image_lbl.place(relx=0.03,rely=0.15)
    divider_lbl = customtkinter.CTkLabel(master=frame4,text="━━━",text_color='white',font=("Helvetica",40,'bold'),)
    divider_lbl.place(relx=0.13,rely=0.35)
    hr_lbl = customtkinter.CTkLabel(master=frame4,text="",font=("Helvetica",35,'bold'))
    hr_lbl.place(relx=0.15,rely=0.12)
    mm_lbl=customtkinter.CTkLabel(master=frame4,text=":",font=("Helvetica",40,'bold'))
    mm_lbl.place(relx=0.45,rely=0.05)
    min_lbl = customtkinter.CTkLabel(master=frame4,text="",font=("Helvetica",35,'bold'))
    min_lbl.place(relx=0.6,rely=0.12)
    date_lbl=customtkinter.CTkLabel(master=frame4,text="",font=("Helvetica",20,'bold'))
    date_lbl.place(relx=0.2,rely=0.63)
    frame5=customtkinter.CTkFrame(master=frame2,width=850,height=330,fg_color="#ffc04d",corner_radius=30) #big rectangle at dashboard
    frame5.place(relx=0.028,rely=0.41)
    frame6=customtkinter.CTkFrame(master=frame2,width=220,height=210,fg_color="#ffc04d",corner_radius=30) #small square at dashboard
    frame6.place(relx=0.72,rely=0.03)
    frame7=customtkinter.CTkFrame(master=frame6,width=180,height=170,fg_color="#ffdd80",corner_radius=40)
    frame7.place(relx=.09,rely=.09)
    frame8=customtkinter.CTkFrame(master=frame5,width=400,height=140,fg_color="#ffdd80",corner_radius=30)
    frame8.place(relx=0.02,rely=0.05)
    frame9=customtkinter.CTkFrame(master=frame5,width=400,height=140,fg_color="#ffdd80",corner_radius=30)
    frame9.place(relx=0.02,rely=0.5)
    frame10=customtkinter.CTkFrame(master=frame5,width=400,height=140,fg_color="#ffdd80",corner_radius=30)
    frame10.place(relx=0.51,rely=0.05)
    frame11=customtkinter.CTkFrame(master=frame5,width=400,height=140,fg_color="#ffdd80",corner_radius=30)
    frame11.place(relx=0.51,rely=0.5)
    bu_logo=customtkinter.CTkImage(Image.open("logo.png"),size=(120,120))
    bu_logo_lbl=customtkinter.CTkLabel(master=frame7,text="",image=bu_logo)
    bu_logo_lbl.place(relx=0.16,rely=0.07)
    bu_lbl=customtkinter.CTkLabel(master=frame7,text="BICOL UNIVERSITY \n POLANGUI",text_color="white",font=("Helvetica",12,'bold'))
    bu_lbl.place(relx=0.2,rely=0.8)

    studImage=customtkinter.CTkImage(Image.open("stud.png"),size=(150,150))
    studImage_lbl=customtkinter.CTkLabel(master=frame8,text="",image=studImage)
    studImage_lbl.place(relx=0.07,rely=0.001)
    microscopeImage=customtkinter.CTkImage(Image.open("microscope.png"),size=(130,130))
    microscopeImage_lbl=customtkinter.CTkLabel(master=frame10,text="",image=microscopeImage)
    microscopeImage_lbl.place(relx=0.05,rely=0.003)
    calib_logo=customtkinter.CTkImage(Image.open('calibb.png'), size=(180, 100))
    calibLogo_lbl=customtkinter.CTkLabel(master=frame9,text="",image=calib_logo)
    calibLogo_lbl.place(relx=0.04,rely=0.15)
    maintenanceImage=customtkinter.CTkImage(Image.open('maint.png'),size=(100,90))
    maintenanceImage_lbl=customtkinter.CTkLabel(master=frame11,text="",image=maintenanceImage)
    maintenanceImage_lbl.place(relx=0.1,rely=0.2)

    studAnalysis_lbl=customtkinter.CTkLabel(master=frame8,text="Student\n Analysis",font=("Helvetica",30,'bold'),text_color="white")
    studAnalysis_lbl.place(relx=0.52,rely=0.2)
    div1=customtkinter.CTkLabel(master=frame8,text="|",font=("Helvetica",80,'bold'),text_color='white')
    div1.place(relx=0.45,rely=0.1)

    calibAnalysis=customtkinter.CTkLabel(master=frame9,text="Calibration\nAnalysis",font=("Helvetica",30,'bold'),text_color="white")
    calibAnalysis.place(relx=0.52,rely=0.22)
    div3=customtkinter.CTkLabel(master=frame9,text="|",font=("Helvetica",80,'bold'),text_color='white')
    div3.place(relx=0.45,rely=0.1)
    inventoryAnalysis_lbl=customtkinter.CTkLabel(master=frame10,text="Inventory\nAnalysis",font=("Helvetica",30,'bold'),text_color='white')
    inventoryAnalysis_lbl.place(relx=0.5,rely=0.2)
    div2=customtkinter.CTkLabel(master=frame10,text='|',text_color='white',font=("Helvetica",80,'bold'))
    div2.place(relx=0.4,rely=0.08)
    maintenanceAnalysis=customtkinter.CTkLabel(master=frame11,text="Maintenance\nAnalysis",font=("Helvetica",30,'bold'),text_color='white')
    maintenanceAnalysis.place(relx=0.5,rely=0.2)
    div4=customtkinter.CTkLabel(master=frame11,text='|',font=('Helvetica',80,'bold'),text_color='white')
    div4.place(relx=0.4,rely=0.1)
    widgets.extend([frame3, frame4, frame5, frame6, frame7, frame8, frame9, frame10, frame11,
                    welcum_lbl, admin_image_lbl, divider_lbl, hr_lbl, mm_lbl, min_lbl, date_lbl,
                    bu_lbl, bu_logo_lbl, studImage_lbl, microscopeImage_lbl, calibLogo_lbl, maintenanceImage_lbl,
                    studAnalysis_lbl, inventoryAnalysis_lbl, calibAnalysis, maintenanceAnalysis])

    def update_time():
        now = datetime.now()
        month=now.strftime("%m")
        day=now.strftime("%d")
        yr=now.strftime("%y")
        date=(f'{day} | {month} | {yr}')
        hr = now.strftime("%H")
        min=now.strftime("%M")
        hr_lbl.configure(text=hr)
        min_lbl.configure(text=min)
        date_lbl.configure(text=date)
        data_win.after(1000, update_time)  # Update every 60 seconds

    update_time()

#widget in dashboard
frame2 = customtkinter.CTkFrame(master=data_win,width=900,height=600,fg_color='white',corner_radius=40,bg_color='White')#frame that contains other frames
frame2.place(relx=0.22,rely=0.1)
frame3 = customtkinter.CTkFrame(master=frame2,width=600,height=200,fg_color="#005aff",corner_radius=30)#color blue frame
frame3.place(relx=0.028,rely=0.04)
frame4=customtkinter.CTkFrame(master=frame3,width=170,height=100,fg_color='#4d8cff',corner_radius=25)
frame4.place(relx=0.66,rely=0.4)
welcum_lbl=customtkinter.CTkLabel(master=frame3,text="Welcome Back Admin!",text_color="white",font=("Calibri",35,'bold'))
welcum_lbl.place(relx=0.4,rely=0.15)
admin_image = customtkinter.CTkImage(Image.open("admin.png"),size=(150,150))
admin_image_lbl = customtkinter.CTkLabel(master=frame3,text="",image=admin_image)
admin_image_lbl.place(relx=0.03,rely=0.15)
divider_lbl = customtkinter.CTkLabel(master=frame4,text="━━━",text_color='white',font=("Helvetica",40,'bold'),)
divider_lbl.place(relx=0.13,rely=0.35)
hr_lbl = customtkinter.CTkLabel(master=frame4,text="",font=("Helvetica",35,'bold'))
hr_lbl.place(relx=0.15,rely=0.12)
mm_lbl=customtkinter.CTkLabel(master=frame4,text=":",font=("Helvetica",40,'bold'))
mm_lbl.place(relx=0.45,rely=0.05)
min_lbl = customtkinter.CTkLabel(master=frame4,text="",font=("Helvetica",35,'bold'))
min_lbl.place(relx=0.6,rely=0.12)
date_lbl=customtkinter.CTkLabel(master=frame4,text="",font=("Helvetica",20,'bold'))
date_lbl.place(relx=0.2,rely=0.63)
frame5=customtkinter.CTkFrame(master=frame2,width=850,height=330,fg_color="#ffc04d",corner_radius=30) #big rectangle at dashboard
frame5.place(relx=0.028,rely=0.41)
frame6=customtkinter.CTkFrame(master=frame2,width=220,height=210,fg_color="#ffc04d",corner_radius=30) #small square at dashboard
frame6.place(relx=0.72,rely=0.03)
frame7=customtkinter.CTkFrame(master=frame6,width=180,height=170,fg_color="#ffdd80",corner_radius=40)
frame7.place(relx=.09,rely=.09)
frame8=customtkinter.CTkFrame(master=frame5,width=400,height=140,fg_color="#ffdd80",corner_radius=30)
frame8.place(relx=0.02,rely=0.05)
frame9=customtkinter.CTkFrame(master=frame5,width=400,height=140,fg_color="#ffdd80",corner_radius=30)
frame9.place(relx=0.25,rely=0.5)
frame10=customtkinter.CTkFrame(master=frame5,width=400,height=140,fg_color="#ffdd80",corner_radius=30)
frame10.place(relx=0.51,rely=0.05)

bu_logo=customtkinter.CTkImage(Image.open("logo.png"),size=(120,120))
bu_logo_lbl=customtkinter.CTkLabel(master=frame7,text="",image=bu_logo)
bu_logo_lbl.place(relx=0.16,rely=0.07)
bu_lbl=customtkinter.CTkLabel(master=frame7,text="BICOL UNIVERSITY \n POLANGUI",text_color="white",font=("Helvetica",12,'bold'))
bu_lbl.place(relx=0.2,rely=0.8)

studImage=customtkinter.CTkImage(Image.open("stud.png"),size=(150,150))
studImage_lbl=customtkinter.CTkLabel(master=frame8,text="",image=studImage)
studImage_lbl.place(relx=0.07,rely=0.001)
microscopeImage=customtkinter.CTkImage(Image.open("microscope.png"),size=(130,130))
microscopeImage_lbl=customtkinter.CTkLabel(master=frame10,text="",image=microscopeImage)
microscopeImage_lbl.place(relx=0.05,rely=0.003)
calib_logo=customtkinter.CTkImage(Image.open('calibb.png'), size=(180, 100))
calibLogo_lbl=customtkinter.CTkLabel(master=frame9,text="",image=calib_logo)
calibLogo_lbl.place(relx=0.04,rely=0.15)


studAnalysis_lbl=customtkinter.CTkLabel(master=frame8,text="Student\n Analysis",font=("Helvetica",30,'bold'),text_color="white")
studAnalysis_lbl.place(relx=0.52,rely=0.2)
div1=customtkinter.CTkLabel(master=frame8,text="|",font=("Helvetica",80,'bold'),text_color='white')
div1.place(relx=0.45,rely=0.1)

calibAnalysis=customtkinter.CTkLabel(master=frame9,text="Calibration\nAnalysis",font=("Helvetica",30,'bold'),text_color="white")
calibAnalysis.place(relx=0.52,rely=0.22)
div3=customtkinter.CTkLabel(master=frame9,text="|",font=("Helvetica",80,'bold'),text_color='white')
div3.place(relx=0.45,rely=0.1)
inventoryAnalysis_lbl=customtkinter.CTkLabel(master=frame10,text="Inventory\nAnalysis",font=("Helvetica",30,'bold'),text_color='white')
inventoryAnalysis_lbl.place(relx=0.5,rely=0.2)
div2=customtkinter.CTkLabel(master=frame10,text='|',text_color='white',font=("Helvetica",80,'bold'))
div2.place(relx=0.4,rely=0.08)

widgets.extend([frame3,frame4,frame5,frame6,frame7,frame8,frame9,frame10,welcum_lbl,admin_image_lbl,divider_lbl,hr_lbl,mm_lbl,min_lbl,date_lbl,bu_lbl,bu_logo_lbl,studImage_lbl,microscopeImage_lbl,calibLogo_lbl,studAnalysis_lbl,inventoryAnalysis_lbl,calibAnalysis,div1,div2,div3])


def update_time():
    try:
        now = datetime.now()
        month = now.strftime("%m")
        day = now.strftime("%d")
        yr = now.strftime("%y")
        date = f'{day} | {month} | {yr}'
        hr = now.strftime("%H")
        min = now.strftime("%M")

        # Attempt to update the labels
        hr_lbl.configure(text=hr)
        min_lbl.configure(text=min)
        date_lbl.configure(text=date)

    except TclError as e:
        print(f"Error updating label text: {e}")

    # Schedule the next update
data_win.after(1000, update_time)  # Update every 60 seconds

data_win.mainloop()