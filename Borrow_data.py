import sqlite3
import customtkinter
import tkinter as tk
from tkinter import ttk

class borrow:
    def data():

        def update_treeview():

            # dedelete lahat ng nasa treeview
            for item in tree.get_children():
                tree.delete(item)

            # kukunin new data
            c.execute("SELECT * FROM BorrowLog")
            result = c.fetchall()

            # lahat ng bagong data ilalagay
            for item in result:
                tree.insert("", "end", text=item[0], values=(item[1], item[2], item[3], item[4],
                                                             item[5], item[6], item[7]))

            # uupdate treeview every second huhu
            window.after(1000, update_treeview)

        window = customtkinter.CTkToplevel()
        window.geometry("800x300")
        window.title("Borrow Log Data")

        main = sqlite3.connect("Laboratory_Database.db")
        c = main.cursor()

        tree = ttk.Treeview(window)

        tree["columns"] = ("ItemID", "ItemQuantity", "Professor", "Status",
                           "DataIssued", "DateReturned", "Remarks",)

        tree.heading("#0", text="Student ID")
        tree.heading("ItemID", text="Item ID")
        tree.heading("ItemQuantity", text="Item Quantity")
        tree.heading("Professor", text="Professor")
        tree.heading("Status", text="Status")
        tree.heading("DataIssued", text="Data Issued")
        tree.heading("DateReturned", text="Date Returned")
        tree.heading("Remarks", text="Remarks")

        tree.column('#0', width=100, anchor=tk.W)
        tree.column('ItemID', width=20, anchor=tk.CENTER)
        tree.column('ItemQuantity', width=30, anchor=tk.CENTER)
        tree.column('Professor', width=100, anchor=tk.W)
        tree.column('Status', width=50, anchor=tk.W)
        tree.column('DataIssued', width=50, anchor=tk.W)
        tree.column('DateReturned', width=50, anchor=tk.W)
        tree.column('Remarks', width=50, anchor=tk.CENTER)

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
                        font=('Helvetica', 11, 'bold'),
                        background='#007acc',  # blue background for headings
                        foreground='black',  # white text for headings
                        bordercolor='#dddddd',  # border color
                        relief='flat')  # flat relief

        style.map("Treeview",
                  background=[('selected', '#007acc')],  # background color for selected rows
                  foreground=[('selected', '#ffffff')])  # text color for selected rows

        update_treeview()

        tree.pack(expand=True, fill="both")

        # Start updating the Treeview periodically
        update_treeview()

        window.mainloop()
