import os

script_dir = os.path.dirname(__file__)
transactions_file = os.path.join(script_dir, "transactions.txt")
report_file = os.path.join(script_dir, "report.txt")

totals = {}
try:
    with open(transactions_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                name, amount_str = line.split(",")
                amount = float(amount_str)
                totals[name] = totals.get(name, 0) + amount
    print(f"Successfully processed {transactions_file}")
except FileNotFoundError:
    print(f"Error: {transactions_file} not found.")

if totals:
    sorted_customers = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    
    print("\nCustomer Spending Summary:")
    print("-" * 30)
    for customer, total in sorted_customers:
        print(f"{customer}: {total:.2f} ETB")

    with open(report_file, "w") as f:
        f.write("Customer Spending Summary\n")
        f.write("-" * 30 + "\n")
        for customer, total in sorted_customers:
            f.write(f"{customer}: {total:.2f} ETB\n")
    print(f"\nReport saved to {report_file}")
