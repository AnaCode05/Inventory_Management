# Import Python libraries
import tkinter as tk
import psycopg2
from tkinter import messagebox
from tkinter import ttk

# Database connection details
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASSWORD = "npg_V0auDHb8LsQz"
DB_HOST = "ep-yellow-truth-a505909v-pooler.us-east-2.aws.neon.tech"


# Function to create the table if it does not exist
def create_table():
    try:
        # connect to DB
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER,
            password=DB_PASSWORD, 
            host=DB_HOST
        )
        cur = conn.cursor()
        
        # Create inventory table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS A3_inventory (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                quantity INTEGER    NOT NULL   DEFAULT 1    CHECK (quantity >= 0),
                price DECIMAL(10,2) 	NOT NULL    CHECK (price >= 0),
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create ledger table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS A3_ledger (
                id SERIAL PRIMARY KEY,
                operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('INSERT', 'UPDATE', 'DELETE')),
                item_name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                previous_quantity INTEGER,
                new_quantity INTEGER,
                previous_price DECIMAL(10,2),
                new_price DECIMAL(10,2),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("Database Error", f"Error creating tables: {str(e)}")

# Functions to open various INVENTORY CRUD operation windows
# CREATE
def open_add_window():
    global operation
    operation = "add"
    try:
        global add_window
        add_window = tk.Toplevel()
        add_window.title("Add Item to Inventory")
        add_window.geometry('400x400')

        # Create UI elements ---------------------

        # Item Name
        labelName = ttk.Label(add_window, text="Enter Item Name:")
        labelName.pack(pady=5)
        global entryItemName
        entryItemName = ttk.Entry(add_window, width=30)
        entryItemName.pack(pady=5)

        # Category
        labelCategory = ttk.Label(add_window, text="Enter Category:")
        labelCategory.pack(pady=5)
        global entryCategory
        entryCategory = ttk.Entry(add_window, width=30)
        entryCategory.pack(pady=5)

        # Quantity
        labelQuantity = ttk.Label(add_window, text="Enter Quantity:")
        labelQuantity.pack(pady=5)
        global entryQuantity
        entryQuantity = ttk.Entry(add_window, width=30)
        entryQuantity.pack(pady=5)

        # Price
        labelPrice = ttk.Label(add_window, text="Enter Price:")
        labelPrice.pack(pady=5)
        global entryPrice
        entryPrice = ttk.Entry(add_window, width=30)
        entryPrice.pack(pady=5)
            

        # Button to add the item
        button = ttk.Button(add_window, text="Add Item Record", command=add_record)
        button.pack(pady=10)

        # Cancel button
        button = ttk.Button(add_window, text="Clear", command=clear_entries)
        button.pack(pady=10)
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("UI Error", f"Error creating add window: {str(e)}")

 # Clear input fields
