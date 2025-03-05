#The purpose is that it initializes a new customer object with an ID, name, and email.
#customer_id is a unique idetifier for each customer.
#name is the customers full name.
#email is the customers email address.
class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

#Returns a formatted string with the customer's details.
    def get_customer_info(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"