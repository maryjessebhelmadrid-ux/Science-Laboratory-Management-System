import datetime
import sqlite3
import tkinter
from tkinter import messagebox
import customtkinter
import tkinter as tk
from tkinter import ttk

class Calibration:
    def record():
        yellow = "#ffdd80"
        blue = "#193A6F"
        orange = "#ffa500"
        light_orange = "#ffc04d"
        gray = "#333333"
        black = "#343a40"

        def update_treeview(sort=True):
            # Clear existing items from the treeview
            for item in tree.get_children():
                tree.delete(item)

            # Retrieve data from the database
            c.execute("SELECT * FROM Calibration")
            result = c.fetchall()

            # Sort the data if sort=True
            if sort:
                result.sort(key=lambda x: x[0])  # Sort by item name (assuming it's the first column)

            # Insert retrieved data into the treeview
            for item in result:
                tree.insert("", "end", text=item[0], values=(item[1], item[2], item[3], item[4],
                                                             item[5], item[6], item[7]))

        def clear_entries():
            equipment_entry.delete(0, tkinter.END)
            identification_entry.delete(0, tkinter.END)
            technician_entry.delete(0, tkinter.END)
            date_calibrated_entry.delete(0, tkinter.END)
            remarks_entry.delete(0, tkinter.END)

        # add function, adding new data---------------------------------------------------------------------------------
        def add_function():
            new_equipment = equipment_entry.get()
            new_identification = identification_entry.get()
            new_technician = technician_entry.get()
            new_calibration_due = due_entry.get()
            new_calibration_done = done_entry.get()
            new_date_calibrated = date_calibrated_entry.get()
            new_remarks = remarks_entry.get()

            if (new_equipment == "" or new_equipment == "" or new_identification == "" or new_technician == "" or
                    new_calibration_due == "" or new_calibration_done == "" or new_date_calibrated == "" or new_remarks == ""):
                messagebox.showerror("Error", "Please fill all data needed.")
            else:
                c.execute("""SELECT * FROM Calibration WHERE Equipment = ?""", (new_equipment,))
                existing_item = c.fetchall()
                if existing_item:
                    clear_entries()
                    messagebox.showerror("Error", "Equipment already in progress")
                else:
                    clear_entries()

                    with main:
                        c.execute("""INSERT INTO Calibration VALUES (?,?,?,?,?,?,?,?)""",
                                  (date_now, new_equipment, new_identification, new_technician, new_calibration_due,
                                   new_calibration_done, new_date_calibrated, new_remarks))
                    main.commit()
                    update_treeview()

                    messagebox.showinfo("Added", "Item Added")

        # delete or remove a data from the database---------------------------------------------------------------------
        def remove_function():
            selected_item = tree.selection()
            value = tree.item(selected_item)

            if selected_item:
                selected_equipment = value['values'][0]
                with main:
                    c.execute("""DELETE FROM Calibration WHERE Equipment = ?""",
                              (selected_equipment, ))
                update_treeview()
                messagebox.showinfo("Removed", "Item Deleted")

            else:
                messagebox.showerror("Error", "Please Select an Item..")

        def return_function():
            pass

        # function of updating database with specified field------------------------------------------------------------
        def update_db(field, new_value, task): # function to update database
            with main:
                c.execute(f"""UPDATE Calibration SET {field} = ? WHERE Equipment = {task}""",
                          (new_value,))
            main.commit()

        # function of changing specified value--------------------------------------------------------------------------
        unselected = "Please select an item"
        invalid = "Input Invalid"

        def change_equipment():  # function of changing equipment
            select = tree.focus()
            if select:  # if there is a selected item
                task = tree.item(select, "values")
                new_value = equipment_entry.get()  # the new input value
                print(task)
                if new_value != "":  # to check if blank

                    with main:
                        c.execute(f"""UPDATE Calibration SET Equipment = ? WHERE Identification = ?""",
                                  (new_value, task[1]))
                    main.commit()  # update treeview

                    tree.item(select, values=(new_value, *tree.item(select, "values")[0:]))
                    equipment_entry.delete(0, tk.END)
                    update_treeview()

                else:  # invalid input
                    messagebox.showerror("Error", invalid)
            else:  # not yet selected error
                messagebox.showerror("Error", unselected)

        def change_identification():  # function of changing party responsible
            select = tree.focus()

            if select:
                task = tree.item(select, "values")
                new_value = identification_entry.get()
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[2:]))
                    with main:
                        c.execute(f"""UPDATE Calibration SET Identification = ? WHERE Equipment = ?""",
                                  (new_value, task[0]))
                    main.commit()  # update treeview
                    update_treeview()

                    identification_entry.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        def change_technician():  # function of changing action taken
            select = tree.focus()

            if select:
                task = tree.item(select, "values")
                new_value = technician_entry.get()
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[3:]))
                    with main:
                        c.execute(f"""UPDATE Calibration SET Technician = ? WHERE Equipment = ?""",
                                  (new_value, task[0]))
                    update_treeview()

                    technician_entry.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        def change_calibration_due():
            select = tree.focus()

            if select:
                task = tree.item(select, "values")
                new_value = due_entry.get()
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[4:]))
                    with main:
                        c.execute(f"""UPDATE Calibration SET CalibrationDue = ? WHERE Equipment = ?""",
                                  (new_value, task[0]))
                    main.commit()  # update treeview
                    update_treeview()

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        def change_calibration_done():
            select = tree.focus()
            if select:
                task = tree.item(select, "values")
                new_value = done_entry.get()
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[5:]))
                    with main:
                        c.execute(f"""UPDATE Calibration SET CalibrationDone = ? WHERE Equipment = ?""",
                                  (new_value, task[0]))
                    main.commit()
                    update_treeview()

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        def change_date_calibrated():
            select = tree.focus()
            if select:
                task = tree.item(select, "values")
                new_value = date_calibrated_entry.get()
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[6:]))
                    with main:
                        c.execute(f"""UPDATE Calibration SET DateCalibrated = ? WHERE Equipment = ?""",
                                  (new_value, task[0]))
                    main.commit()
                    update_treeview()

                    date_calibrated_entry.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        def change_remarks():
            select = tree.focus()

            new_value = remarks_entry.get()
            if select:
                task = tree.item(select, "values")
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[7:]))
                    with main:
                        c.execute(f"""UPDATE Calibration SET Remarks = ? WHERE Equipment = ?""",
                                  (new_value, task[0]))
                    main.commit()
                    update_treeview()

                    remarks_entry.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        window = customtkinter.CTkToplevel()
        window.geometry("1000x600")
        window.title("Calibration")
        window.resizable(False, False)

        main = sqlite3.connect("Laboratory_Database.db")
        c = main.cursor()

        tree = ttk.Treeview(window)

        tree["columns"] = ("Equipment", "Identification", "Technician", "CalibrationDue", "CalibrationDone",
                           "DateCalibrated", "Remarks")

        tree.heading("#0", text="Date")
        tree.heading("Equipment", text="Equipment")
        tree.heading("Identification", text="Identification")
        tree.heading("Technician", text="Technician")
        tree.heading("CalibrationDue", text="CalibrationDue")
        tree.heading("CalibrationDone", text="CalibrationDone")
        tree.heading("DateCalibrated", text="DateCalibrated")
        tree.heading("Remarks", text="Remarks")

        tree.column('#0', width=30, anchor=tk.W)
        tree.column('Equipment', width=10, anchor=tk.CENTER)
        tree.column('Identification', width=10, anchor=tk.CENTER)
        tree.column('Technician', width=10, anchor=tk.CENTER)
        tree.column('CalibrationDue', width=10, anchor=tk.CENTER)
        tree.column('CalibrationDone', width=10, anchor=tk.CENTER)
        tree.column('DateCalibrated', width=10, anchor=tk.CENTER)
        tree.column('Remarks', width=10, anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Treeview",
                        rowheight=25,
                        font=('Helvetica', 11),
                        background='#f8f8f8',  # light background
                        foreground='#333333',  # dark text
                        fieldbackground='#f8f8f8',  # light background for the entry field
                        bordercolor='#dddddd',  # border color
                        relief='flat')  # flat relief

        style.configure("Treeview.Heading",
                        font=('Helvetica', 13, 'bold'),
                        background='#007acc',  # blue background for headings
                        foreground='black',  # white text for headings
                        bordercolor='#dddddd',  # border color
                        relief='flat')  # flat relief

        style.map("Treeview",
                  background=[('selected', '#007acc')],  # background color for selected rows
                  foreground=[('selected', '#ffffff')])  # text color for selected rows

        update_treeview()

        tree.place(relx= 0, rely= 0, relwidth= 0.8, relheight=1)

        menu_frame = customtkinter.CTkFrame(window,
                                            fg_color=blue,
                                            corner_radius=0,
                                            width=200,
                                            height=700)
        menu_frame.place(relx=0.8, rely=0)

        calibration_text = customtkinter.CTkLabel(menu_frame,
                                                  text="Calibration",
                                                  font=("Arial", 20, "bold"),
                                                  text_color="white")
        calibration_text.place(relx=0.15, rely=0.06)

        date_now = datetime.datetime.now().strftime("%x")

        date_entry = customtkinter.CTkLabel(menu_frame,
                                            text=f"Date: {date_now}",
                                            width=180,
                                            anchor="w")
        date_entry.place(relx=0.06, rely=0.15)

        equipment_entry = customtkinter.CTkEntry(menu_frame,
                                                 placeholder_text="Equipment",
                                                 width=150)
        equipment_entry.place(relx=0.06, rely=0.22)

        identification_entry = customtkinter.CTkEntry(menu_frame,
                                                      placeholder_text="Identification",
                                                      width=150)
        identification_entry.place(relx=0.06, rely=0.29)

        technician_entry = customtkinter.CTkEntry(menu_frame,
                                                  placeholder_text="Technician(Agency)",
                                                  width=150)
        technician_entry.place(relx=0.06, rely=0.36)

        due_values = ["Yes", "No"]

        due_entry = customtkinter.CTkComboBox(menu_frame,
                                              width=150,
                                              values=due_values)
        due_entry.place(relx=0.06, rely=0.43)

        done_entry = customtkinter.CTkComboBox(menu_frame,
                                               width=150,
                                               values=due_values)
        done_entry.place(relx=0.06, rely=0.50)

        date_calibrated_entry = customtkinter.CTkEntry(menu_frame,
                                                 placeholder_text="Date Done(MM/DD/YY)",
                                                 width=150)
        date_calibrated_entry.place(relx=0.06, rely=0.57)

        remarks_entry = customtkinter.CTkEntry(menu_frame,
                                         placeholder_text="Remarks",
                                         width=150)
        remarks_entry.place(relx=0.06, rely=0.64  )

        add_button = customtkinter.CTkButton(menu_frame,
                                             text="Add",
                                             width=175,
                                             command=add_function)
        add_button.place(relx=0.06, rely=0.7)

        remove_button = customtkinter.CTkButton(menu_frame,
                                                text="Remove",
                                                width=175,
                                                fg_color="#880808",
                                                command=remove_function)
        remove_button.place(relx=0.06, rely=0.75)

        change_equipment = customtkinter.CTkButton(menu_frame,
                                                   text="➨",
                                                   width=25,
                                                   fg_color="#228B22",
                                                   command=change_equipment)
        change_equipment.place(relx=0.82, rely=0.22)

        change_identification = customtkinter.CTkButton(menu_frame,
                                               text="➨",
                                               width=25,
                                               fg_color="#228B22",
                                               command=change_identification)
        change_identification.place(relx=0.82, rely=0.29)

        change_technician = customtkinter.CTkButton(menu_frame,
                                                text="➨",
                                                width=25,
                                                fg_color="#228B22",
                                                command=change_technician)
        change_technician.place(relx=0.82, rely=0.36)

        change_calibration_due = customtkinter.CTkButton(menu_frame,
                                                    text="➨",
                                                    width=25,
                                                    fg_color="#228B22",
                                                    command=change_calibration_due)
        change_calibration_due.place(relx=0.82, rely=0.43)

        change_calibration_done = customtkinter.CTkButton(menu_frame,
                                                    text="➨",
                                                    width=25,
                                                    fg_color="#228B22",
                                                    command=change_calibration_done)
        change_calibration_done.place(relx=0.82, rely=0.50)

        change_date_calibrated = customtkinter.CTkButton(menu_frame,
                                                 text="➨",
                                                 width=25,
                                                 fg_color="#228B22",
                                                 command=change_date_calibrated)
        change_date_calibrated.place(relx=0.82, rely=0.57)

        change_remarks = customtkinter.CTkButton(menu_frame,
                                                    text="➨",
                                                    width=25,
                                                    fg_color="#228B22",
                                                    command=change_remarks)
        change_remarks.place(relx=0.82, rely=0.64)

        refresh_button = customtkinter.CTkButton(menu_frame,
                                                 text="↻",
                                                 width=25,
                                                 fg_color="white",
                                                 text_color="black",
                                                 command=update_treeview)
        refresh_button.place(relx=0.06, rely=0.8)

        window.mainloop()

