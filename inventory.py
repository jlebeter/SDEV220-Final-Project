#items stores item names as keys and their quantities as values.
#prices stores item names as keys and their prices as values.
class Inventory:
    def __init__(self):
        self.items = {}
        self.prices = {}

#Adds a new item or updates an existing one.
#Ensures price is updated even if quantity changes.
    def add_item(self, item_name, quantity, price):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        self.prices[item_name] = price

#Checks if item exists and has enough quantity.
#Reduces quanitity or removes item completly if it reaches zero.
#Raises an error if item does not exist or quantity is insufficient.
    def remove_item(self, item_name, quantity):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]
                del self.prices[item_name]
        else:
            raise ValueError("Item not available or insufficient quantity")

#Returns the current inventory as a dictionary.
    def get_inventory(self):
        return self.items

#Returns the price of an item or 0 if the item doesn't exist.
    def get_price(self, item_name):
        return self.prices.get(item_name, 0)