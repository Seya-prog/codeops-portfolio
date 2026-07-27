class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self.__balance = balance # Encapsulated private balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount

    def statement(self):
        print(f"Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance} ETB")


# Testing the implementation
if __name__ == "__main__":
    acc1 = Account("Almaz Bekele", "100010001000", 1500)
    acc2 = Account("Dawit Tesfaye", "100020002000", 800)

    print("--- Initial Statements ---")
    acc1.statement()
    acc2.statement()

    print("\n--- Performing Transactions ---")
    acc1.deposit(500)
    print("Deposited 500 into Almaz's account.")
    
    acc2.withdraw(200)
    print("Withdrew 200 from Dawit's account.")

    print("\n--- Final Statements ---")
    acc1.statement()
    acc2.statement()

    print("\n--- Testing Validations ---")
    try:
        acc1.withdraw(5000) # Trying to overdraft
    except ValueError as e:
        print(f"Error caught for Almaz: {e}")
        
    try:
        acc2.deposit(-100) # Trying to deposit negative
    except ValueError as e:
        print(f"Error caught for Dawit: {e}")
