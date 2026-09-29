import sqlite3
import customtkinter
import tkinter as tk
from tkinter import ttk

class reserve:
    def data():
        def update_treeview():

            # dedelete lahat ng nasa treeview
            for item in tree.get_children():
                tree.delete(item)

            # kukunin new data
            c.execute("SELECT * FROM ReservationLog")
            result = c.fetchall()

            # lahat ng bagong data ilalagay
            for item in result:
                tree.insert("", "end", text=item[0], values=(item[1], item[2], item[3], item[4]))

            # uupdate treeview every second huhu
            window.after(1000, update_treeview)

        window = customtkinter.CTkToplevel()
        window.geometry("800x300")
        window.title("Reservation Data")

        main = sqlite3.connect("Laboratory_Database.db")
        c = main.cursor()

        tree = ttk.Treeview(window)

        tree["columns"] = ("ItemID", "Quantity", "Date", "Status",)

        tree.heading("#0", text="StudentID")
        tree.heading("ItemID", text="ItemID")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Date", text="Date")
        tree.heading("Status", text="Status")

        tree.column('#0', width=170, anchor=tk.W)
        tree.column('ItemID', width=80, anchor=tk.W)
        tree.column('Quantity', width=50, anchor=tk.W)
        tree.column('Date', width=170, anchor=tk.W)
        tree.column('Status', width=120, anchor=tk.W)

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
