import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
import sqlite3
import csv
from sqlite3 import connect
from tkinter import Canvas
from contextlib import closing
from tkinter.ttk import Entry

#http://paletton.com/#uid=51-0O0kjNif5hOiapt5u38HGb31

root_window = Tk()
root_window.geometry("640x490")
root_window.title("Tilly_Tek Inventory Logg-r")
root_window.resizable(False, False)

ADD_REMOVE = [
    "Select",
    "Add",
    "Remove"
]

SORT_OPTIONS = [
    "Select",
    "Show Log",
    "In Stock"
]

ITEM_TYPE = []

ITEM_SUBTYPE = []

def create_item_list():
    conn = sqlite3.connect("my_database.sqlite")
    c = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS item_list(PRIMARY_ID INTEGER PRIMARY KEY, ITEM_TYPE CHAR(20), ITEM_NAME CHAR(20),
QUANTITY INTEGER(3) DEFAULT 0,
TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
    c.execute(query)
    conn.commit()
    conn.close()

def create_main_table():
    conn = sqlite3.connect("my_database.sqlite")
    c = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS main_table(PRIMARY_ID INTEGER PRIMARY KEY, ITEM_TYPE CHAR(20), ITEM_NAME CHAR(20),
QUANTITY INTEGER(3) DEFAULT 0, TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''
    c.execute(query)
    conn.commit()
    conn.close()


def fetch_database():
    text_field.configure(state=NORMAL)
    text_field.delete(1.0, END)
    conn = sqlite3.connect("my_database.sqlite")
    conn.row_factory = sqlite3.Row
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM main_table'''
        c.execute(query,)
        my_database = c.fetchall()
    if my_database is not None:
        for main_table in my_database:
            id_string = (str(main_table["PRIMARY_ID"]))
            id_filler = len(id_string)
            namespace_filler = 30 - (len(main_table["ITEM_NAME"]))
            quantity_filler = str(main_table["QUANTITY"])
            if quantity_filler[0] != "-":
                quantity_filler = "|" + quantity_filler
            quantity_num_filler = 5 - len(quantity_filler)
            formatted_date = (main_table["TIMESTAMP"].split(" "))
            text_field.insert(1.0, str(main_table["PRIMARY_ID"]) + (" " * (5 - id_filler)) + "|"
                              + main_table["ITEM_NAME"] + ("_" * namespace_filler) + quantity_filler +
                              (" " * quantity_num_filler) + "|" + formatted_date[0] + "\n")
    text_field.configure(state=DISABLED)

def display_item_list():
    text_field.configure(state=NORMAL)
    text_field.delete(1.0, END)
    conn = sqlite3.connect("my_database.sqlite")
    conn.row_factory = sqlite3.Row
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM item_list'''
        c.execute(query, ())
        my_database = c.fetchall()
    if my_database is not None:
        for main_table in my_database:
            id_string = (str(main_table["PRIMARY_ID"]))
            id_filler = len(id_string)
            namespace_filler = 30 - (len(main_table["ITEM_NAME"]))
            quantity_filler = str(main_table["QUANTITY"])
            if quantity_filler[0] != "-":
                quantity_filler = "|" + quantity_filler
            quantity_num_filler = 5 - len(quantity_filler)
            formatted_date = (main_table["TIMESTAMP"].split(" "))
            text_field.insert(1.0, str(main_table["PRIMARY_ID"]) + (" " * (5 - id_filler)) + "|"
                              + main_table["ITEM_NAME"] + ("_" * namespace_filler) + quantity_filler +
                              (" " * quantity_num_filler) + "|" + formatted_date[0] + "\n")
    text_field.configure(state=DISABLED)

def sort_method():
    x = sort_menu.get()
    if x == 'Show Log':
        fetch_database()
    elif x == 'In Stock':
        display_item_list()

def get_quantity(ITEM_NAME):
    conn = sqlite3.connect("my_database.sqlite")
    conn.row_factory = sqlite3.Row
    with closing(conn.cursor()) as c:
        query = '''SELECT QUANTITY FROM item_list WHERE ITEM_NAME = (?)'''
        c.execute(query, (ITEM_NAME,))
        my_database = c.fetchall()
        if my_database is not None:
            for item_list in my_database:
                item_quantity = item_list["QUANTITY"]
    return item_quantity

        
def enter_into_database():
    text_field.configure(state=NORMAL)
    add_or_remove_value = add_or_remove.get()
    ITEM_NAME = str(item_subtype_name.get())
    x = get_quantity(ITEM_NAME)
    if add_or_remove_value == "Remove":
        QUANTITY = int(enter_quantity.get()) * -1
    else:
        QUANTITY = int(enter_quantity.get())
    ITEM_TYPE = str(item_name.get())
    UPDATED_QUANTITY = QUANTITY + x
    conn = sqlite3.connect("my_database.sqlite")
    with closing(conn.cursor()) as c:
        sql = '''INSERT INTO main_table (ITEM_NAME, QUANTITY) VALUES (?, ?)'''
        c.execute(sql, (ITEM_NAME, QUANTITY))
        sql_2 = '''UPDATE item_list SET QUANTITY = (?) WHERE ITEM_NAME = (?)'''
        c.execute(sql_2, (UPDATED_QUANTITY, ITEM_NAME))
        conn.commit()
    quantity.set("")
    item_name.set("Select")
    item_subtype_name.set("Select")
    fetch_database()
    text_field.configure(state=DISABLED)


def change_subtype(item_name):

    ITEM_SUBTYPE = []
    enter_subtype = ttk.OptionMenu(root_window, item_subtype_name, *ITEM_SUBTYPE)
    conn = sqlite3.connect("my_database.sqlite")
    conn.row_factory = sqlite3.Row
    ITEM_SUBTYPE.append('Select')
    with closing(conn.cursor()) as c:
        query = '''SELECT ITEM_NAME FROM item_list WHERE ITEM_TYPE = (?)'''
        c.execute(query, (item_name,))
        my_database = c.fetchall()
    if my_database is not None:
        for item_list in my_database:
            count = ITEM_SUBTYPE.count(item_list["ITEM_NAME"])
            if item_list["ITEM_NAME"] != '' and count < 1:
                ITEM_SUBTYPE.append(item_list["ITEM_NAME"])
    enter_subtype = ttk.OptionMenu(root_window, item_subtype_name, *ITEM_SUBTYPE)
    enter_subtype.place(x=140, y=335)


def spot_duplicate_entries(item_subtype):
    ITEM_COUNT = []
    conn = sqlite3.connect("my_database.sqlite")
    conn.row_factory = sqlite3.Row
    with closing(conn.cursor()) as c:
        query = '''SELECT * FROM item_list where ITEM_NAME = (?)'''
        c.execute(query, (item_subtype,))
        my_database = c.fetchall()
    if my_database is not None:
        for item_list in my_database:
            ITEM_COUNT.append(item_list["ITEM_NAME"])
    return len(ITEM_COUNT)

    
def update_inventory_list():
    text_field.configure(state=NORMAL)
    text_field.delete(1.0, END)
    item_type_entry = add_remove_type.get()
    item_type_pulldown = select_item_type.get()
    item_subtype = add_remove_name.get()
    x = spot_duplicate_entries(item_subtype)
    add_remove =  add_or_remove_item.get()
    if x > 0 and add_remove == "Add":
        text_field.insert(1.0, "This item is already listed in the database.")
    else:
        if item_type_entry == "" and item_type_pulldown == "Select":
            text_field.insert(1.0, 'Please specify an item type')
            select_item_type.set('Select') 
        elif item_subtype == "" and add_remove == "Add":
            text_field.insert(1.0, 'Please include an item to list for this type')
        else:
            if add_remove == "Add":
                conn = sqlite3.connect("my_database.sqlite")
                with closing(conn.cursor()) as c:
                    query = '''INSERT INTO item_list (item_type, item_name) VALUES (?, ?)'''
                    if item_type_entry != "":
                        c.execute(query, (item_type_entry, item_subtype,))
                    else:
                        c.execute(query, (item_type_pulldown, item_subtype,))
                    conn.commit()
            elif add_remove == "Remove":
                conn = sqlite3.connect("my_database.sqlite")
                with closing(conn.cursor()) as c:
                    if item_subtype == "":
                        query = '''DELETE FROM item_list WHERE ITEM_TYPE = (?)'''
                        c.execute(query, (item_type_entry,))
                    else:
                        query = '''DELETE FROM item_list WHERE ITEM_TYPE = (?) AND ITEM_NAME = (?)'''                        
                        c.execute(query, (item_type_pulldown, item_subtype,))
                    conn.commit()
        select_item_type.set('')   
        add_remove_type.set('')
        add_remove_name.set('')
        item_name.set('')
        item_subtype_name.set('Select')
        item_type_populate()

def delete_from_database():
    item_id = delete_value.get()
    conn = sqlite3.connect("my_database.sqlite")
    with closing(conn.cursor()) as c:
        query = '''DELETE FROM main_table WHERE PRIMARY_ID = (?)'''
        c.execute(query, (item_id,))
        conn.commit()
    delete_value.set('')
    fetch_database()
    

def item_type_populate():
    ITEM_TYPE = ['Select']
    try:
        conn = sqlite3.connect("my_database.sqlite")
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as c:
            query = '''SELECT ITEM_TYPE FROM item_list ORDER BY ITEM_TYPE ASC'''
            c.execute(query, ())
            my_database = c.fetchall()
        if my_database is not None:
            for item_list in my_database:
                count = ITEM_TYPE.count(item_list["ITEM_TYPE"])
                if count < 1:
                    ITEM_TYPE.append(item_list["ITEM_TYPE"])
    except sqlite3.OperationalError:
        print("This doesn't work")
    enter_name = ttk.OptionMenu(root_window, item_name, *ITEM_TYPE, command=change_subtype)
    enter_name.place(x=140, y=300)
    select_item_pulldown = ttk.OptionMenu(root_window, select_item_type, *ITEM_TYPE)
    select_item_pulldown.place(x=378, y=300)
    

canvas = Canvas(root_window, width="640", height="490", background="#180E00")
canvas.create_text(487, 38, fill="#2C4004", font="Georgia 26 bold italic", text="__________|")
canvas.create_text(321, 37, fill="#6A8734", font="Georgia 26 bold italic", text="Inventory Logg-r __________|")
canvas.create_text(181, 36, fill="#EAF8CF", font="Georgia 26 bold italic", text="Inventory Logg-r")
canvas.create_text(61, 246, fill="#6A8734", font="Georgia 14 bold", text="ID")
canvas.create_text(60, 245, fill="#EAF8CF", font="Georgia 14 bold", text="ID")
canvas.create_text(259, 246, fill="#6A8734", font="Georgia 14 bold", text="Item Desc.")
canvas.create_text(258, 245, fill="#EAF8CF", font="Georgia 14 bold", text="Item Desc.")
canvas.create_text(218, 279, fill="#452B04", font="Georgia 14", text="Update Inventory")
canvas.create_text(217, 278, fill="#FFEED5", font="Georgia 14", text="Update Inventory")
canvas.create_text(531, 246, fill="#6A8734", font="Georgia 14 bold", text="Date")
canvas.create_text(530, 245, fill="#EAF8CF", font="Georgia 14 bold", text="Date")
canvas.create_text(73, 279, fill="#452B04", font="Georgia 14", text="Show Items")
canvas.create_text(72, 278, fill="#FFEED5",  font="Georgia 14", text="Show Items")
canvas.create_text(450, 246, fill="#6A8734", font="Georgia 14 bold", text="QTY")
canvas.create_text(449, 245, fill="#EAF8CF", font="Georgia 14 bold", text="QTY")
canvas.create_text(161, 416, fill="#452B04", font="Georgia 14", text="QTY:")
canvas.create_text(160, 415, fill="#FFEED5", font="Georgia 14", text="QTY:")
canvas.create_text(418, 279, fill="#452B04", font="Georgia 14", text="Add / Remove Items")
canvas.create_text(417, 278, fill="#FFEED5", font="Georgia 14", text="Add / Remove Items")
canvas.create_text(341, 309, fill="#452B04", font="Georgia 14", text="Type:")
canvas.create_text(340, 308, fill="#FFEED5", font="Georgia 14", text="Type:")
canvas.create_text(344, 344, fill="#452B04", font="Georgia 9", text="(Add New)")
canvas.create_text(343, 343, fill="#FFEED5", font="Georgia 9", text="(Add New)")
canvas.create_text(346, 379, fill="#452B04", font="Georgia 14", text="Name:")
canvas.create_text(345, 378, fill="#FFEED5", font="Georgia 14", text="Name:")
canvas.create_rectangle(128, 264, 131, 472, fill="#452B04")
canvas.create_rectangle(126, 262, 129, 470, fill="#916D37")
canvas.create_rectangle(306, 264, 309, 472, fill="#452B04")
canvas.create_rectangle(304, 262, 307, 470, fill="#916D37")
canvas.create_rectangle(525, 264, 528, 472, fill="#452B04")
canvas.create_rectangle(523, 262, 526, 470, fill="#916D37")
canvas.create_rectangle(28, 262, 616, 265, fill="#452B04")
canvas.create_rectangle(26, 260, 614, 263, fill="#916D37")
canvas.pack()
create_item_list()
create_main_table()
text_field = Text(root_window, font=("courier", 14, "bold"), height=7, width=52)
text_field.place(x=29, y=73)
sort_menu = tk.StringVar()
sort_menu.set("Select")
sort_widget = ttk.OptionMenu(root_window, sort_menu, *SORT_OPTIONS)
sort_widget.place(x=30, y=300)
submit = Button(root_window, text="Show List", font=("Georgia", 8, "bold"), fg="#181500", bg="#FFFAD5", command=sort_method).place(x=32, y=445)
item_name = tk.StringVar()
item_name.set("Select")
select_item_type = tk.StringVar()
select_item_type.set("Select")
item_subtype_name = tk.StringVar()
item_subtype_name.set("Select")
item_type_populate()
enter_subtype = ttk.OptionMenu(root_window, item_subtype_name, *ITEM_SUBTYPE)
enter_subtype.place(x=140, y=335)
add_or_remove = tk.StringVar()
add_or_remove.set(ADD_REMOVE[0])
update_inventory = ttk.OptionMenu(root_window, add_or_remove, *ADD_REMOVE)
update_inventory.place(x=140, y=370)
quantity = tk.StringVar()
enter_quantity = ttk.Entry(root_window, width=3, textvariable=quantity)
enter_quantity.place(x=190, y=405)
enter_button = Button(text="Submit Update", font=("Georgia", 8, "bold"), fg="#181500", bg="#FFFAD5", command=enter_into_database)
enter_button.place(x=162, y=445)
add_remove_type = tk.StringVar()
item_type_update = ttk.Entry(root_window, width=20, textvariable=add_remove_type).place(x=378, y=335)
add_remove_name = tk.StringVar()
item_name_update = ttk.Entry(root_window, width=20, textvariable=add_remove_name).place(x=378, y=370)
add_or_remove_item = tk.StringVar()
add_or_remove_item.set(ADD_REMOVE[0])
update_item_list = ttk.OptionMenu(root_window, add_or_remove_item, *ADD_REMOVE)
update_item_list.place(x=378, y=405)
item_list_button = Button(root_window, text="Update Item List", font=("Georgia", 8, "bold"), fg="#181500", bg="#FFFAD5", command=update_inventory_list)
item_list_button.place(x=357, y=445)
root_window.mainloop()
