# 1. Unique cities
cities = ["Addis Ababa", "Adama", "Hawassa", "Adama", "Bahir Dar", "Addis Ababa"]
unique_cities = set(cities)
print("Unique cities:", unique_cities)
print("Count:", len(unique_cities))
print("\n---")

# 2. Price report
prices = {"Bread": 50, "Milk": 80, "Eggs": 120, "Coffee": 300, "Sugar": 60}
for item, price in prices.items():
    print(f"{item}: {price} ETB")
print("\n---")

# 3. Tax comprehension
prices_list = [100, 250, 400, 80]
with_tax = [p * 1.15 for p in prices_list]
print("Prices with tax:", with_tax)
print("\n---")

# 4. Cheap items
cheap = [p for p in prices_list if p < 200]
print("Cheap items (under 200):", cheap)
print("\n---")

# 5. Write & read
names = ["Almaz", "Dawit", "Tigist"]
with open("names.txt", "w") as f:
    for name in names:
        f.write(f"{name}\n")

print("Reading names.txt:")
with open("names.txt", "r") as f:
    for line in f:
        print(line.strip())
print("\n---")

# 6. Safe division
try:
    amount_str = input("Amount to divide 1000 by: ")
    amount = int(amount_str)
    result = 1000 / amount
    print(f"1000 / {amount} = {result}")
except ValueError:
    print("Please enter a valid number")
except ZeroDivisionError:
    print("Amount can't be zero")
