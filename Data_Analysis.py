import sqlite3
import customtkinter
import tkinter as tk
from tkinter import ttk


class data_analysis:

    def record():

        data = [20, 10, 10, 1, 1, 1, 1, 5, 2, 15, 22, 10, 17, 3,
                3, 5, 2, 10, 6, 2, 5, 3, 10, 9, 11, 15, 3, 2, 1,
                3, 46, 1, 20, 5, 5, 5, 15, 6, 18, 7, 1, 80, 1, 5,
                13, 7, 7, 12, 1, 10, 1, 1, 1, 7, 22, 4, 10, 10,
                17, 4, 6, 1, 10, 1, 5, 7, 5, 5, 4, 28, 10, 11,
                16, 5, 384, 56, 156, 88, 26, 2, 26, 2, 15, 9, 3,
                10, 6, 2, 2, 1, 5, 26, 13, 10, 1]

        def update_treeview(sort=True):
            # Clear existing items from the treeview
            for item in tree.get_children():
                tree.delete(item)

            # Retrieve data from the database
            c.execute("SELECT * FROM InventoryAnalysis")
            result = c.fetchall()

            # Sort the data if sort=True
            if sort:
                result.sort(key=lambda x: x[0])  # Sort by item name (assuming it's the first column)

            # Insert retrieved data into the treeview
            for item in result:
                tree.insert("", "end", text=item[0], values=(item[1], item[2], item[3], item[4], item[5]))

            window.after(1000, update_treeview)

        window = customtkinter.CTkToplevel()
        window.geometry("900x300")
        window.title("Data Analysis")

        main = sqlite3.connect("Laboratory_Database.db")
        c = main.cursor()

        tree = ttk.Treeview(window)

        tree["columns"] = ("BorrowedItem", "ReservedItem", "OnHand", "BorrowingFrequency", "ReservingFrequency",)

        tree.heading("#0", text="ItemID")
        tree.heading("BorrowedItem", text="Borrowed Item")
        tree.heading("ReservedItem", text="Reserved tem")
        tree.heading("OnHand", text="On Hand")
        tree.heading("BorrowingFrequency", text="Borrowing Frequency")
        tree.heading("ReservingFrequency", text="Reserving Frequency")

        tree.column('#0', width=30, anchor=tk.W)
        tree.column('BorrowedItem', width=10, anchor=tk.W)
        tree.column('ReservedItem', width=10, anchor=tk.CENTER)
        tree.column('OnHand', width=10, anchor=tk.CENTER)
        tree.column('BorrowingFrequency', width=10, anchor=tk.CENTER)
        tree.column('ReservingFrequency', width=10, anchor=tk.CENTER)

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

        tree.pack(expand=True, fill="both")

        # Start updating the Treeview periodically
        update_treeview()


        window.mainloop()

