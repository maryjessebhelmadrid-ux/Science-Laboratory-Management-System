import sqlite3
import customtkinter
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class inventory:
    def record():

        def update_treeview(sort=True):
            # Clear existing items from the treeview
            for item in tree.get_children():
                tree.delete(item)

            # Retrieve data from the database
            c.execute("SELECT * FROM Inventory")
            result = c.fetchall()

            # Sort the data if sort=True
            if sort:
                result.sort(key=lambda x: x[0])  # Sort by item name (assuming it's the first column)

            # Insert retrieved data into the treeview
            for item in result:
                tree.insert("", "end", text=item[0], values=(item[1], item[2], item[3], item[4], item[5]))

        blue = "#193A6F"
        orange = "#FE7A36"
        yellow = "#ffdd80"

        window = customtkinter.CTkToplevel()
        window.geometry("1000x500")
        window.title("Inventory Data")
        window.config(background=blue)
        window.resizable(False, False)

        main = sqlite3.connect("Laboratory_Database.db")
        c = main.cursor()

        def clear_boxes():
            item_box.delete(0, tk.END)
            description_box.delete(0, tk.END)
            quantity_box.delete(0, tk.END)
            unit_box.delete(0, tk.END)
            remarks_box.delete(0, tk.END)

        # adding new item in database-----------------------------------------------------------------------------------
        def add_func():
            item_name = (item_box.get()).upper()
            item_description = (description_box.get()).upper()
            item_quantity = quantity_box.get()
            item_unit = (unit_box.get()).upper()
            item_remarks = (remarks_box.get()).upper()

            try:  # to check if all the item is filled
                if (item_name == "" or item_description == "" or item_quantity == ""
                        or item_unit == "" or item_remarks == ""):
                    messagebox.showerror("Error", "Please fill all items properly")

                else:
                    c.execute("""SELECT MAX(ItemID) FROM Inventory""")
                    max_item_id = c.fetchone()[0]  # get the maximum ItemID currently in the database

                    if max_item_id is None:
                        new_item_id = "0001"  # if there are no existing items, start with "0001"

                    else:  # increment the maximum ItemID and pad with zeros
                        new_item_id = str(int(max_item_id) + 1).zfill(4)

                    if item_quantity.isdigit():  # to check if the quantity input is valid
                        clear_boxes()

                        with main:  # update all the database needed
                            c.execute("""INSERT INTO Inventory VALUES (?,?,?,?,?,?)""",
                                      (item_name, new_item_id, item_description,
                                       item_quantity, item_unit, item_remarks))

                            c.execute("""INSERT INTO InventoryAnalysis VALUES (?,?,?,?,?,?)""",
                                      (new_item_id, 0, 0, item_quantity, 0, 0))

                            messagebox.showinfo("Imported", "Item Data Added!")

                            update_treeview()
                    else:
                        messagebox.showerror("Error", "Invalid Quantity")
            except:
                messagebox.showerror("Error", "Invalid item fill!")

        # removing or deleting item from all database-------------------------------------------------------------------
        def remove_func():
            selected_item = tree.selection()
            value = tree.item(selected_item)



            if selected_item:  # deleting the item from inventory
                item_id = str(int(value['values'][0])).zfill(4)
                with main:

                    c.execute("""DELETE FROM Inventory WHERE ItemID = ?""", (item_id,))
                    c.execute("""DELETE FROM InventoryAnalysis WHERE ItemID = ?""", (item_id,))
                    main.commit()
                    messagebox.showerror("Deleted", "Item Deleted")

                    update_treeview()

            else:
                messagebox.showerror("Error", "Please select an item!")

        # changing items------------------------------------------------------------------------------------------------
        def update_db(field, new_value, item_id): # function to update database
            with main:
                c.execute(f"""UPDATE Inventory SET {field} = ? WHERE ItemID = ?""",
                          (new_value, item_id))
            main.commit()

        def change_item_name():
            item_id = tree.focus()
            if item_id:
                item_values = tree.item(item_id, "values")
                selected_item_id = item_values[0]
                new_value = (item_box.get()).upper()
                if new_value != "":
                    tree.item(item_id, text=new_value)

                    update_db("ItemName", new_value, selected_item_id)  # update database
                    item_box.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Invalid Name")
            else:
                messagebox.showerror("Error", "Please Select an item")

        def change_description():
            item_id = tree.focus()
            if item_id:
                item_values = tree.item(item_id, "values")
                selected_item_id = item_values[0]
                new_value = (description_box.get()).upper()
                if new_value != "":
                    tree.item(item_id, values=(*tree.item(item_id, "values")[:1], new_value, *tree.item(item_id, "values")[2:]))

                    update_db("Description", new_value, selected_item_id)  # update database
                    description_box.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Invalid description")
            else:
                messagebox.showerror("Error", "Please Select an item")

        def change_quantity():
            item_id = tree.focus()
            if item_id:
                item_values = tree.item(item_id, "values")
                selected_item_id = item_values[0]
                new_value = quantity_box.get()
                if new_value.isdigit() and int(new_value) > 0 and new_value != "":
                    # update treeview and database
                    tree.item(item_id, values=(*tree.item(item_id, "values")[:2], new_value, *tree.item(item_id, "values")[3:]))
                    update_db("Quantity", new_value, selected_item_id)  # update database
                    quantity_box.delete(0, tk.END)

                    c.execute("""UPDATE InventoryAnalysis SET OnHand = ? WHERE ItemID = ?""",
                              (new_value, selected_item_id))
                    main.commit()

                else:
                    messagebox.showerror("Error Quantity", "Invalid Quantity")
            else:
                messagebox.showerror("Error", "Please Select an item")

        def change_unit():
            item_id = tree.focus()
            if item_id:
                item_values = tree.item(item_id, "values")
                selected_item_id = item_values[0]
                new_value = (unit_box.get()).upper()
                if new_value != "":
                    tree.item(item_id, values=(*tree.item(item_id, "values")[:3], new_value, *tree.item(item_id, "values")[4:]))

                    update_db("Unit", new_value, selected_item_id)  # update database
                    unit_box.delete(0,tk.END)

                else:
                    messagebox.showerror("Error", "Invalid Unit")
            else:
                messagebox.showerror("Error", "Please Select an item")

        def change_remarks():
            item_id = tree.focus()
            if item_id:
                item_values = tree.item(item_id, "values")
                selected_item_id = item_values[0]
                new_value = (remarks_box.get()).upper()
                if new_value != "":
                    tree.item(item_id, values=(*tree.item(item_id, "values")[:4], new_value))

                    update_db("Remarks", new_value, selected_item_id)  # update database
                    remarks_box.delete(0, tk.END)

                else:
                    messagebox.showerror("Error", "Invalid Remarks")
            else:
                messagebox.showerror("Error", "Please Select an item")

        def close_window():
            window.destroy()

        inventory_label = customtkinter.CTkLabel(window,
                                                 text="Inventory",
                                                 bg_color=blue,
                                                 font=('Arial', 30, 'bold'))
        inventory_label.place(relx= .83, rely=.09)
        inventory_label.configure(text_color='white')

        item_box = customtkinter.CTkEntry(window,
                                          width=150,
                                          height=28,
                                          bg_color=blue,
                                          font=("Arial", 10, "normal"),
                                          fg_color= 'white',
                                          text_color='black',
                                          corner_radius=5,
                                          placeholder_text="ItemID Name",
                                          )
        item_box.place(relx=0.81, rely = 0.2)

        description_box = customtkinter.CTkEntry(window,
                                                width=150,
                                                height=28,
                                                bg_color=blue,
                                                font=("Arial", 10, "normal"),
                                                fg_color= 'white',
                                                text_color='black',
                                                corner_radius=5,
                                                 placeholder_text=" ItemID Description")
        description_box.place(relx=0.81, rely = 0.3)

        quantity_box = customtkinter.CTkEntry(window,
                                              width=150,
                                              height=28,
                                              bg_color=blue,
                                              font=("Arial", 10, "normal"),
                                              fg_color= 'white',
                                              text_color='black',
                                              corner_radius=5,
                                              placeholder_text="Quantity")
        quantity_box.place(relx=0.81, rely = 0.4)

        unit_box = customtkinter.CTkEntry(window,
                                          width=150,
                                          height=28,
                                          bg_color=blue,
                                          font=("Arial", 10, "normal"),
                                          fg_color= 'white',
                                          text_color='black',
                                          corner_radius=5,
                                          placeholder_text="Unit")
        unit_box.place(relx=0.81, rely = 0.5)

        remarks_box = customtkinter.CTkEntry(window,
                                             width=150,
                                             height=28,
                                             bg_color=blue,
                                             font=("Arial", 10, "normal"),
                                             fg_color= 'white',
                                             text_color='black',
                                             corner_radius=5,
                                             placeholder_text= "Remarks")
        remarks_box.place(relx=0.81, rely = 0.6)

        add_button = customtkinter.CTkButton(window,
                                             text="Add",
                                             bg_color=blue,
                                             corner_radius=5,
                                             width=180,
                                             hover_color= orange,
                                             command=add_func)
        add_button.place(relx= 0.81, rely= 0.77)

        remove_button = customtkinter.CTkButton(window,
                                             text="Remove",
                                             bg_color=blue,
                                             corner_radius=5,
                                             width=180,
                                             hover_color= orange,
                                             fg_color= "#880808",
                                                command=remove_func)
        remove_button.place(relx= 0.81, rely= 0.7)

        change_name_button = customtkinter.CTkButton(window,
                                             text="➨",
                                             bg_color=blue,
                                             corner_radius=5,
                                             width=30,
                                             hover_color= orange,
                                             fg_color= "#228B22",
                                                     command=change_item_name)
        change_name_button.place(relx= 0.965, rely= 0.2)

        change_name_button = customtkinter.CTkButton(window,
                                                     text="➨",
                                                     bg_color=blue,
                                                     corner_radius=5,
                                                     width=30,
                                                     hover_color=orange,
                                                     fg_color="#228B22",
                                                     command=change_description)
        change_name_button.place(relx=0.965, rely=0.3)

        change_quantity_button = customtkinter.CTkButton(window,
                                                     text="➨",
                                                     bg_color=blue,
                                                     corner_radius=5,
                                                     width=30,
                                                     hover_color=orange,
                                                     fg_color="#228B22",
                                                         command=change_quantity)
        change_quantity_button.place(relx=0.965, rely=0.4)

        change_unit_button = customtkinter.CTkButton(window,
                                                     text="➨",
                                                     bg_color=blue,
                                                     corner_radius=5,
                                                     width=30,
                                                     hover_color=orange,
                                                     fg_color="#228B22",
                                                     command=change_unit)
        change_unit_button.place(relx=0.965, rely=0.5)

        change_remarks_button = customtkinter.CTkButton(window,
                                                     text="➨",
                                                     bg_color=blue,
                                                     corner_radius=5,
                                                     width=30,
                                                     hover_color=orange,
                                                     fg_color="#228B22",
                                                        command=change_remarks)
        change_remarks_button.place(relx=0.965, rely=0.6)

        refresh_button = customtkinter.CTkButton(window,
                                                 text="↻",
                                                 bg_color=blue,
                                                 corner_radius=5,
                                                 width=30,
                                                 hover_color= orange,
                                                 fg_color= 'white',
                                                 command=update_treeview,
                                                 text_color='black')
        refresh_button.place(relx= 0.81, rely= 0.9)

        close_button = customtkinter.CTkButton(window,
                                               text="Exit",
                                               bg_color=blue,
                                               fg_color="red",
                                               hover_color=orange,
                                               command=close_window)
        close_button.place(relx=0.85, rely=0.9)

        # Treeview Code

        tree = ttk.Treeview(window)

        tree["columns"] = ("ItemID", "Description", "Quantity", "Unit", "Remarks")

        tree.heading("#0", text="ItemName")
        tree.heading("ItemID", text="ItemID")
        tree.heading("Description", text="Description")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Unit", text="Unit")
        tree.heading("Remarks", text="Remarks")

        tree.column('#0', width=170, anchor=tk.W)
        tree.column('ItemID', width=50, anchor=tk.W)
        tree.column('Description', width=50, anchor=tk.W)
        tree.column('Quantity', width=30, anchor=tk.CENTER)
        tree.column('Unit', width=10, anchor=tk.W)
        tree.column('Remarks', width=100, anchor=tk.W)

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
                  foreground=[('selected', '#ffffff')])  # text color for selected rows))

        update_treeview()

        tree.place(relx= 0, rely= 0, relwidth= 0.8, relheight=1)

        window.mainloop()
