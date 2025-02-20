import pandas as pd
from system import Inventory, Customer, Order, System


def update_customer_sheet(customer):
    df = pd.DataFrame([{
        'Customer ID': customer.customer_id,
        'Name': customer.name,
        'Email': customer.email
    }])
    df.to_excel('customers.xlsx', mode='a', index=False, header=not pd.io.common.file_exists('customers.xlsx'))


def update_inventory_sheet(item_name, quantity, price):
    df = pd.DataFrame([{
        'Item Name': item_name,
        'Quantity': quantity,
        'Price': price
    }])
    df.to_excel('inventory.xlsx', mode='a', index=False, header=not pd.io.common.file_exists('inventory.xlsx'))


def update_order_sheet(order, item_quantities, inventory):
    total_price = sum(
        inventory.prices.get(item, 0) * quantity
        for item, quantity in item_quantities.items()
    )

    df = pd.DataFrame([{
        'Order ID': order.order_id,
        'Customer Name': order.customer.name,
        'Items': ', '.join(f"{item} x{qty}" for item, qty in item_quantities.items()),
        'Total Price': total_price
    }])
    df.to_excel('orders.xlsx', mode='a', index=False, header=not pd.io.common.file_exists('orders.xlsx'))


def main():
    inventory = Inventory()
    system = System()

    inventory.prices = {}

    while True:
        print("\nWelcome to the Order System!")
        print("1. New Order")
        print("2. Inventory List")
        print("3. Order List")
        print("4. Customer List")
        print("5. Add Inventory Item")
        print("6. Add Customer")
        print("7. Exit")

        choice = input("Please choose an option (1-7): ")

        if choice == '1':
            customer_id = int(input("Enter Customer ID: "))
            if customer_id not in system.customers:
                print("Customer not found!")
                continue

            items = input("Enter items (comma-separated): ").split(",")
            items = [item.strip() for item in items]

            item_quantities = {}
            for item in items:
                if item not in inventory.items:
                    print(f"Item '{item}' is not available.")
                    continue

                quantity = int(input(f"Enter quantity for {item}: "))
                if inventory.items[item] < quantity:
                    print(f"Insufficient stock for {item}. Available: {inventory.items[item]}")
                    continue

                item_quantities[item] = quantity

            if not item_quantities:
                print("No valid items for this order.")
                continue

            order_id = max(system.orders.keys(), default=100) + 1
            order_items_list = [f"{item} x{quantity}" for item, quantity in item_quantities.items()]
            order = Order(order_id, system.customers[customer_id], order_items_list)
            system.place_order(order)

            for item, quantity in item_quantities.items():
                inventory.remove_item(item, quantity)

            print(f"\nOrder {order_id} placed successfully!")
            print(f"Customer: {system.customers[customer_id].name}")

            total_price = 0
            print("Items Purchased:")
            for item, quantity in item_quantities.items():
                price = inventory.prices.get(item, 0)
                item_total = price * quantity
                total_price += item_total
                print(f"  {item} - {quantity} units @ ${price:.2f} each = ${item_total:.2f}")

            print(f"Total Price: ${total_price:.2f}")

            # Update Excel
            update_order_sheet(order, item_quantities, inventory)

        elif choice == '2':
            print("\nInventory List:")
            for item, quantity in inventory.get_inventory().items():
                price = inventory.prices.get(item, "N/A")
                print(f"{item}: {quantity} units - ${price} each")

        elif choice == '3':
            print("\nOrder List:")
            for order in system.orders.values():
                print(order.get_order_details())

        elif choice == '4':
            print("\nCustomer List:")
            for customer_id, customer in system.customers.items():
                order_ids = system.get_customer_orders(customer_id)
                print(f"{customer.get_customer_info()} | Orders: {order_ids}")

        elif choice == '5':
            item_name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per unit: "))
            inventory.add_item(item_name, quantity)
            inventory.prices[item_name] = price
            print(f"{quantity} units of {item_name} added at ${price:.2f} each.")

            # Update Excel
            update_inventory_sheet(item_name, quantity, price)

        elif choice == '6':
            customer_id = int(input("Enter Customer ID: "))
            name = input("Enter Customer Name: ")
            email = input("Enter Customer Email: ")
            customer = Customer(customer_id, name, email)
            system.add_customer(customer)
            print(f"Customer {name} added successfully.")

            # Update Excel
            update_customer_sheet(customer)

        elif choice == '7':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()