#Checks if the customers.xlsx file exists.
#If it doesn't exist then the program creates one.
#Reads the existing customer data from the file.
#Updates excel file with new information provided. 
import pandas as pd
import os

def update_customer_sheet(customer):
    file_path = 'data/customers.xlsx'

    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Customer ID", "Name", "Email"])
        df.to_excel(file_path, index=False, engine="openpyxl")

    try:
        existing_df = pd.read_excel(file_path, engine="openpyxl")
    except Exception:
        existing_df = pd.DataFrame(columns=["Customer ID", "Name", "Email"])

    new_data = pd.DataFrame([{
        'Customer ID': customer.customer_id,
        'Name': customer.name,
        'Email': customer.email
    }])

    updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    updated_df.to_excel(file_path, index=False, engine="openpyxl")


#Checks if inventory.xlsx exists, otherwise creates it.
#Reads current inventory data from Excel.
#Adds a new inventory item with Item Name, Quantity, and Price.
#Saves the updated inventory to Excel.
def update_inventory_sheet(item_name, quantity, price):
    file_path = 'data/inventory.xlsx'

    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Item Name", "Quantity", "Price"])
        df.to_excel(file_path, index=False, engine="openpyxl")

    try:
        existing_df = pd.read_excel(file_path, engine="openpyxl")
    except Exception:
        existing_df = pd.DataFrame(columns=["Item Name", "Quantity", "Price"])

    new_data = pd.DataFrame([{
        'Item Name': item_name,
        'Quantity': quantity,
        'Price': price
    }])

    updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    updated_df.to_excel(file_path, index=False, engine="openpyxl")


# Checks if orders.xlsx exists, otherwise creates it.
#Reads existing order data from Excel.
#Calculates the Total Price of the order using inventory.get_price(item).
#Formats the order details (items and quantities) as a string.
#Appends the order to the existing data.
#Saves the updated data back to Excel.
def update_order_sheet(order, item_quantities, inventory):
    file_path = 'data/orders.xlsx'

    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Order ID", "Customer Name", "Items", "Total Price"])
        df.to_excel(file_path, index=False, engine="openpyxl")

    try:
        existing_df = pd.read_excel(file_path, engine="openpyxl")
    except Exception:
        existing_df = pd.DataFrame(columns=["Order ID", "Customer Name", "Items", "Total Price"])

    total_price = sum(
        inventory.get_price(item) * quantity
        for item, quantity in item_quantities.items()
    )

    new_data = pd.DataFrame([{
        'Order ID': order.order_id,
        'Customer Name': order.customer.name,
        'Items': ', '.join(f"{item} x{qty}" for item, qty in item_quantities.items()),
        'Total Price': total_price
    }])

    updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    updated_df.to_excel(file_path, index=False, engine="openpyxl")
