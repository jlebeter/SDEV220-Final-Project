class Order:

#order_id is a unique identifier for the order.
#customer object represents the buyer
#items is a dictionary representing items purchased.
    def __init__(self, order_id, customer, items):
        self.order_id = order_id
        self.customer = customer
        self.items = items

#Formats order details as a readable string.
    def get_order_details(self):
        item_details = ', '.join(f"{item} x{qty}" for item, qty in self.items.items())
        return f"Order ID: {self.order_id}, Customer: {self.customer.name}, Items: {item_details}"