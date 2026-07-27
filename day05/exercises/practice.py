from abc import ABC, abstractmethod

# 1. Vehicle hierarchy & 5. Abstract method
class Vehicle(ABC):
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def describe(self):
        print(f"This is a {self.make} {self.model}.")

    @abstractmethod
    def wheels(self):
        pass

# 2. Use super() & 3. Override
class Car(Vehicle):
    def wheels(self):
        return 4

class Truck(Vehicle):
    def __init__(self, make, model, capacity):
        super().__init__(make, model) # Reusing parent's __init__
        self.capacity = capacity

    def describe(self): # Overriding parent's method
        print(f"This is a {self.make} {self.model} with a capacity of {self.capacity} tons.")

    def wheels(self):
        return 18

# 4. Polymorphism
vehicles = [
    Car("Toyota", "Corolla"),
    Truck("Volvo", "FH16", 40),
    Car("Honda", "Civic")
]

print("--- Vehicle Fleet ---")
for v in vehicles:
    v.describe()
    print(f"It has {v.wheels()} wheels.")
    print("-")
