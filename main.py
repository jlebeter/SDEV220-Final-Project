#tkinter is used tp create a GUI 
#messagebox displays a popup message
#Inventory, Order, Customer, and System create custom classes
#excel_utils stores everything in an excel file
#os checks the existece of a file

import tkinter as tk
from tkinter import messagebox
from inventory import Inventory
from order import Order
from customer import Customer
from system import System
from excel_utils import update_customer_sheet, update_inventory_sheet, update_order_sheet
import os

#inventory stores item names, quantities, and prices
#system manages customers and orders

inventory = Inventory()
system = System()

#Creates the main tkinter window
#Sets the window title and size and defines the font size for GUI

root = tk.Tk()
root.title("Order Management System")
root.geometry("1200x800")
LARGE_FONT = ("Arial", 30)
SMALL_FONT = ("Arial", 10)

#create_label() creates a label with a specified font
#create_entry() creates a text input field
#create_button() creates a button with a specific function and color

def create_label(window, text, font=LARGE_FONT):
    tk.Label(window, text=text, font=font).pack()

def create_entry(window, font=LARGE_FONT):
    entry = tk.Entry(window, font=font)
    entry.pack()
    return entry

def create_button(window, text, command, bg_color="blue"):
    tk.Button(window, text=text, font=LARGE_FONT, command=command, bg=bg_color, fg="white", width=30, height=2).pack()

def load_customers_from_excel():
    file_path = "data/customers.xlsx"

    if not os.path.exists(file_path):
        return 

    try:
        df = pd.read_excel(file_path, engine="openpyxl")

        for _, row in df.iterrows():
            customer = Customer(int(row["Customer ID"]), row["Name"], row["Email"])
            system.add_customer(customer) 
        print("Customers loaded:", system.customers)
    except Exception as e:
        print(f"Error loading customers: {str(e)}")

#Creates a new window for customer registration.
#Checks if the customer ID already exists.
#Creates a Customer object and saves it in the system.
#Saves customer data to Excel

def add_customer():
    def submit_customer():
        try:
            customer_id = int(customer_id_entry.get())
            name = name_entry.get()
            email = email_entry.get()

            if customer_id in system.customers:
                messagebox.showerror("Error", "Customer ID already exists!")
                return

            new_customer = Customer(customer_id, name, email)
            system.add_customer(new_customer)
            update_customer_sheet(new_customer)

            print("Customers in system:", system.customers)

            messagebox.showinfo("Success", f"Customer {name} added successfully!")
            add_customer_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid Customer ID.")


    add_customer_window = tk.Toplevel(root)
    add_customer_window.title("Add Customer")

    create_label(add_customer_window, "Customer ID:")
    customer_id_entry = create_entry(add_customer_window)

    create_label(add_customer_window, "Name:")
    name_entry = create_entry(add_customer_window)

    create_label(add_customer_window, "Email:")
    email_entry = create_entry(add_customer_window)

    create_button(add_customer_window, "Submit", submit_customer, "green")

#Captures new inventory items.
#Validates input for quantity and price.
#Adds items to the inventory object and Excel file.

def add_inventory():
    def submit_inventory():
        try:
            item_name = item_name_entry.get()
            quantity = int(quantity_entry.get())
            price = float(price_entry.get())

            inventory.add_item(item_name, quantity, price)
            update_inventory_sheet(item_name, quantity, price)

            messagebox.showinfo("Success", f"Item '{item_name}' added successfully!")
            add_inventory_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter a valid number for quantity and price.")

    add_inventory_window = tk.Toplevel(root)
    add_inventory_window.title("Add Inventory Item")

    create_label(add_inventory_window, "Item Name:")
    item_name_entry = create_entry(add_inventory_window)

    create_label(add_inventory_window, "Quantity:")
    quantity_entry = create_entry(add_inventory_window)

    create_label(add_inventory_window, "Price per Unit:")
    price_entry = create_entry(add_inventory_window)

    create_button(add_inventory_window, "Submit", submit_inventory, "green")

#Verifies the customer exists.
#Ensures ordered items exist and have sufficient stock.
#Calculates the total order price.
#Removes purchased items from the inventory.
#Saves the order to Excel.

