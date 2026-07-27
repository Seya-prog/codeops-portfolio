# 1. Book class
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def describe(self):
        print(f"'{self.title}' by {self.author}, {self.pages} pages")

book1 = Book("Fikir Eske Mekabir", "Haddis Alemayehu", 554)
book2 = Book("Oromay", "Bealu Girma", 370)
book1.describe()
book2.describe()

print("\n---")

# 2. Product class, 3. Make it private, 4. Validate
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.__quantity = quantity # Private attribute

    @property
    def quantity(self):
        return self.__quantity

    def restock(self, n):
        if n > 0:
            self.__quantity += n
        else:
            print("Restock amount must be positive.")

    def sell(self, n):
        if n <= 0:
            print("Sell amount must be positive.")
        elif n > self.__quantity:
            print(f"Error: Cannot sell {n} {self.name}(s). Only {self.__quantity} in stock.")
        else:
            self.__quantity -= n

# 5. Prove independence
p1 = Product("Soap", 25, 100)
p2 = Product("Shampoo", 150, 50)
p3 = Product("Toothpaste", 80, 200)

# Changing p1 and p2 should leave p3 unaffected
p1.sell(30)
p2.restock(20)

print(f"{p1.name} quantity: {p1.quantity}")
print(f"{p2.name} quantity: {p2.quantity}")
print(f"{p3.name} quantity: {p3.quantity}")