# UPDATE
def open_edit_window():
    global operation
    operation = "edit"
    try:
        global edit_window
        edit_window = tk.Toplevel()
        edit_window.title("Edit Item from Inventory")
        edit_window.geometry('400x400')

        # Create UI elements ---------------------

        # Item ID
        labelId = ttk.Label(edit_window, text="Edit Item ID:")
        labelId.pack(pady=5)
        global entryItemId_edit
        entryItemId_edit = ttk.Entry(edit_window, width=30)
        entryItemId_edit.pack(pady=5)

        # Item Name
        labelName = ttk.Label(edit_window, text="Edit Item Name:")
        labelName.pack(pady=5)
        global entryItemName
        entryItemName = ttk.Entry(edit_window, width=30)
        entryItemName.pack(pady=5)

        # Category
        labelCategory = ttk.Label(edit_window, text="Edit Category:")
        labelCategory.pack(pady=5)
        global entryCategory
        entryCategory = ttk.Entry(edit_window, width=30)
        entryCategory.pack(pady=5)

        # Quantity
        labelQuantity = ttk.Label(edit_window, text="Edit Quantity:")
        labelQuantity.pack(pady=5)
        global entryQuantity
        entryQuantity = ttk.Entry(edit_window, width=30)
        entryQuantity.pack(pady=5)

        # Price
        labelPrice = ttk.Label(edit_window, text="Edit Price:")
        labelPrice.pack(pady=5)
        global entryPrice
        entryPrice = ttk.Entry(edit_window, width=30)
        entryPrice.pack(pady=5)

        button = ttk.Button(edit_window, text="Update Item Record", command=edit_record)
        button.pack(pady=10)

        # Cancel button
        button = ttk.Button(edit_window, text="Clear", command=clear_entries)
        button.pack(pady=10)
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("UI Error", f"Error creating edit window: {str(e)}")   
# DELETE
def open_delete_window():
    global operation
    operation = "delete"
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER,
            password=DB_PASSWORD, 
            host=DB_HOST
        )
        cur = conn.cursor()

        global delete_window
        delete_window = tk.Toplevel()
        delete_window.title("Delete Item from Inventory")
        delete_window.geometry('300x200')

        # Create UI elements ---------------------

        # Item Name
        labelId = ttk.Label(delete_window, text="Enter Item ID:")
        labelId.pack(pady=5)
        global entryItemId
        entryItemId = ttk.Entry(delete_window, width=5)
        entryItemId.pack(pady=5)

        button = ttk.Button(delete_window, text="Delete Item Record", command=delete_record)
        button.pack(pady=10)

        # Cancel button
        button = ttk.Button(delete_window, text="Clear", command=clear_entries)
        button.pack(pady=10)

        conn.commit()
        cur.close()
        conn.close()
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("UI Error", f"Error creating delete window: {str(e)}")
# READ
def open_inventory_window():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER,
            password=DB_PASSWORD, 
            host=DB_HOST
        )
        cur = conn.cursor()

        bkg = "grey"
        inventory_window = tk.Toplevel(background=bkg)
        inventory_window.title("Inventory List")
        inventory_window.geometry('650x400')

        trv = ttk.Treeview(inventory_window, columns=(1,2,3,4,5,6), height=15, show="headings")
        
        trv.column(1, anchor="center", stretch="no", width=100)
        trv.column(2, anchor="center", stretch="no", width=100)
        trv.column(3, anchor="center", stretch="no", width=100)
        trv.column(4, anchor="center", stretch="no", width=100)
        trv.column(5, anchor="center", stretch="no", width=100)
        trv.column(6, anchor="center", stretch="no", width=150)

        trv.heading(1, text="Item ID")
        trv.heading(2, text="Item Name")
        trv.heading(3, text="Category")
        trv.heading(4, text="Quantity")
        trv.heading(5, text="Price")
        trv.heading(6, text="Date Added")

        trv.grid(row=0, column=0)
        #inventory_window.grid(row=0, column=0)

        # Execute query to read all items
        cur.execute('SELECT * FROM A3_inventory')
        items = cur.fetchall() # get all items from the DB
        # loop through all items & add to list
        for item in items:
            trv.insert('', 'end', value=(item[0], item[1], item[2], item[3], item[4], item[5]))

        conn.commit()
        cur.close()
        conn.close()
        
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("UI Error", f"Error creating inventory window: {str(e)}")   

