import sqlite3
import tkinter
from tkinter import messagebox
import customtkinter
import tkinter as tk
from tkinter import ttk

class maitenance:


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
            c.execute("SELECT * FROM Maintenance")
            result = c.fetchall()

            # Sort the data if sort=True
            if sort:
                result.sort(key=lambda x: x[0])  # Sort by item name (assuming it's the first column)

            # Insert retrieved data into the treeview
            for item in result:
                tree.insert("", "end", text=item[0], values=(item[1], item[2], item[3], item[4]))

        def clear_entries():
            task_entry.delete(0, tkinter.END)
            frequency_entry.delete(0, tkinter.END)
            party_entry.delete(0, tkinter.END)
            action_entry.delete(0, tkinter.END)
            notes_entry.delete("1.0", "end-1c")

        # add function, adding new data---------------------------------------------------------------------------------
        def add_function():
            #
            new_task = task_entry.get()
            new_frequency = frequency_entry.get()
            new_party = party_entry.get()
            new_action = action_entry.get()
            new_note = notes_entry.get("1.0", "end-1c")

            if new_task == "" or new_frequency == "" or new_party == "" or new_action == "" or new_note == "":
                messagebox.showerror("Error", "Please fill all data needed.")
            else:
                    clear_entries()

                    with main:
                        c.execute("""INSERT INTO Maintenance VALUES (?,?,?,?,?)""",
                                  (new_task, new_frequency, new_party, new_action, new_note))
                    main.commit()
                    update_treeview()

                    messagebox.showinfo("Added", "Item Added")

        # delete or remove a data from the database---------------------------------------------------------------------
        def remove_function():
            selected_item = tree.selection()
            value = tree.item(selected_item)

            if selected_item:

                selected_task = value['text']
                selected_freq = value['values'][0]
                selected_party = value['values'][1]
                with main:
                    c.execute("""DELETE FROM Maintenance WHERE Task = ? AND Frequency = ? AND Responsible_Party = ?""",
                              (selected_task, selected_freq, selected_party))
                update_treeview()
                messagebox.showinfo("Removed", "Item Deleted")

            else:
                messagebox.showerror("Error", "Please Select an Item..")

        def return_function():
            pass

        # function of updating database with specified field------------------------------------------------------------
        def update_db(field, new_value, task): # function to update database
            with main:
                c.execute(f"""UPDATE Maintenance SET {field} = ? WHERE Task = ?""",
                          (new_value, task))
            main.commit()

        # function of changing specified value--------------------------------------------------------------------------
        unselected = "Please select an item"
        invalid = "Input Invalid"

        def change_frequency():  # function of changing frequency
            select = tree.focus()
            task = tree.item(select, "text")

            if select:  # if there is a selected item
                new_value = frequency_entry.get()  # the new input value
                if new_value != "":  # to check if blank
                    tree.item(select, values=(new_value, *tree.item(select, "values")[1:]))
                    update_db("Frequency", new_value, task)  # updates new item
                    update_treeview()  # update treeview

                    frequency_entry.delete(0, tk.END)

                else:  # invalid input
                    messagebox.showerror("Error", invalid)
            else:  # not yet selected error
                messagebox.showerror("Error", unselected)

        def change_party():  # function of changing party responsible
            select = tree.focus()
            task = tree.item(select, "text")
            if select:
                new_value = party_entry.get()
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[2:]))
                    update_db("Responsible_Party", new_value, task)
                    update_treeview()

                    party_entry.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        def change_action():  # function of changing action taken
            select = tree.focus()
            task = tree.item(select, "text")
            if select:
                new_value = action_entry.get()
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[3:]))
                    update_db("Action_Taken", new_value, task)
                    update_treeview()

                    action_entry.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)

        def change_notes():  # function of changing notes
            select = tree.focus()
            task = tree.item(select, "text")
            if select:
                new_value = notes_entry.get("1.0", "end-1c")
                if new_value != "":
                    tree.item(select, values=(new_value, *tree.item(select, "values")[4:]))
                    update_db("Notes", new_value, task)
                    update_treeview()

                    notes_entry.delete("1.0", "end-1c")
                else:
                    messagebox.showerror("Error", invalid)
            else:
                messagebox.showerror("Error", unselected)
            print("notes")

        window = customtkinter.CTkToplevel()
        window.geometry("1000x500")
        window.title("Maintenance")
        window.resizable(False, False)

        def close_window():
            window.destroy()

        main = sqlite3.connect("Laboratory_Database.db")
        c = main.cursor()

        tree = ttk.Treeview(window)

        tree["columns"] = ("Frequency", "Responsible_Party", "Action_Taken", "Notes")

        tree.heading("#0", text="Task")
        tree.heading("Frequency", text="Frequency")
        tree.heading("Responsible_Party", text="Responsible Party")
        tree.heading("Action_Taken", text="Action Taken")
        tree.heading("Notes", text="Notes")

        tree.column('#0', width=30, anchor=tk.W)
        tree.column('Frequency', width=10, anchor=tk.CENTER)
        tree.column('Responsible_Party', width=10, anchor=tk.CENTER)
        tree.column('Action_Taken', width=10, anchor=tk.CENTER)
        tree.column('Notes', width=10, anchor=tk.CENTER)

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
                                            height=500)
        menu_frame.place(relx=0.8, rely=0)

        maintenance_text = customtkinter.CTkLabel(menu_frame,
                                                  text="Maintenance",
                                                  font=("Arial", 20, "bold"),
                                                  text_color="white")
        maintenance_text.place(relx=0.15, rely=0.06)

        task_entry = customtkinter.CTkEntry(menu_frame,
                                            placeholder_text="Task",
                                            width=180)
        task_entry.place(relx=0.06, rely=0.15)

        frequency_entry = customtkinter.CTkEntry(menu_frame,
                                            placeholder_text="Frequency",
                                            width=150)
        frequency_entry.place(relx=0.06, rely=0.25)

        party_entry = customtkinter.CTkEntry(menu_frame,
                                            placeholder_text="Party Responsible",
                                            width=150)
        party_entry.place(relx=0.06, rely=0.35)

        action_entry = customtkinter.CTkEntry(menu_frame,
                                            placeholder_text="Action Taken",
                                              width=150)
        action_entry.place(relx=0.06, rely=0.45)

        note_text = customtkinter.CTkLabel(menu_frame,
                                           text="Notes:",
                                           anchor="w",
                                           fg_color=blue,
                                           width=200)
        note_text.place(relx=0.06, rely=0.51)

        notes_entry = customtkinter.CTkTextbox(menu_frame,
                                               height=100,
                                               bg_color=blue,
                                               fg_color="white",
                                               text_color=black,
                                               width=175)
        notes_entry.place(relx=0.06, rely=0.57)

        add_button = customtkinter.CTkButton(menu_frame,
                                             text="Add",
                                             width=145,
                                             command=add_function,)
        add_button.place(relx=0.06, rely=0.78)

        remove_button = customtkinter.CTkButton(menu_frame,
                                                text="Remove",
                                                width=175,
                                                fg_color="#880808",
                                                command=remove_function)
        remove_button.place(relx=0.06, rely=0.85)

        change_frequency = customtkinter.CTkButton(menu_frame,
                                                text="➨",
                                                width=25,
                                                fg_color="#228B22",
                                                command=change_frequency)
        change_frequency.place(relx=0.82, rely=0.25)

        change_party = customtkinter.CTkButton(menu_frame,
                                                text="➨",
                                                width=25,
                                                fg_color="#228B22",
                                                command=change_party)
        change_party.place(relx=0.82, rely=0.35)

        change_action = customtkinter.CTkButton(menu_frame,
                                                text="➨",
                                                width=25,
                                                fg_color="#228B22",
                                                command=change_action)
        change_action.place(relx=0.82, rely=0.45)

        change_notes = customtkinter.CTkButton(menu_frame,
                                                text="➨",
                                                width=25,
                                                fg_color="#228B22",
                                                command=change_notes)
        change_notes.place(relx=0.8, rely=0.78)

        refresh_button = customtkinter.CTkButton(menu_frame,
                                                 text="↻",
                                                 width=25,
                                                 fg_color="white",
                                                 text_color="black",
                                                 command=update_treeview)
        refresh_button.place(relx=0.06, rely=0.92)

        close_button = customtkinter.CTkButton(window,
                                               text="Exit",
                                               bg_color=blue,
                                               fg_color="red",
                                               hover_color=orange,
                                               command=close_window)
        close_button.place(relx=0.846, rely=0.92)


        window.mainloop()


