# 1. Temperature label
try:
    temp_input = input("Enter temperature in °C: ")
    temp = float(temp_input)
    if temp < 15:
        print("cold")
    elif temp <= 28:
        print("warm")
    else:
        print("hot")
except ValueError:
    print("Invalid temperature input.")

print("\n---")

# 2. Receipt loop
for i in range(1, 11):
    print(f"Receipt #{i}")

print("\n---")

# 3. Even numbers
for i in range(1, 21):
    if i % 2 == 0:
        print(i)

print("\n---")

# 4. Discount function
def apply_discount(price, percent=10):
    return price - (price * percent / 100)

print(f"Price: 1000, Default discount (10%): {apply_discount(1000)}")
print(f"Price: 1000, Custom discount (25%): {apply_discount(1000, 25)}")

print("\n---")

# 5. Countdown
count = 5
while count > 0:
    print(count)
    count -= 1
print("Liftoff!")
