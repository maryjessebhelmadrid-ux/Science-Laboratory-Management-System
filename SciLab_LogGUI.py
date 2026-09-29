import datetime
import tkinter
import tkinter.ttk
from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import Image
from round import *
import sqlite3

class service:

    global chosen_acc
    chosen_acc = {'name': 'SEM Cesar S de Paula',
                  'course': 'BSCPE',
                  'block': '2B',
                  'student_id': '2023-6679-74617'}

    # to be accessed by other system
    def __init__(self):
        self.chosen_acc = chosen_acc
    def get_chosen_acc(self):
        return self.chosen_acc

    # --------------------------------------------starting code of the system-------------------------------------------
    def student_service():

        # main window attribute

        window = customtkinter.CTk()
        window.geometry("800x600+500+50")
        window.title('Science Lab Manager')
        window.resizable(False, False)

        # connect to database
        main = sqlite3.connect("Laboratory_Database.db")
        c = main.cursor()

        customtkinter.set_appearance_mode("Light")

        # colors to be used
        orange = "#FE7A36"
        d_blue = "#3652AD"
        blue = "#193A6F"
        white = "#E9F6FF"
        white2 = "#FEFBF3"

        # images used
        bg_photo = customtkinter.CTkImage(dark_image=Image.open("logo.png"), size=(70, 70))  # background photo
        bu_photo = customtkinter.CTkImage(dark_image=Image.open("bu_home_high.png"), size=(800, 600))  # bu logo

        widgets_holder = []

        # to clear all the placed widgets
        def clear_widgets():
            for i in widgets_holder:
                i.destroy()

        # function to log out
        def logout():
            chosen_acc.clear()
            window.destroy()

        # data privacy screen-------------------------------------------------------------------------------------------
        def info_borrow():
            clear_widgets()

            reserve_button.configure(fg_color=blue, state='normal')
            info_button.configure(fg_color=orange, state='disabled')
            return_button.configure(fg_color=blue, state='normal')
            borrow_button.configure(fg_color=blue, state='normal')

            user_privacy_bg = customtkinter.CTkFrame(window,
                                                     bg_color=orange,
                                                     fg_color=orange,
                                                     width=750,
                                                     height=400)
            user_privacy_bg.place(relx=0.01, rely=0.2)

            # user data privacy
            user_privacy = customtkinter.CTkLabel(window,
                                                  text="\n\n\n\n\tThis Data Privacy Policy is to assure the users that their given personal "
                                                       "information will be protected by the authorized \nand unreachable to the"
                                                       " unauthorized of the system access. This will show how we make use and "
                                                       "protect your data when you \ninteract with our system services.\n\n"
                                                       "Informations we collect:\n\n"
                                                       "\t When you use our system, we may collect the following types of information:\n\n"
                                                       "           1.   Personal Information: This includes your name, student number, college program, block and year.\n"
                                                       "           2.   Borrowing Information: Our system will automatically collect your borrowing list and \n\t store it to keep "
                                                       "track of the laboratory equipment inventory, this will include the \n"
                                                       "           3.   ReservationLog Information: This is to know when you will be using the science laboratory\n\n"
                                                       "How we use your informations:\n\n"
                                                       "\tWe may use the informations you have given for the following purposes:\n\n"
                                                       "           1.   Authentication: We need to verify if you are a Bicol University "
                                                       "Polangui student by validating your name and student number.\n"
                                                       "           2.   Inventory: We made this system to keep track of the laboratory equipment inventory.\n"
                                                       "           3.	ReservationLog: The system will store the dates that you will reserve for your research group "
                                                       "in avoidance of simultaneous use \n\twith other researchers/laboratory users.\n\n"
                                                       "\tWe do not desire to disseminate the private information you have given us to people who are working "
                                                       "with related systems yet \nunauthorized. We shall ensure you that your data is protected by the Republic "
                                                       "Act 10173 - Data Privacy Act of 2012.",
                                                  width=750,
                                                  height=400,
                                                  bg_color=white,
                                                  font=('Helvetica', 12, 'italic'),
                                                  justify="left",
                                                  anchor=N)
            user_privacy.place(relx=0.03, rely=0.23)

            data_privacy_label = customtkinter.CTkLabel(window,
                                                        text="DATA PRIVACY POLICY",
                                                        font=('Times New Roman', 14, 'bold'),
                                                        fg_color=white,
                                                        bg_color=white,
                                                        height=2, )
            data_privacy_label.place(relx=0.066, rely=0.27)

            widgets_holder.extend([user_privacy, user_privacy_bg, data_privacy_label])

        # function of borrowing item from the system--------------------------------------------------------------------
        def borrow_func():
            clear_widgets()

            reserve_button.configure(fg_color=blue, state='normal')
            info_button.configure(fg_color=blue, state='normal')
            return_button.configure(fg_color=blue, state='normal')
            borrow_button.configure(fg_color=orange, state='disabled')

            borrow_label = customtkinter.CTkLabel(window,
                                                  text="",
                                                  width=100,
                                                  height=375,
                                                  bg_color=orange,
                                                  corner_radius=1000)

            borrow_label.place(relx=0.025, rely=0.23)

            borrow_label2 = customtkinter.CTkLabel(window,
                                                   text="",
                                                   width=100,
                                                   height=375,
                                                   bg_color="#FEFBF3",
                                                   corner_radius=1000)
            borrow_label2.place(relx=0.05, rely=0.2)

            borrow_bg = customtkinter.CTkLabel(window,
                                               text="",
                                               width=320,
                                               height=460,
                                               bg_color="#d2e7d6",
                                               corner_radius=15)
            borrow_bg.place(relx=0.56, rely=0.2)

            confirm_label = customtkinter.CTkLabel(window,
                                                   text="CONFIRMATION",
                                                   font=("Helvetica", 40, 'bold'),
                                                   bg_color="#FEFBF3",
                                                   fg_color=blue,
                                                   corner_radius=10,
                                                   text_color='white')
            confirm_label.place(relx=0.08, rely=0.27)

            # gathering values for list box and sorted alphabetically---------------------------------------------------

            # fetching all the items from inventory
            c.execute("""SELECT ItemName FROM Inventory""")
            list_of_items = c.fetchall()

            # fetching all the description of the item from inventory
            c.execute("""SELECT Description FROM Inventory""")
            des_list_item = c.fetchall()

            c.execute("""SELECT ItemID FROM Inventory""")
            list_item_id = c.fetchall()

            new_list = []  # items and description to be placed

            # inserting all the items and description fetched together
            for number in range(len(list_of_items)):  # format: item_name<item_description>
                new_list.append(f"{list_item_id[number][0]}:{list_of_items[number][0]}<{des_list_item[number][0]}>")

            # sorting the list of items in new_list alphabetically
            sorted_data = sorted(new_list, key=lambda x: x[0])

            item_description_label = customtkinter.CTkLabel(window,
                                                    text="Item:",
                                                    bg_color="#FEFBF3",
                                                    font=('Helvetica', 13, 'italic'))
            item_description_label.place(relx=0.08, rely=0.4)

            item_description = tk.Listbox(window,
                                  height=3,
                                  width=50,
                                  bg=blue,
                                  activestyle='dotbox',
                                  font=("Helvetica", 10, "italic"),
                                  borderwidth=2,
                                  selectbackground=orange)
            item_description.place(relx=0.12, rely=0.4)
            item_description.configure(background=blue, foreground=white2)

            # inserting all the sorted items in the list box------------------------------------------------------------
            for sorted_item in sorted_data:
                item_description.insert("end", sorted_item)

            item_quan_label = customtkinter.CTkLabel(window,
                                                     text="     Item Quantity:",
                                                     bg_color='white',
                                                     font=('Helvetica', 13, 'italic'))
            item_quan_label.place(relx=0.06, rely=0.5)

            # combo box values
            quan_var = IntVar()
            quan_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

            item_qua = customtkinter.CTkComboBox(window,
                                                 variable=quan_var,
                                                 values=quan_values,
                                                 width=75,
                                                 height=32,
                                                 bg_color='white',
                                                 corner_radius=15,
                                                 button_hover_color=blue,
                                                 fg_color="#FEFBF3")
            item_qua.set("0")
            item_qua.place(relx=0.19, rely=0.5)

            professor_label = customtkinter.CTkLabel(window,
                                                     text="Professor:",
                                                     bg_color='white',
                                                     font=('Helvetica', 13, 'italic'))
            professor_label.place(relx=0.103, rely=0.6)

            prof_entry = customtkinter.CTkEntry(window,
                                                placeholder_text="Professor",
                                                width=225,
                                                height=32,
                                                corner_radius=15,
                                                bg_color='white',
                                                fg_color="#FEFBF3")
            prof_entry.place(relx=0.19, rely=0.6)

            global count
            count = 0

            # function of adding item to be borrowed in the treeview(parang note)---------------------------------------
            def add_item_func():

                # to get the selected item in the list box
                selected_indices = item_description.curselection()

                if selected_indices:  # to check if there is a selected item in the list box
                    if item_qua.get() != "0":  # to check if the quantity of the user is valid

                        index = selected_indices[0]  # to get the index based on the selection in the list box
                        selected_item = item_description.get(index)  # to get the item based on the index (item_name)

                        selected_item_id = (selected_item.split(":"))[0]  # output: ItemID

                        c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (selected_item_id,))
                        inventory_selected = c.fetchone()  # fetching the item from inventory with specified parameters

                        if inventory_selected[3] == 0:  # Out of stock checker
                            messagebox.showerror("Error", "Out of Stock")

                        elif int(item_qua.get()) > inventory_selected[3]:  # Low on stock check
                            messagebox.showerror("Error", f"Low on Stock: {inventory_selected[3]}")

                        else:
                            global count

                            if selected_item:
                                same_item = False
                                item = selected_item  # the selected item
                                for item_id in view.get_children():
                                    values = view.item(item_id, 'values')
                                    item_in_treeview = (values[0])
                                    if item == item_in_treeview:
                                        same_item= True

                                if not same_item:
                                    c.execute("""SELECT * FROM BorrowLog WHERE StudentID = ? AND ItemID = ? 
                                    AND Status = 'Pending'""", (chosen_acc['student_id'], selected_item_id,))
                                    pending_item = c.fetchall()

                                    if not pending_item:
                                        quantity = item_qua.get()  # the quantity to be borrowed

                                        view.insert(parent='', index="end", iid=count, text='Parent', values=(item, quantity, ""))
                                        count += 1

                                        item_description.selection_clear(0, tk.END)

                                    else:
                                        messagebox.showerror("Error", "Item still pending on your slip.")

                                else:
                                    messagebox.showerror("Error", "Item Already in the list.")

                            else:  # if any item is not selected
                                messagebox.showerror("Error", "Please select an item!")

                            item_description.selection_clear(0, tk.END)
                    else:  # input quantity invalid
                        messagebox.showerror("Error", "Invalid Quantity.")

                else:  # item not selected
                    messagebox.showerror("Error", "No item selected.")

            def remove():
                item_description.selection_clear(0, tk.END)

                selected_item = view.selection()  # selected item from treeview
                print(selected_item)

                if selected_item:
                    view.delete(selected_item)  # to delete the selected item

                else:  # any item is not selected
                    messagebox.showerror("Select", "Please select an item!")

            def change_item():
                item_description.selection_clear(0, tk.END)
                selected_item = view.selection()  # selected item

                if selected_item:  # to check if there is selected item

                    new_quantity = int(item_qua.get())
                    item_name = view.item(selected_item, 'values')[0]
                    item_remarks = view.item(selected_item, 'values')[2]
                    item_id = item_name.split(":")[0]

                    c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (item_id, ))
                    item_check = c.fetchone()

                    if new_quantity <= item_check[3]:  # to check availability
                        # to change the quantity of the selected value
                        view.item(selected_item, values=(item_name, new_quantity, item_remarks))

                    elif item_check[3] == 0:  # out of stock error
                        messagebox.showerror("Error", "Out of Stocks")

                    else:  # low on stocks error
                        messagebox.showerror("Error", f"Low on Stocks: {item_check[3]}")

                else:
                    messagebox.showerror("Select", "Please select an item!")

            # Starting code of TREEVIEW

            view = tkinter.ttk.Treeview(window, height=10)
            view.grid(row=0, column=0, sticky="nsew")
            view.configure(style="Treeview")
            style = tkinter.ttk.Style()
            style.configure("Treeview", rowheight=20, font=('Helvetica', 10))
            style.configure("Treeview.Heading", font=('Helvetica', 12, 'italic'))
            style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

            # Set grid lines options
            style.map("Treeview", foreground=[('selected', 'black')], background=[('selected', '#FFE0C7')])

            # column
            view['columns'] = ('Item', 'Quantity', 'Remarks')

            view.column("#0", width=0, stretch=NO)
            view.column("Item", anchor=W, width=160)
            view.column("Quantity", anchor=CENTER, width=80)
            view.column('Remarks', anchor=W, width=120)

            # headings
            view.heading("#0", text='Label', anchor=W)
            view.heading("Item", text="Item", anchor=W)
            view.heading("Quantity", text="Quantity", anchor=CENTER)
            view.heading("Remarks", text='Remarks', anchor=W)

            view.place(x=580, y=300)

            item_add_button = customtkinter.CTkButton(window,
                                                      text="Add Item",
                                                      bg_color="#FEFBF3",
                                                      corner_radius=15,
                                                      width=1,
                                                      height=32,
                                                      command=add_item_func,
                                                      fg_color=blue,
                                                      font=('Helvetica', 13, 'normal'),
                                                      state='normal')
            item_add_button.place(relx=0.09, rely=0.7)

            item_remove_button = customtkinter.CTkButton(window,
                                                         text="Remove Item",
                                                         bg_color=white2,
                                                         corner_radius=15,
                                                         width=1,
                                                         height=32,
                                                         command=remove,
                                                         fg_color="#880808",
                                                         font=('Helvetica', 13, 'normal'),
                                                         state='normal')
            item_remove_button.place(relx=0.21, rely=0.7)

            item_change_button = customtkinter.CTkButton(window,
                                                         text="Change Item",
                                                         bg_color=white2,
                                                         corner_radius=15,
                                                         width=1,
                                                         height=32,
                                                         command=change_item,
                                                             fg_color="#228B22",
                                                         font=('Helvetica', 13, 'normal'),
                                                         state='normal')
            item_change_button.place(relx=0.36, rely=0.7)

            note_for_user = customtkinter.CTkLabel(window,
                                                   text="Note: Using reservation will terminate modification",
                                                   font=("Arial", 12, "italic"),
                                                   height=15,
                                                   fg_color=white2,
                                                   text_color="black",
                                                   bg_color=white2
                                                   )
            note_for_user.place(relx=0.06, rely=0.78)

            def borrower_slip():
                global borrowers_name, borrowers_prof, date_now
                borrowers_name = customtkinter.CTkLabel(window,
                                                        text=f"""{chosen_acc['name']}""",
                                                        font=('Times New Roman', 13, 'normal',),
                                                        bg_color="#d2e7d6",
                                                        anchor=W,
                                                        height=2)
                borrowers_name.place(relx=0.7, rely=0.758)

                borrowers_prof = customtkinter.CTkLabel(window,
                                                        text=f"""{(prof_entry.get().upper())}""",
                                                        font=('Times New Roman', 13, 'normal',),
                                                        bg_color="#d2e7d6",
                                                        anchor=W,
                                                        height=2)
                borrowers_prof.place(relx=0.7, rely=0.837)

                date_now = customtkinter.CTkLabel(window,
                                                  text=f"  {(datetime.datetime.now().strftime('%x'))}   ",
                                                  font=('Times New Roman', 13, 'normal'),
                                                  bg_color="#d2e7d6",
                                                  height=2)
                date_now.place(relx=0.85, rely=0.367)

            def update_slipbutton_state(*args):
                selected_prof = prof_entry.get()
                if selected_prof:
                    slip_button.configure(state='normal')
                    submit_button.configure(state='normal')
                else:
                    slip_button.configure(state='disabled')
                    submit_button.configure(state='disabled')

            slip_button = customtkinter.CTkButton(window,
                                                  text="Generate Borrower's Slip",
                                                  bg_color='white',
                                                  fg_color=blue,
                                                  font=('Helvetica', 20, 'bold'),
                                                  command=borrower_slip,
                                                  corner_radius=5,
                                                  width=300,
                                                  state='disabled')
            slip_button.place(relx=0.1, rely=0.9)

            prof_entry.bind("<KeyRelease>", update_slipbutton_state)

            slip_name_label = customtkinter.CTkLabel(window,
                                                     text="BICOL UNIVERSITY",
                                                     font=('Times New Roman', 15, 'bold'),
                                                     bg_color="#d2e7d6")
            slip_name_label.place(relx=0.66, rely=0.23)

            slip_name_label2 = customtkinter.CTkLabel(window,
                                                      text="POLANGUI CAMPUS",
                                                      font=('Times New Roman', 12, 'normal'),
                                                      bg_color="#d2e7d6",
                                                      height=10)
            slip_name_label2.place(relx=0.68, rely=0.27)

            slip_name_label3 = customtkinter.CTkLabel(window,
                                                      text="Polangui, Albay",
                                                      font=('Times New Roman', 12, 'normal'),
                                                      bg_color="#d2e7d6",
                                                      height=10)
            slip_name_label3.place(relx=0.71, rely=0.3)

            divider_label = customtkinter.CTkLabel(window,
                                                   text="━━━━━━━━━━━━━━━━━━━━━━━━",
                                                   font=('Times New Roman', 12, 'normal'),
                                                   bg_color="#d2e7d6",
                                                   height=2)
            divider_label.place(relx=0.58, rely=0.34)

            date_label = customtkinter.CTkLabel(window,
                                                text="Date:__________",
                                                font=('Times New Roman', 13, 'normal'),
                                                bg_color="#d2e7d6",
                                                height=2)
            date_label.place(relx=0.82, rely=0.37)

            borrowers_info = customtkinter.CTkLabel(window,
                                                    text="""Borrower:""",
                                                    font=('Times New Roman', 13, 'normal',),
                                                    bg_color="#d2e7d6",
                                                    anchor=W,
                                                    height=2)
            borrowers_info.place(relx=0.7, rely=0.72)

            borrowers_info2 = customtkinter.CTkLabel(window,
                                                     text="""━━━━━━━━━━━━━━\nName""",
                                                     font=('Times New Roman', 13, 'normal',),
                                                     bg_color="#d2e7d6",
                                                     anchor=W,
                                                     height=2)
            borrowers_info2.place(relx=0.7, rely=0.77)

            borrowers_info3 = customtkinter.CTkLabel(window,
                                                     text="""━━━━━━━━━━━━━━\nIn-charge""",
                                                     font=('Times New Roman', 13, 'normal',),
                                                     bg_color="#d2e7d6",
                                                     anchor=W,
                                                     height=2)
            borrowers_info3.place(relx=0.7, rely=0.85)

            def clear_treeview(tree):
                for item in tree.get_children():
                    tree.delete(item)

            global reserve_slip
            reserve_slip = False

            # updating all the data in database
            def submit_button_function():
                global reserve_slip
                date_for_rec = (datetime.datetime.now()).strftime("%x")
                student_id = chosen_acc['student_id']
                professor = prof_entry.get()

                if reserve_slip:

                    submit_button.configure(state='disabled')

                    c.execute("""SELECT * FROM ReservationLog WHERE StudentID = ? AND Status = 'Pending' """,
                              (chosen_acc['student_id'],))
                    reservation_result = c.fetchall()  # student with reservation

                    for k in reservation_result:
                        with main:

                            # fetch the current values of the item to be changed
                            c.execute("""SELECT * FROM InventoryAnalysis WHERE ItemID = ?""", (k[1],))
                            analysis_db = c.fetchone()

                            # adding new record in BorrowLog
                            c.execute("""INSERT INTO BorrowLOG VALUES (?,?,?,?,?,?,?,?)""",
                                      (student_id, k[1], k[2], professor, 'Pending',
                                       date_for_rec, '---', '---'))

                            # updating reservation log
                            c.execute("""UPDATE ReservationLog SET Status = 'Claimed' WHERE 
                            StudentID = ? AND Status = ?""", (chosen_acc['student_id'], 'Pending'))

                            # new values to record
                            new_borrowed_item = k[2] + analysis_db[1]
                            new_borrowing_frequency = analysis_db[4] + 1
                            new_reserved_item = analysis_db[2] - k[2]

                            # updating the Analysis
                            c.execute("""UPDATE InventoryAnalysis SET BorrowedItem = ?, BorrowingFrequency = ?, 
                                                        ReservedItem = ? WHERE ItemID = ?""",
                                      (new_borrowed_item, new_borrowing_frequency, new_reserved_item, k[1]))

                    reserve_slip = False

                else:
                    submit_button.configure(state='disabled')

                    for x in view.get_children():
                        item_value = view.item(x)['values']  # output: (ItemName, ItemQuantity, Remarks)

                        item_id = ((item_value[0]).split(":"))[0]
                        item_quantity = int(item_value[1])

                        # fetch the current values of the item to be changed
                        c.execute("""SELECT * FROM InventoryAnalysis WHERE ItemID = ?""", (item_id,))
                        analysis_db = c.fetchone()

                        with main:
                            # inserting new record in borrow log
                            c.execute("""INSERT INTO BorrowLOG VALUES (?,?,?,?,?,?,?,?)""",
                                      (student_id, item_id, item_quantity, professor, 'Pending',
                                       date_for_rec, "---", "---"))

                            c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (item_id,))
                            borrow_result = c.fetchone()

                            c.execute("""UPDATE Inventory SET Quantity = ? WHERE ItemID = ?""",
                                      ((borrow_result[3] - item_quantity), item_id))

                            # new values to record
                            new_borrowed_item = item_quantity + analysis_db[1]
                            new_borrowing_frequency = analysis_db[4] + 1
                            new_on_hand_inventory = analysis_db[3] - (new_borrowed_item + analysis_db[2])

                            # updating the Analysis
                            c.execute("""UPDATE InventoryAnalysis SET BorrowedItem = ?, BorrowingFrequency = ?,
                             OnHand = ? WHERE ItemID = ?""",
                                      (new_borrowed_item, new_borrowing_frequency,
                                       new_on_hand_inventory, item_id))
                            main.commit()

                clear_treeview(view)
                borrowers_name.configure(text="")
                borrowers_prof.configure(text="")
                date_now.configure(text="")
                prof_entry.delete(0, END)

            submit_button = customtkinter.CTkButton(window,
                                                    text="➤➤",
                                                    font=('Helvetica', 15, 'bold'),
                                                    width=30,
                                                    height=30,
                                                    fg_color=blue,
                                                    bg_color="#d2e7d6",
                                                    hover_color=orange,
                                                    command=submit_button_function,
                                                    corner_radius=20,
                                                    state='disabled')
            submit_button.place(relx=0.58, rely=0.9)

            global borrow_count
            borrow_count = 0

            c.execute("""SELECT * FROM ReservationLog WHERE StudentID = ? AND Status = 'Pending'""",
                      (chosen_acc['student_id'],))
            result = c.fetchall()
            print(result)

            if result:
                response = messagebox.askyesno("ReservationLog found", "Do you want to use reservation?")
                if not response:
                    response_2 = messagebox.askyesno("Confirmation", "Are you sure?")
                    if response_2:
                        messagebox.showinfo("Cancellation", "ReservationLog Cancelled!")

                        for i in result:
                            with main:
                                c.execute("""UPDATE ReservationLog SET Status = 'Cancelled' WHERE Status = 'Pending'"""
                                          "AND StudentID = ? AND ItemID = ?", (i[0], i[1],))

                                c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (i[1],))
                                got_item = c.fetchone()

                                c.execute("""UPDATE Inventory SET Quantity = ? WHERE ItemID = ?""",
                                          (got_item[3] + i[2], i[1], ))
                                main.commit()

                else:
                    item_add_button.configure(state="disabled")
                    item_change_button.configure(state="disabled")
                    item_remove_button.configure(state="disabled")

                    for i in result:

                        # to fetch the info of the item
                        c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (i[1],))
                        chosen_item = c.fetchone()

                        formatted_item = f"{chosen_item[1]}:{chosen_item[0]}"

                        view.insert(parent='', index="end", iid=borrow_count, text='Parent', values=(formatted_item, i[2], ""))
                        borrow_count += 1

                    reserve_slip = True

            widgets_holder.extend([borrow_bg, borrow_label, borrow_label2, confirm_label, item_description_label,
                                   item_quan_label, item_description, item_qua, professor_label, prof_entry,
                                   item_add_button, slip_button, view, borrowers_info, borrowers_info2, borrowers_info3,
                                   submit_button, date_label, divider_label, slip_name_label, slip_name_label2,
                                   slip_name_label3, item_remove_button, item_change_button])

        # function of returning item from the system--------------------------------------------------------------------
        def return_func():

            try:
                clear_widgets()
                count2 = 0

                reserve_button.configure(fg_color=blue, state='normal')
                info_button.configure(fg_color=blue, state='normal')
                return_button.configure(fg_color=orange, state='disabled')
                borrow_button.configure(fg_color=blue, state='normal')

                return_bg = customtkinter.CTkLabel(window,
                                                   text="---------------------------",
                                                   width=320,
                                                   height=460,
                                                   bg_color="#d2e7d6",
                                                   corner_radius=15)
                return_bg.place(relx=0.05, rely=0.2)

                # starting code of Treeview
                return_view = tkinter.ttk.Treeview(window, height=10)
                return_view.grid(row=0, column=0, sticky="nsew")
                return_view.configure(style="Treeview")
                style = tkinter.ttk.Style()
                style.configure("Treeview", rowheight=20, font=('Helvetica', 10))
                style.configure("Treeview.Heading", font=('Helvetica', 12, 'italic'))
                style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

                # Set grid lines options
                style.map("Treeview", foreground=[('selected', 'black')], background=[('selected', '#FFE0C7')])

                # column
                return_view['columns'] = ('Item', 'Quantity', 'Remarks')

                return_view.column("#0", width=0, stretch=NO)
                return_view.column("Item", anchor=W, width=160)
                return_view.column("Quantity", anchor=CENTER, width=80)
                return_view.column('Remarks', anchor=W, width=120)

                # headings
                return_view.heading("#0", text='Label', anchor=W)
                return_view.heading("Item", text="Item", anchor=W)
                return_view.heading("Quantity", text="Quantity", anchor=CENTER)
                return_view.heading("Remarks", text='Remarks', anchor=W)

                # add data
                def on_click_treeview(*args):  # to put the item text in the description
                    try:
                        selected_item = return_view.selection()
                        item_info = return_view.item(selected_item)

                        item_return.configure(text=f"{((item_info['values'][0]).split('<'))[0]}",
                                              bg_color=white2)
                        item_quan2.configure(text=f"Item quantity:{item_info['values'][1]}")
                        return_item_submitt.configure(state="normal")
                    except:
                        pass

                return_view.place(x=70, y=300)
                return_view.bind("<ButtonRelease-1>", on_click_treeview)

                #
                with main:
                    c.execute("""SELECT * FROM BorrowLog WHERE StudentID = ? AND DateReturned = '---'""",
                              (chosen_acc['student_id'],))
                    result = c.fetchall()

                    for i in result:
                        # to fetch the item name with item id
                        c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (i[1], ))
                        item_name = c.fetchone()
                        formatted_item_name = f"{item_name[1]}:{item_name[0]}"

                        return_view.insert(parent='', index="end", iid=count2,
                                           text='Parent', values=(formatted_item_name, i[2], ""))
                        count2 += 1

                slip_name_label2 = customtkinter.CTkLabel(window,
                                                          text="BICOL UNIVERSITY",
                                                          font=('Times New Roman', 15, 'bold'),
                                                          bg_color="#d2e7d6")
                slip_name_label2.place(relx=0.15, rely=0.23)

                slip_name_label22 = customtkinter.CTkLabel(window,
                                                           text="POLANGUI CAMPUS",
                                                           font=('Times New Roman', 12, 'normal'),
                                                           bg_color="#d2e7d6",
                                                           height=10)
                slip_name_label22.place(relx=0.17, rely=0.27)

                slip_name_label32 = customtkinter.CTkLabel(window,
                                                           text="Polangui, Albay",
                                                           font=('Times New Roman', 12, 'normal'),
                                                           bg_color="#d2e7d6",
                                                           height=10)
                slip_name_label32.place(relx=0.2, rely=0.3)

                divider_label2 = customtkinter.CTkLabel(window,
                                                        text="━━━━━━━━━━━━━━━━━━━━━━━━",
                                                        font=('Times New Roman', 12, 'normal'),
                                                        bg_color="#d2e7d6",
                                                        height=2)
                divider_label2.place(relx=0.07, rely=0.34)

                date_label2 = customtkinter.CTkLabel(window,
                                                     text="Date:__________",
                                                     font=('Times New Roman', 13, 'normal'),
                                                     bg_color="#d2e7d6",
                                                     height=2)
                date_label2.place(relx=0.31, rely=0.37)

                borrowers_info2 = customtkinter.CTkLabel(window,
                                                         text="""Borrower:""",
                                                         font=('Times New Roman', 13, 'normal',),
                                                         bg_color="#d2e7d6",
                                                         anchor=W,
                                                         height=2)
                borrowers_info2.place(relx=0.19, rely=0.72)

                borrowers_info22 = customtkinter.CTkLabel(window,
                                                          text="""━━━━━━━━━━━━━━\nName""",
                                                          font=('Times New Roman', 13, 'normal',),
                                                          bg_color="#d2e7d6",
                                                          anchor=W,
                                                          height=2)
                borrowers_info22.place(relx=0.19, rely=0.77)

                borrowers_info32 = customtkinter.CTkLabel(window,
                                                          text="""━━━━━━━━━━━━━━\nIn-charge""",
                                                          font=('Times New Roman', 13, 'normal',),
                                                          bg_color="#d2e7d6",
                                                          anchor=W,
                                                          height=2)
                borrowers_info32.place(relx=0.19, rely=0.85)

                borrowers_name2 = customtkinter.CTkLabel(window,
                                                         text=f"""{chosen_acc['name']}""",
                                                         font=('Times New Roman', 13, 'normal',),
                                                         bg_color="#d2e7d6",
                                                         anchor=W,
                                                         height=2)
                borrowers_name2.place(relx=0.19, rely=0.758)

                borrowers_prof2 = customtkinter.CTkLabel(window,
                                                         text=f"{result[0][3]}",
                                                         font=('Times New Roman', 13, 'normal',),
                                                         bg_color="#d2e7d6",
                                                         anchor=W,
                                                         height=2)
                borrowers_prof2.place(relx=0.19, rely=0.837)

                date_now2 = customtkinter.CTkLabel(window,
                                                   text=f"  {result[0][5]}   ",
                                                   font=('Times New Roman', 13, 'normal'),
                                                   bg_color="#d2e7d6",
                                                   height=2)
                date_now2.place(relx=0.34, rely=0.367)

                return_frame2 = customtkinter.CTkLabel(window,
                                                       width=300,
                                                       height=300,
                                                       text="",
                                                       bg_color=orange)
                return_frame2.place(relx=0.55, rely=0.17)

                return_frame3 = customtkinter.CTkLabel(window,
                                                       width=300,
                                                       height=300,
                                                       text="",
                                                       bg_color=blue)
                return_frame3.place(relx=0.61, rely=0.23)

                return_frame = customtkinter.CTkLabel(window,
                                                      width=300,
                                                      height=300,
                                                      text="",
                                                      bg_color='white')
                return_frame.place(relx=0.58, rely=0.2)

                verify_label = customtkinter.CTkLabel(window,
                                                      text='VERIFICATION',
                                                      font=('Arial', 35, 'bold'),
                                                      bg_color='white',
                                                      fg_color=blue,
                                                      text_color='white',
                                                      corner_radius=10)
                verify_label.place(relx=0.6, rely=0.24)

                return_values = []

                for i in result:
                    return_values.append(i[4])


                # remarks function
                def return_sub_func():
                    selected_item = return_view.selection()  # the selected item in the treeview

                    if selected_item:
                        new_quantity = rem_var.get()

                        return_view.item(selected_item, values=(return_view.item(selected_item, 'values')[0],
                                                                return_view.item(selected_item, 'values')[1],
                                                                new_quantity))

                    else:
                        messagebox.showerror("Error", "No item selected.")

                def combobox_select(*args):
                    for i in result:
                        if i[4].upper() == return_var.get():
                            item_quan2.configure(text=f"Item quantity:   {i[5]}")

                return_var = StringVar()
                item_return = customtkinter.CTkLabel(window,
                                                     text="",
                                                     bg_color=white2,
                                                     font=('Helvetica', 11, 'italic'))
                item_return.place(relx=0.723, rely=0.343)

                return_var.trace_add("write", combobox_select)

                return_sub_button = customtkinter.CTkButton(window,
                                                            command=return_sub_func,
                                                            corner_radius=20,
                                                            text="Remarks",
                                                            bg_color='white',
                                                            hover_color=blue,
                                                            fg_color=orange)
                return_sub_button.place(relx=0.726, rely=0.61)

                item_description2 = customtkinter.CTkLabel(window,
                                                   text="Item description: ",
                                                   font=('Helvetica', 13, 'italic'),
                                                   bg_color='white')
                item_description2.place(relx=0.6, rely=0.34)

                item_quan2 = customtkinter.CTkLabel(window,
                                                    text=f"Item quantity:   0",
                                                    font=('Helvetica', 13, 'italic'),
                                                    bg_color='white')
                item_quan2.place(relx=0.62, rely=0.43)

                remarks_values = ['Good', 'Defect', 'Broken', 'Pass']
                rem_var = StringVar()
                remarks = customtkinter.CTkComboBox(window,
                                                    values=remarks_values,
                                                    corner_radius=15,
                                                    bg_color='white',
                                                    button_hover_color=blue,
                                                    variable=rem_var)
                remarks.place(relx=0.726, rely=0.52)

                remarks_label = customtkinter.CTkLabel(window,
                                                       text='Remarks: ',
                                                       font=('Helvetica', 13, 'italic'),
                                                       bg_color='white')
                remarks_label.place(relx=0.65, rely=0.52)

                # returning item function where it updates all database-------------------------------------------------
                def add_item_func():

                    with main:
                        selected_item = return_view.selection()
                        item_info = return_view.item(selected_item)

                        selected_item_name = item_info['values'][0]
                        selected_item_id = (item_info['values'][0].split(":"))[0]
                        selected_item_remarks = item_info['values'][2]
                        selected_item_quantity = item_info['values'][1]

                        item_return.configure(text=selected_item_name)

                        c.execute("SELECT * FROM Inventory WHERE ItemID=?", (selected_item_id,))
                        returning_item = c.fetchone()  # to get the info of the selected item in inventory

                        date_returned = (datetime.datetime.now()).strftime("%x")  # date right now

                        c.execute("""SELECT * FROM BorrowLOG WHERE StudentID = ? AND Status = 'Pending' 
                        AND ItemID = ?""", (chosen_acc['student_id'], selected_item_id))
                        acc_return = c.fetchone()  # to get the  borrow record of this account

                        if acc_return is None:  # if there is no borrower presented or already updated
                            messagebox.showerror("Error", "No borrower slip present")

                        else:  # if the pending item is not yet updated or recorded
                            with main:

                                # updating borrow log into returned record
                                c.execute("""UPDATE BorrowLOG SET DateReturned = ?, Status = 'Returned', 
                                             Remarks = ? WHERE StudentID = ? AND ItemID = ? AND Remarks = '---' """,
                                          (date_returned, selected_item_remarks, chosen_acc['student_id'],
                                           selected_item_id))

                                new_quantity = returning_item[3] + selected_item_quantity  # new quantity to record

                                # updating inventory record to update the returned items
                                c.execute("""UPDATE Inventory SET Quantity = ? WHERE ItemID = ?""",
                                          (new_quantity, selected_item_id))

                                # to get the all the values in Data analysis
                                c.execute("""SELECT * FROM InventoryAnalysis WHERE ItemID = ?""", (selected_item_id,))
                                analysis_result = c.fetchone()

                                new_borrowed_item = analysis_result[1] - selected_item_quantity
                                new_on_hand = analysis_result[3] + selected_item_quantity

                                c.execute("""UPDATE InventoryAnalysis SET BorrowedItem = ?, OnHand = ? WHERE ItemID = ?""",
                                          (new_borrowed_item, new_on_hand, selected_item_id))

                            item_selected = return_view.selection()
                            return_view.delete(item_selected)
                            return_item_submitt.configure(state="disabled")
                            item_return.configure(text="")
                            item_quan2.configure(text="Item quantity: ")

                return_item_submitt = customtkinter.CTkButton(window,
                                                              text="RETURN Item",
                                                              font=('Arial', 20, 'bold'),
                                                              width=300,
                                                              height=20,
                                                              hover_color=orange,
                                                              bg_color=blue
                                                              , fg_color=blue,
                                                              text_color='white',
                                                              corner_radius=0,
                                                              border_width=2,
                                                              border_color='gray',
                                                              state='disabled',
                                                              command=add_item_func)
                return_item_submitt.place(relx=0.58, rely=0.85)

                widgets_holder.extend([return_bg, return_view, slip_name_label2, slip_name_label22, slip_name_label32,
                                       divider_label2, date_label2, borrowers_info2, borrowers_info22, borrowers_info32,
                                       return_frame, return_frame2, return_frame3, verify_label, item_description2,
                                       item_quan2, remarks, remarks_label, item_return, return_item_submitt,
                                       return_sub_button, borrowers_name2, borrowers_prof2, date_now2])

                for item in return_view.get_children():
                    return_view.tag_bind(item, "<<TreeviewSelect>>", lambda event, item=item: add_item_func())

            except:
                no_slip_bg = customtkinter.CTkLabel(window,
                                                    text="",
                                                    bg_color=orange,
                                                    width=350)
                no_slip_bg.place(relx=0.4850, rely=0.420)

                no_borrower_slip = customtkinter.CTkLabel(window,
                                                          text="NO BORROWER'S SLIP PRESENT",
                                                          bg_color=d_blue,
                                                          text_color=white2,
                                                          width=350,
                                                          font=('Arial', 20, 'bold'))
                no_borrower_slip.place(relx=0.50, rely=0.40)

                widgets_holder.extend([return_bg, return_view, slip_name_label2, slip_name_label22, slip_name_label32,
                                       divider_label2, date_label2, borrowers_info2, borrowers_info22, borrowers_info32,
                                       borrowers_name2, no_borrower_slip, no_slip_bg])

        # reserving item function of the system-------------------------------------------------------------------------
        def reserve_func():
            clear_widgets()

            reserve_button.configure(fg_color=orange, state='disabled')
            info_button.configure(fg_color=blue, state='normal')
            return_button.configure(fg_color=blue, state='normal')
            borrow_button.configure(fg_color=blue, state='normal')

            global res_count
            res_count = 0

            reserve_bg_label = customtkinter.CTkLabel(window,
                                                      bg_color=orange,
                                                      height=57,
                                                      width=300,
                                                      text="")
            reserve_bg_label.place(relx=0.07, rely=.2)

            reserve_status = customtkinter.CTkLabel(window,
                                                    font=('Arial', 25, 'bold'),
                                                    bg_color=orange,
                                                    fg_color=blue,
                                                    text=f"RESERVATION",
                                                    corner_radius=5,
                                                    text_color=white2,
                                                    width=280)
            reserve_status.place(relx=0.08, rely=0.22)

            reserve_form = customtkinter.CTkLabel(window,
                                                  bg_color=white,
                                                  text="",
                                                  width=300,
                                                  height=350)
            reserve_form.place(relx=0.07, rely=0.35)

            reserve_form_label = customtkinter.CTkLabel(window,
                                                        font=("Times New Roman", 20, "bold"),
                                                        text="RESERVATION FORM",
                                                        bg_color=white)
            reserve_form_label.place(relx=0.128, rely=0.38)

            reserve_name = customtkinter.CTkLabel(window,
                                                  font=("Times New Roman", 13, "normal"),
                                                  text=f"Name: {chosen_acc['name']}",
                                                  bg_color=white,
                                                  height=10)
            reserve_name.place(relx=0.09, rely=0.480)

            reserve_course = customtkinter.CTkLabel(window,
                                                    font=("Times New Roman", 13, "normal"),
                                                    bg_color=white,
                                                    height=10,
                                                    text=f"Course: {chosen_acc['course']}")
            reserve_course.place(relx=.09, rely=0.530)

            reserve_view = tkinter.ttk.Treeview(window, height=10)
            reserve_view.grid(row=0, column=0, sticky="nsew")
            reserve_view.configure(style="Treeview")
            style = tkinter.ttk.Style()
            style.configure("Treeview", rowheight=20, font=('Helvetica', 10))
            style.configure("Treeview.Heading", font=('Helvetica', 12, 'italic'))
            style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

            # Set grid lines options
            style.map("Treeview", foreground=[('selected', 'black')], background=[('selected', '#FFE0C7')])

            # column
            reserve_view['columns'] = ('Item', 'Quantity', 'Date')

            reserve_view.column("#0", width=0, stretch=NO)
            reserve_view.column("Item", anchor=W, width=160)
            reserve_view.column("Quantity", anchor=CENTER, width=80)
            reserve_view.column('Date', anchor=W, width=120)

            # headings
            reserve_view.heading("#0", text="Label", anchor=W)
            reserve_view.heading("Item", text="Item", anchor=W)
            reserve_view.heading("Quantity", text="Quantity", anchor=CENTER)
            reserve_view.heading("Date", text="Date", anchor=W)

            # add data

            reserve_view.place(x=78, y=430)

            reserve_blue_bg = customtkinter.CTkLabel(window,
                                                     bg_color=blue,
                                                     height=440,
                                                     width=350,
                                                     text="")
            reserve_blue_bg.place(relx=0.47, rely=0.17)

            reserve_red_bg = customtkinter.CTkLabel(window,
                                                    bg_color=orange,
                                                    height=440,
                                                    width=350,
                                                    text="")
            reserve_red_bg.place(relx=0.53, rely=0.23)

            reserve_white_bg = customtkinter.CTkLabel(window,
                                                      bg_color=white2,
                                                      height=440,
                                                      width=350,
                                                      text="")
            reserve_white_bg.place(relx=0.5, rely=0.20)

            c.execute("""SELECT ItemName FROM Inventory""")
            list_of_items = c.fetchall()  # to fetch all the item name in the inventory

            c.execute("""SELECT Description FROM Inventory""")
            des_list_item = c.fetchall()  # fetch all the Description in the inventory

            c.execute("""SELECT ItemID FROM Inventory""")
            item_id_list = c.fetchall()  # fetch all the Description in the inventory

            new_list = []
            for i in range(len(list_of_items)):
                new_list.append(f"{item_id_list[i][0]}:{list_of_items[i][0]}<{des_list_item[i][0]}>")

            fill_out_label = customtkinter.CTkLabel(window,
                                                    text="Fill out",
                                                    font=("Arial", 30, "bold"),
                                                    bg_color=white2,
                                                    text_color=white2,
                                                    corner_radius=10,
                                                    fg_color=blue)
            fill_out_label.place(relx=0.63, rely=0.23)

            reserve_item_name = customtkinter.CTkLabel(window,
                                                       bg_color=white2,
                                                       font=("Helvetica", 13, "italic"),
                                                       text="Reserve Item",
                                                       )
            reserve_item_name.place(relx=0.53, rely=0.32)

            reserve_item = tk.Listbox(window,
                                      height=4,
                                      width=50,
                                      bg="grey",
                                      activestyle='dotbox',
                                      font=("Helvetica", 10, "italic"),
                                      fg="yellow",
                                      selectbackground=orange,
                                      borderwidth=2)

            reserve_item.place(relx=0.53, rely=0.37)
            reserve_item.configure(background=blue,
                                   foreground=white2, )

            sorted_data = sorted(new_list, key=lambda x: x[0])

            for i in sorted_data:
                reserve_item.insert("end", i)

            res_quan_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

            reserve_quantity_label = customtkinter.CTkLabel(window,
                                                            text="Quantity",
                                                            font=("Helvetica", 13, "italic"),
                                                            bg_color=white2)
            reserve_quantity_label.place(relx=0.53, rely=0.525)

            reserve_quantity = customtkinter.CTkComboBox(window,
                                                         width=150,
                                                         height=29,
                                                         values=res_quan_values,
                                                         corner_radius=15,
                                                         bg_color=white2,
                                                         )

            reserve_quantity.place(relx=0.53, rely=0.57)

            reserve_quantity.set("0")

            reserve_date = (datetime.datetime.now()).strftime("%x")

            reserve_date_label = customtkinter.CTkLabel(window,
                                                        text=f"Date:\t{reserve_date}",
                                                        font=("Helvetica", 13, "italic"),
                                                        bg_color=white2)
            reserve_date_label.place(relx=0.53, rely=0.65)

            # adding selected value in the treeview
            def reserve_add():
                if reserve_quantity.get() != "0":
                    global res_count

                    if reserve_item.curselection():
                        item = reserve_item.get(reserve_item.curselection()[0])
                        quantity = int(reserve_quantity.get())
                        date = reserve_date
                        selected_item_id = item.split(":")[0]

                        c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (selected_item_id,))
                        selected_item = c.fetchone()  # to get the selected item from the inventory

                        if selected_item[3] >= quantity:
                            already_reserved = False

                            c.execute("""SELECT * FROM ReservationLog WHERE StudentId = ? AND ItemID = ? AND Status = 'Pending'""",
                                      (chosen_acc['student_id'], selected_item_id,))
                            in_reserve = c.fetchall()

                            if in_reserve:
                                already_reserved = True

                            if not already_reserved:
                                reserve_view.insert(parent='', index="end", iid=res_count, text='Parent',
                                                    values=(item, quantity, date))
                                res_count += 1
                                reserve_item.selection_clear(0, tk.END)
                            else:
                                messagebox.showerror("Error", "Item still in your reservation")

                        elif selected_item[2] == 0:
                            messagebox.showerror("Stock Error", "Out of Stock!")
                        else:
                            messagebox.showerror("Stock", "Low on Stock!")
                    else:
                        messagebox.showerror("Select", "Please select an item!")
                else:
                    messagebox.showerror("Error", "Invalid quantity input!")

            # function of deleting an item in the treeview
            def delete_item_func():
                reserve_item.selection_clear(0, tk.END)

                selected_item = reserve_view.selection()

                if selected_item:
                    reserve_view.delete(selected_item)

                else:
                    messagebox.showerror("Select", "Please select an item!")

            # function of changing the quantity of the selected item----------------------------------------------------
            def change_item_func():
                selected_item = reserve_view.focus()

                if selected_item:  # if there is a selected item in the treeview
                    item_value = reserve_view.item(selected_item)['values']
                    selected_item_id = ((item_value[0]).split(":"))[0]
                    selected_item_quantity = (item_value[1])

                    c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (selected_item_id,))
                    item_check = c.fetchone()  # fetched item from inventory

                    new_quantity = int(reserve_quantity.get())  # the selected quantity of the user

                    if new_quantity == 0:  # to check if quantity is 0
                        messagebox.showerror("Quantity Error", "Invalid Quantity!")

                    elif new_quantity <= item_check[3]:  # to check if the quantity is valid
                        reserve_view.item(selected_item, values=(reserve_view.item(selected_item, 'values')[0],
                                                                 new_quantity,
                                                                 reserve_view.item(selected_item, 'values')[2]))
                    elif item_check[3] == 0:  # to check if the is stocks
                        messagebox.showerror("stock Error", "Out of Stock!")

                    else:
                        messagebox.showerror("Stock Error", "Low on Stocks")

                else:
                    messagebox.showerror("Select", "Please select an item!")

                reserve_item.selection_clear(0, tk.END)

            # function of finalizing and recording of reservation
            def reserve_submit():

                def clear_treeview():
                    reserve_view.delete(*reserve_view.get_children())
                    tree_date.clear()
                    tree_id.clear()
                    tree_quantities.clear()
                    reserve_quantity.set(str(0))

                tree_id, tree_quantities, tree_date = [], [], []

                all_items = reserve_view.get_children()

                for item in all_items:
                    item_details = reserve_view.item(item)

                    item_id = (((item_details['values'])[0]).split(":"))[0]
                    item_quantity = (item_details['values'])[1]
                    item_date = (item_details['values'])[2]

                    tree_id.append(item_id)
                    tree_quantities.append(item_quantity)
                    tree_date.append(item_date)

                    with main:
                        c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (item_id,))
                        get_item = c.fetchone()
                        get_item_quantity = get_item[3]

                        # update inventory when reservation is done
                        c.execute("""UPDATE Inventory SET Quantity = ? WHERE ItemID = ?""",
                            ((get_item_quantity - item_quantity), item_id))

                for i in range(len(tree_id)):
                    with main:
                        # update the Reservation log
                        c.execute("""INSERT INTO ReservationLog VALUES (?,?,?,?,?)""",
                                  (chosen_acc['student_id'], tree_id[i], tree_quantities[i], tree_date[i], "Pending"))

                        # fetching item from inventory analysis
                        c.execute("""SELECT * FROM InventoryAnalysis WHERE ItemID = ?""", (tree_id[i],))
                        data_result = c.fetchone()

                        new_reserved_item = data_result[2] + tree_quantities[i]
                        new_on_hand = data_result[3] - tree_quantities[i]
                        new_reserve_freq = data_result[5] + 1
                        print(new_on_hand)

                        # updating data analysis record after reservation
                        c.execute("""UPDATE InventoryAnalysis SET ReservedItem = ?, OnHand = ?, ReservingFrequency = ? 
                        WHERE ItemID = ?""", (new_reserved_item, new_on_hand, new_reserve_freq, tree_id[i], ))


                clear_treeview()

            delete_button = customtkinter.CTkButton(window,
                                                    text="Remove",
                                                    command=delete_item_func,
                                                    width=80,
                                                    height=30,
                                                    bg_color=white2,
                                                    fg_color="#880808")
            delete_button.place(relx=.67, rely=.8)

            reserve_addbutton = customtkinter.CTkButton(window,
                                                        text="Add Item",
                                                        command=reserve_add,
                                                        width=80,
                                                        height=30,
                                                        bg_color=white2,
                                                        fg_color=orange)
            reserve_addbutton.place(relx=.53, rely=.8)

            change_button = customtkinter.CTkButton(window,
                                                    text="Change",
                                                    command=change_item_func,
                                                    width=80,
                                                    height=30,
                                                    bg_color=white2,
                                                    fg_color="#228B22")
            change_button.place(relx=.81, rely=.8)

            user_note = customtkinter.CTkLabel(window,
                                               text="Note: To change or change, select an item in the list of the form.",
                                               bg_color=white2,
                                               font=("Helvetica", 11, "italic"))

            user_note.place(relx=.52, rely=.86)

            reserve_submit_button = customtkinter.CTkButton(window,
                                                            text="Reserve",
                                                            command=reserve_submit,
                                                            width=281,
                                                            height=30,
                                                            bg_color=white2,
                                                            fg_color=blue,
                                                            hover_color=orange)
            reserve_submit_button.place(relx=.08, rely=.88)

            widgets_holder.extend(
                [reserve_status, reserve_bg_label, reserve_form, reserve_addbutton, reserve_date_label, reserve_blue_bg,
                 reserve_addbutton, reserve_red_bg, reserve_name, reserve_view, reserve_quantity, reserve_quantity_label,
                 reserve_item, reserve_item_name, user_note, reserve_white_bg, change_button, delete_button, fill_out_label,
                 reserve_course, reserve_form_label, reserve_submit_button])

        # this is to check if there is unclaimed reserved item----------------------------------------------------------
        def check_expired_reservation():

            c.execute("""SELECT * FROM ReservationLog""")
            db_values = c.fetchall()  # fetching all item in reservation log to check

            date_today = (datetime.datetime.now()).strftime("%x")  # date today

            with main:
                for j in db_values:  # checking every item fetched
                    if j[3] < date_today and j[4] == "Pending":

                        # updating all the item with expired date
                        c.execute("""UPDATE ReservationLog SET Status = 'Expired' WHERE StudentID = ?""",
                                  (j[0],))
                        retrieved_expired = c.fetchone()

                        c.execute("""SELECT * FROM Inventory WHERE ItemID = ?""", (j[1],))
                        retrieved_item = c.fetchone()  # fetched item to update quantity

                        new_quantity = retrieved_item[3] + retrieved_expired[2]

                        c.execute("""UPDATE Inventory SET Quantity = ? WHERE ItemID = ?""",
                                  (new_quantity, retrieved_expired[1]))


        panel_bg = customtkinter.CTkLabel(window,
                                          width=10,
                                          height=10,
                                          image=bu_photo,
                                          text="")
        panel_bg.place(relx=0, rely=0)

        panel_color = customtkinter.CTkLabel(window,
                                             width=800,
                                             height=85,
                                             bg_color=blue,
                                             text="")
        panel_color.place(relx=0, rely=0)

        bg_photo_label = customtkinter.CTkLabel(window,
                                                image=bg_photo,
                                                width=1,
                                                height=1,
                                                text="",
                                                bg_color=blue)

        bg_photo_label.place(relx=0.01, rely=0.01)

        round_label = RoundClickableLabel(window,
                                          text=f"{chosen_acc['name'][0]}",
                                          radius=32,
                                          bg_color=white,
                                          text_color="black",
                                          callback=logout,
                                          border_color=white,
                                          background=blue,
                                          highlightbackground=blue)
        round_label.place(relx=0.9, rely=0.02)

        name_label = customtkinter.CTkLabel(window,
                                            text=f"{(chosen_acc['name'])}",
                                            width=250,
                                            height=10,
                                            anchor="e",
                                            justify="left",
                                            bg_color=blue,
                                            text_color=white,
                                            font=("Helvetica", 14, 'italic'))

        name_label.place(relx=0.58, rely=0.03)

        course_label = customtkinter.CTkLabel(window,
                                              text=f"{(chosen_acc['course']).upper()}",
                                              width=250,
                                              anchor="e",
                                              justify="left",
                                              bg_color=blue,
                                              text_color=white,
                                              font=("Helvetica", 14, 'italic'),
                                              height=4)

        course_label.place(relx=0.58, rely=0.06)

        info_button = customtkinter.CTkButton(window,
                                              text_color="white",
                                              text='Info',
                                              font=("Helvetica", 20, 'italic'),
                                              width=80,
                                              bg_color=blue,
                                              hover_color=orange,
                                              command=info_borrow,
                                              state='disabled',
                                              border_color=orange,
                                              border_width=2,
                                              text_color_disabled=white)

        info_button.place(relx=0.14, rely=0.06)

        borrow_button = customtkinter.CTkButton(window,
                                                text_color="white",
                                                text='Borrow',
                                                font=("Helvetica", 20, 'italic'),
                                                width=80,
                                                bg_color=blue,
                                                fg_color=blue,
                                                hover_color=orange,
                                                command=borrow_func,
                                                border_color=orange,
                                                border_width=2,
                                                text_color_disabled=white)

        borrow_button.place(relx=0.27, rely=0.06)

        return_button = customtkinter.CTkButton(window,
                                                text_color="white",
                                                text='Return',
                                                font=("Helvetica", 20, 'italic'),
                                                width=80,
                                                bg_color=blue,
                                                fg_color=blue,
                                                hover_color=orange,
                                                command=return_func,
                                                border_color=orange,
                                                border_width=2,
                                                text_color_disabled=white)

        return_button.place(relx=0.4, rely=0.06)

        reserve_button = customtkinter.CTkButton(window,
                                                 text_color="white",
                                                 text='Reserve',
                                                 font=("Helvetica", 20, 'italic'),
                                                 width=80,
                                                 bg_color=blue,
                                                 fg_color=blue,
                                                 hover_color=orange,
                                                 command=reserve_func,
                                                 border_color=orange,
                                                 border_width=2,
                                                 text_color_disabled=white)

        reserve_button.place(relx=0.53, rely=0.06)

        seperator1 = customtkinter.CTkLabel(window,
                                            text="",
                                            bg_color='gray',
                                            width=1,
                                            height=65)
        seperator1.place(relx=0.11, rely=0.02)

        seperator2 = customtkinter.CTkLabel(window,
                                            text="",
                                            bg_color='gray',
                                            width=1,
                                            height=52)
        seperator2.place(relx=0.68, rely=0.03)

        info_borrow()
        check_expired_reservation()

        window.mainloop()
