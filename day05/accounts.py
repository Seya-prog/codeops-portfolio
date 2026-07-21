class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self.__balance = balance

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
        print(f"[Account] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")


class SavingsAccount(Account):
    def __init__(self, owner, number, balance=0, rate=0.05):
        super().__init__(owner, number, balance)
        self.rate = rate

    def add_interest(self):
        # Reusing the parent's deposit method
        self.deposit(self.balance * self.rate)

    def statement(self):
        # Override to label the account type
        print(f"[Savings] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")


class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft=1000):
        super().__init__(owner, number, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        # Overridden to allow the overdraft
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance - amount < -self.overdraft:
            raise ValueError("Overdraft limit exceeded")
        # Directly modify parent's private balance using name mangling
        self._Account__balance -= amount

    def statement(self):
        # Override to label the account type
        print(f"[Current] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")


if __name__ == "__main__":
    # Polymorphism: Put different account types in one list and loop
    accounts = [
        Account("Hanna", "1001", 1500),
        SavingsAccount("Almaz", "1002", 1500),
        CurrentAccount("Dawit", "1003", 800)
    ]

    print("--- Initial Statements ---")
    for acc in accounts:
        acc.statement()

    print("\n--- Processing Transactions ---")
    accounts[1].add_interest()
    print("Added interest to Almaz's Savings Account.")
    
    accounts[2].withdraw(1200) # (800 - 1200 = -400) - utilizing overdraft
    print("Withdrew 1200 from Dawit's Current Account.")

    print("\n--- Final Statements ---")
    for acc in accounts:
        acc.statement()
