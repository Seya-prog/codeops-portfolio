import os

script_dir = os.path.dirname(__file__)
stock_file = os.path.join(script_dir, "stock.txt")
stock = {}

# 1. Read stock from file
try:
    with open(stock_file, "r") as f:
        for line in f:
            if line.strip():
                item, qty = line.strip().split(",")
                stock[item] = int(qty)
    print("Stock loaded successfully.")
except FileNotFoundError:
    print("No stock file yet — starting empty")

# 2. Function to adjust stock
def adjust(item, amount):
    stock[item] = stock.get(item, 0) + amount

# Adjusting stock manually to test the script
adjust("Paracetamol", 20)
adjust("Ibuprofen", 5) 
adjust("Vitamin C", -5) # Simulating sales
adjust("Cough Syrup", -1) 

# 3. Report low stock items (less than 10)
low_stock = [item for item, qty in stock.items() if qty < 10]
print(f"\nLow stock alert (qty < 10): {low_stock}")

# 4. Save updated stock back to file
with open(stock_file, "w") as f:
    for item, qty in stock.items():
        f.write(f"{item},{qty}\n")

print("\nUpdated stock saved to stock.txt.")
