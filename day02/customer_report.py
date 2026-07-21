customers = [
    ("Almaz", 1500), 
    ("Dawit", 700), 
    ("Tigist", 200),
    ("Hanna", 1200), 
    ("Samuel", 450),
]

def tier(balance):
    if balance >= 1000:
        return "Premium"
    elif balance >= 500:
        return "Standard"
    return "Basic"

# Dictionary to keep track of the count for each tier
tier_counts = {
    "Premium": 0,
    "Standard": 0,
    "Basic": 0
}

print("=== TeleBirr Customer Report ===")
for name, balance in customers:
    customer_tier = tier(balance)
    print(f"{name}: {customer_tier} ({balance} ETB)")
    # Increment the count for the assigned tier
    tier_counts[customer_tier] += 1

print("\n=== Summary ===")
for t, count in tier_counts.items():
    print(f"{t}: {count} customer(s)")