# Ledger -- READ
def open_ledger_window():
    try:
        # Connect to DB
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER,
            password=DB_PASSWORD, 
            host=DB_HOST
        )
        cur = conn.cursor()

        # Set up window
        bkg = "grey"
        ledger_window = tk.Toplevel(background=bkg)
        ledger_window.title("Ledger (Record)")
        ledger_window.geometry('850x800')

        trv = ttk.Treeview(ledger_window, columns=(1,2,3,4,5,6,7,8), height=100, show="headings")
        
        trv.column(1, anchor="center", stretch="no", width=100)
        trv.column(2, anchor="center", stretch="no", width=100)
        trv.column(3, anchor="center", stretch="no", width=100)
        trv.column(4, anchor="center", stretch="no", width=100)
        trv.column(5, anchor="center", stretch="no", width=100)
        trv.column(6, anchor="center", stretch="no", width=100)
        trv.column(7, anchor="center", stretch="no", width=100)
        trv.column(8, anchor="center", stretch="no", width=150)

        trv.heading(1, text="Operation Type")
        trv.heading(2, text="Item Name")
        trv.heading(3, text="Category")
        trv.heading(4, text="Previous Quantity")
        trv.heading(5, text="New Quantity")
        trv.heading(6, text="Previous Price")
        trv.heading(7, text="New Price")
        trv.heading(8, text="Timestamp")

        trv.grid(row=0, column=0)

        # Execute query to read all transactions
        cur.execute('SELECT * FROM A3_ledger')
        transactions = cur.fetchall() # get all transactions from the DB
        # loop through all transactions & add to list by timestamp
        for transaction in transactions:
            trv.insert('', 'end', value=(transaction[1], transaction[2], transaction[3], transaction[4], transaction[5], transaction[6], transaction[7], transaction[8]))

        # Commit changes and close connections 
        conn.commit()
        cur.close()
        conn.close()
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("UI Error", f"Error creating ledger window: {str(e)}")

# Function to insert a record into the database
def add_record():
    itemName = entryItemName.get().strip()  # Get item name input and remove extra spaces
    category = entryCategory.get().strip()  # Get category input and remove extra spaces
    quantity = entryQuantity.get().strip()  # Get quantity input and remove extra spaces
    price = entryPrice.get().strip()  # Get price input and remove extra spaces

    if not itemName: # Ensure the inputs are not empty
        messagebox.showerror("Item Name Error", "Item name field cannot be empty!")
        return
    if not category:
        messagebox.showerror("Category Error", "Category field cannot be empty!")
        return
    if not quantity:
        messagebox.showerror("Quantity Error", "Quantity name field cannot be empty!")
        return
    if not price: 
        messagebox.showerror("Price Error", "Price field cannot be empty!")
        return
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()

        # Insert the item into the inventory table
        cur.execute("INSERT INTO A3_inventory (item_name,category,quantity,price) VALUES (%s,%s,%s,%s)", (itemName, category, int(quantity), float(price)))

        cur.execute("INSERT INTO A3_ledger (operation_type,item_name,category,previous_quantity,new_quantity,previous_price,new_price) VALUES (%s,%s,%s,%s,%s,%s,%s)", ("INSERT", itemName, category, int(quantity), int(quantity), float(price), float(price)))
        conn.commit()  # Save changes
        
        # Show output of successful add
        messagebox.showinfo("Success", f"Record '{itemName}' added successfully!")

        # close add window after successfully added item
        add_window.destroy() 

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
# Function to update a record of the database
def edit_record():
    itemId = entryItemId_edit.get().strip() # Get item ID input and remove extra spaces
    itemName = entryItemName.get().strip()  # Get item name input and remove extra spaces
    category = entryCategory.get().strip()  # Get category input and remove extra spaces
    quantity = entryQuantity.get().strip()  # Get quantity input and remove extra spaces
    price = entryPrice.get().strip()  # Get price input and remove extra spaces

    if not itemId: # Ensure the inputs are not empty
        messagebox.showerror("Item ID Error", "Item ID field cannot be empty!")
        return
    if not itemName:
        messagebox.showerror("Item Name Error", "Item name field cannot be empty!")
        return
    if not category:
        messagebox.showerror("Category Error", "Category field cannot be empty!")
        return
    if not quantity:
        messagebox.showerror("Quantity Error", "Quantity name field cannot be empty!")
        return
    if not price: 
        messagebox.showerror("Price Error", "Price field cannot be empty!")
        return
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()
        
        # Get the selected item information before updating
        cur.execute("SELECT * FROM A3_inventory WHERE id=" + itemId)
        item_to_edit = cur.fetchone()
        print(item_to_edit)
        print(item_to_edit[0])
        print(itemId)

        # UPDATE the item in the 'inventory' table
        
        cur.execute("UPDATE A3_inventory SET item_name= %s, category=%s, quantity=%s, price=%s WHERE id=%s", (itemName, category, quantity, price, itemId))
        print("Item updated")

        # Add the record of update to the ledger
        cur.execute("INSERT INTO A3_ledger (operation_type,item_name,category,previous_quantity,new_quantity,previous_price,new_price) VALUES (%s,%s,%s,%s,%s,%s,%s)", ("UPDATE", itemName, category, item_to_edit[3], quantity, item_to_edit[4], price))
        print("Update transaction added to ledger")

        conn.commit()

        # Show output of successful update
        messagebox.showinfo("Success", f"Record '{itemName}' updated successfully!")

        # close edit window after successfully updated item
        edit_window.destroy()

        cur.close()
        conn.close()
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("Database Error", f"Error updating item: {str(e)}")
        print(str(e))