def place_order():
    def submit_order():
        try:
            customer_id = int(customer_id_entry.get())

            print("Available customers:", system.customers)

            if customer_id not in system.customers:
                messagebox.showerror("Error", "Customer not found!")
                return

            customer = system.customers[customer_id]
            items = items_entry.get().split(",")
            items = [item.strip() for item in items]

            item_quantities = {}
            total_price = 0

            for item in items:
                if item not in inventory.get_inventory():
                    messagebox.showerror("Error", f"Item '{item}' is not available.")
                    return

                quantity = int(quantity_entries[item].get())

                if inventory.items[item] < quantity:
                    messagebox.showerror("Error", f"Insufficient stock for {item}. Available: {inventory.items[item]}")
                    return

                item_quantities[item] = quantity
                item_price = inventory.prices.get(item, 0)
                total_price += item_price * quantity

            order_id = max(system.orders.keys(), default=100) + 1
            order = Order(order_id, customer, item_quantities)
            system.place_order(order)

            for item, quantity in item_quantities.items():
                inventory.remove_item(item, quantity)

            update_order_sheet(order, item_quantities, inventory)

            messagebox.showinfo("Success", f"Order placed successfully!\nTotal Price: ${total_price:.2f}")
            place_order_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter correct values.")

    place_order_window = tk.Toplevel(root)
    place_order_window.title("Place Order")

    create_label(place_order_window, "Customer ID:", SMALL_FONT)
    customer_id_entry = create_entry(place_order_window, SMALL_FONT)

    create_label(place_order_window, "Enter items (comma-separated):", SMALL_FONT)
    items_entry = create_entry(place_order_window, SMALL_FONT)

    quantity_entries = {}
    for item in inventory.get_inventory():
        create_label(place_order_window, f"{item}:", SMALL_FONT)
        quantity_entries[item] = create_entry(place_order_window, SMALL_FONT)

    create_button(place_order_window, "Submit", submit_order, "green")

import pandas as pd

#Displays inventory items with their quantities and prices.

def show_inventory():
    inventory_window = tk.Toplevel(root)
    inventory_window.title("Inventory List")

    file_path = "data/inventory.xlsx"
    
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Inventory file not found!")
        return
    
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        inventory_list = df.to_string(index=False)
    except Exception as e:
        inventory_list = f"Error loading inventory: {str(e)}"

    create_label(inventory_window, inventory_list, SMALL_FONT)

#Displays all customers along with their orders.

def show_customers():
    customers_window = tk.Toplevel(root)
    customers_window.title("Customer List")

    file_path = "data/customers.xlsx"
    
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Customer file not found!")
        return
    
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        customer_list = df.to_string(index=False)
    except Exception as e:
        customer_list = f"Error loading customers: {str(e)}"

    create_label(customers_window, customer_list, SMALL_FONT)

#Displays all the orders placed.

def show_orders():
    orders_window = tk.Toplevel(root)
    orders_window.title("Order List")

    file_path = "data/orders.xlsx"
    
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Order file not found!")
        return
    
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        order_list = df.to_string(index=False)
    except Exception as e:
        order_list = f"Error loading orders: {str(e)}"

    create_label(orders_window, order_list, SMALL_FONT)

#Saves all data before exiting.
#Handles exceptions in case of errors.

def exit_program():
    try:
        for customer in system.customers.values():
            update_customer_sheet(customer)

        for item, quantity in inventory.get_inventory().items():
            update_inventory_sheet(item, quantity, inventory.get_price(item))

        for order in system.orders.values():
            update_order_sheet(order, order.items, inventory)

        messagebox.showinfo("Success", "All data saved successfully!")
        root.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")

#Creates buttons for each function.
#Starts the Tkinter main event loop.

create_button(root, "Place Order", place_order, "green")
create_button(root, "Add Customer", add_customer, "blue")
create_button(root, "Add Inventory", add_inventory, "blue")
create_button(root, "View Inventory", show_inventory, "orange")
create_button(root, "View Customers", show_customers, "orange")
create_button(root, "View Orders", show_orders, "orange")
create_button(root, "Exit", exit_program, "red")

root.mainloop()