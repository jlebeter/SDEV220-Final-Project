# Author
- Jack Lebeter

# Course
- SDEV220 Final Project

# Date
- March 2025

# Order Management System

This is a Python-based Order Management System with a graphical user interface (GUI) built using tkinter. It allows users to manage customers, inventory, and orders, and saves data in Excel files.

# Features
- Place Orders: Allows user to place and process orders.
- Add Customers: Allows user to create new customer profiles that include customer ID, full name, and email address.
- Add Inventory: Allows user to add inventory and include details such as name, quantity, and price per unit.
- View Customers: Allows the user to view all the customers' profiles with the appropriate information.
- View Inventory: Add and track inventory items.
- View Orders: Allows user to view all the orders placed with the appropriate information.
- Exit: Saves information input from user to Excel files.

# Installation
To set up the project, create a virtual environment and install dependencies:
- pandas
- python
- openpyxl
- tkinter

# Usage
- Run the main script to start the application

# File Structure
data/ #Excel files for storage 
main.py #Main GUI application
customer.py #Customer class
inventory.py #Inventory class
order.py #Order class
system.py #System class to manage customers and orders
excel_utils.py #Functions to update Excel sheets
requirements.txt #Required dependencies
README.md # Project documentation

# Testing
1. Create virtual environment.
2. Install the required dependencies.
3. Run program.
4. Click the 'Add Inventory' button to add new items to the inventory.
4. A window will appear and prompt the user to include the name, quantity added, and the price per unit for the item.
5. Click 'Submit' to save the information.
6. Click the 'View Inventory' button and a window will pop up.
7. Check the text in the window for new items to ensure that they were added to the appropriate Excel file.
8. Click the 'Add Customer' button and a window will open.
9. The window will prompt the user to input information including customer ID, name, and email address.
10. Click the 'Submit' button to save the information that was input.
11. Click the 'View Customers' button and a window will open.
12. Check the text in the window to ensure that the customer was added to the appropriate Excel file.
13. Click the 'Place Order' button and a window will open.
14. The window will prompt the user to input the customer's ID number.
15. The window will also prompt the user to input the items the customer is ordering.
16. The window then prompts the user to input the quantity of each item that is purchased.
17. Click the 'Submit' button to save the order.
18. The program will output a message that states the customer's name and the total price of their order.
19. Click the 'View Orders' button to ensure that the order was saved to the appropriate Excel file.
20. Click the 'Exit' button when finished to save all of the information to their resoected Excel sheet. 