# Function to delete a record of the database
def delete_record():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER,
            password=DB_PASSWORD, 
            host=DB_HOST
        )
        cur = conn.cursor()

        itemId = entryItemId.get().strip()
        if not itemId: # Ensure the input is not empty
            messagebox.showerror("Item ID Error", "Item ID field cannot be empty!")
            return
        
        # Delete confirmation message box
        confirmation = messagebox.askquestion('Confirm Delete', 'Are you sure you want to delete item with ID '+itemId+'?')
        # Exit delete function if answer is 'no'
        if confirmation == "no":
            return
        # Keep going if answer is 'yes'

        # Get the selected item information before deleting
        cur.execute("SELECT * FROM A3_inventory WHERE id=" + itemId)
        item_to_delete = cur.fetchone()
        print(item_to_delete)
        print(item_to_delete[0])
        print(itemId)

        # Delete the item from the 'inventory' table
        delete_query = "DELETE FROM A3_inventory WHERE id=" + itemId
        cur.execute(delete_query)

        # Add the record of deletion to the ledger
        cur.execute("INSERT INTO A3_ledger (operation_type,item_name,category,previous_quantity,new_quantity,previous_price,new_price) VALUES (%s,%s,%s,%s,%s,%s,%s)", ("DELETE", item_to_delete[1], item_to_delete[2], item_to_delete[3], item_to_delete[3], item_to_delete[4], item_to_delete[4]))

        conn.commit()

        # Show output of successful delete
        messagebox.showinfo("Success", f"Record '{item_to_delete[1]}' deleted successfully!")

        # close delete window after successfully deleted item
        delete_window.destroy() 

        cur.close()
        conn.close()
    # catch any exceptions
    except Exception as e:
        messagebox.showerror("Database Error", f"Error deleting item: {str(e)}")
        print(str(e))

# Function to clear all input fields
def clear_entries():
    if (operation == "add"):
        entryItemName.delete(0, tk.END)
        entryCategory.delete(0, tk.END)
        entryQuantity.delete(0, tk.END)
        entryPrice.delete(0, tk.END)
    elif (operation == "edit"):
        entryItemId_edit.delete(0, tk.END)
        entryItemName.delete(0, tk.END)
        entryCategory.delete(0, tk.END)
        entryQuantity.delete(0, tk.END)
        entryPrice.delete(0, tk.END)
    else:
        entryItemId.delete(0, tk.END)

# Create the main Tkinter UI
root = tk.Tk()
root.title("Choose an action")
root.geometry("400x400")
root.configure(background="lavender")

# Run table creation on startup
create_table()
# Create UI elements -------------

buttonTheme = "lightblue"

button = tk.Button(root, text="Add Item Window", command=open_add_window, background=buttonTheme)
button.pack(pady=10)

button = tk.Button(root, text="Edit Item Window", command=open_edit_window, background=buttonTheme)
button.pack(pady=10)

button = tk.Button(root, text="Delete Item Window", command=open_delete_window, background=buttonTheme)
button.pack(pady=10)

button = tk.Button(root, text="Inventory Window", command=open_inventory_window, background=buttonTheme)
button.pack(pady=10)

button = tk.Button(root, text="Ledger Window", command=open_ledger_window, background=buttonTheme)
button.pack(pady=10)

button = tk.Button(root, text="Exit", command=root.destroy, background="darkred", foreground="white")
button.pack(pady=10, padx=10)

# Run the Tkinter event loop
root.mainloop()