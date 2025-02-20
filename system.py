class Order:
    def __init__(self, order_id, customer, items):
        self.order_id = order_id
        self.customer = customer
        self.items = items

    def get_order_details(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer.name}, Items: {', '.join(self.items)}"


class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, quantity):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def remove_item(self, item_name, quantity):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]
        else:
            raise ValueError("Item not available or insufficient quantity")

    def get_inventory(self):
        return self.items


class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def get_customer_info(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"


class System:
    def __init__(self):
        self.customers = {}
        self.orders = {}
        self.customer_orders = {}

    def add_customer(self, customer):
        self.customers[customer.customer_id] = customer
        self.customer_orders[customer.customer_id] = []

    def place_order(self, order):
        self.orders[order.order_id] = order
        if order.customer.customer_id in self.customer_orders:
            self.customer_orders[order.customer.customer_id].append(order.order_id)
        else:
            self.customer_orders[order.customer.customer_id] = [order.order_id]

    def get_customer_orders(self, customer_id):
        if customer_id in self.customer_orders:
            return self.customer_orders[customer_id]
        else:
            return "Customer not found or no orders placed."
