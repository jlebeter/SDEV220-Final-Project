class System:

#customer maps customer_id to Customer object
#orders maps ord_id to Object order.
#customer_orders maps customer_id to list of order_id.
    def __init__(self):
        self.customers = {}
        self.orders = {}
        self.customer_orders = {}

#Adds a new customer to the system.
#Initializes an empty list in customer_orders to track future orders.
    def add_customer(self, customer):
        self.customers[customer.customer_id] = customer
        self.customer_orders[customer.customer_id] = []

#Stores the order in orders dictionary.
#Links the order to the customer in customer_orders.
    def place_order(self, order):
        self.orders[order.order_id] = order
        if order.customer.customer_id in self.customer_orders:
            self.customer_orders[order.customer.customer_id].append(order.order_id)
        else:
            self.customer_orders[order.customer.customer_id] = [order.order_id]

#Returns a list of order IDs if the customer exists.
#Returns an error message if the customer is not found.
    def get_customer_orders(self, customer_id):
        if customer_id in self.customer_orders:
            return self.customer_orders[customer_id]
        else:
            return "Customer not found or no orders placed."