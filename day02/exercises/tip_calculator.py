# TeleBirr Tip Calculator

# 1. Store a bill total (ETB) and number of people in variables.
bill_total = 1500  # ETB
friends = ["Almaz", "Dawit", "Tigist", "Hanna", "Samuel"]
num_people = len(friends)

# 2. Write a function split_bill(total, people, tip_rate=0.10).
def split_bill(total, people, tip_rate=0.10):
    total_with_tip = total * (1 + tip_rate)
    return total_with_tip / people

# 3. Use it to compute the per-person amount, tip included.
per_person_share = split_bill(bill_total, num_people)

# 4. Loop over a list of names and print each person's share.
print("=== TeleBirr Tip Calculator ===")
print(f"Total Bill: {bill_total} ETB")
print(f"Tip rate: 10%")
print(f"Number of people: {num_people}")
print("-" * 30)

for friend in friends:
    print(f"{friend} needs to pay: {per_person_share:.2f} ETB")
