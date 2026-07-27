from abc import ABC, abstractmethod
import os

# --- Singleton Pattern ---
class BankConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BankConfig, cls).__new__(cls)
            cls._instance.savings_rate = 0.05
            cls._instance.overdraft_limit = 1000
        return cls._instance

# --- Observer Pattern ---
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class SMSAlert(Observer):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def update(self, message):
        pass # print(f"[SMS -> {self.phone_number}] {message}")

class AuditLog(Observer):
    def __init__(self, log_file="audit.log"):
        self.log_file = log_file

    def update(self, message):
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

# --- Accounts (Observable) ---
class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self.__balance = balance
        self._observers = []
        self.history = [] # Stack for transaction history

    @property
    def balance(self):
        return self.__balance

    def subscribe(self, observer):
        self._observers.append(observer)

    def _notify(self, message):
        for observer in self._observers:
            observer.update(message)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount
        self.history.append(("deposit", amount))
        self._notify(f"Account {self.account_number} ({self.owner}) | Deposit: {amount:.2f} ETB | New Balance: {self.balance:.2f} ETB")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        self.history.append(("withdraw", amount))
        self._notify(f"Account {self.account_number} ({self.owner}) | Withdrawal: {amount:.2f} ETB | New Balance: {self.balance:.2f} ETB")

    def undo_last(self):
        if not self.history:
            print(f"Account {self.account_number}: No transactions to undo.")
            return
        action, amount = self.history.pop()
        if action == "deposit":
            self.__balance -= amount
        elif action == "withdraw":
            self.__balance += amount
        self._notify(f"Account {self.account_number} ({self.owner}) | Undo {action.capitalize()} of {amount:.2f} ETB | New Balance: {self.balance:.2f} ETB")

    # NEW: Recursive total_transactions
    def total_transactions(self, history_subset=None):
        """Recursively calculates the total volume (sum of amounts) of transactions."""
        if history_subset is None:
            history_subset = self.history
            
        # Base case
        if not history_subset:
            return 0
            
        # Recursive step
        _, amount = history_subset[0]
        return amount + self.total_transactions(history_subset[1:])

    def statement(self):
        print(f"[Account] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")

class SavingsAccount(Account):
    def __init__(self, owner, number, balance=0, rate=None):
        super().__init__(owner, number, balance)
        self.rate = rate if rate is not None else BankConfig().savings_rate

    def add_interest(self):
        interest = self.balance * self.rate
        self.deposit(interest)

    def statement(self):
        print(f"[Savings] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")

class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft=None):
        super().__init__(owner, number, balance)
        self.overdraft = overdraft if overdraft is not None else BankConfig().overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance - amount < -self.overdraft:
            raise ValueError("Overdraft limit exceeded")
        self._Account__balance -= amount
        self.history.append(("withdraw", amount))
        self._notify(f"Account {self.account_number} ({self.owner}) | Withdrawal: {amount:.2f} ETB | New Balance: {self.balance:.2f} ETB")

    def statement(self):
        print(f"[Current] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")

# --- Factory Pattern ---
class AccountFactory:
    @staticmethod
    def create(kind, owner, number, balance=0, **kwargs):
        kind = kind.lower()
        if kind == "savings":
            return SavingsAccount(owner, number, balance, rate=kwargs.get("rate"))
        elif kind == "current":
            return CurrentAccount(owner, number, balance, overdraft=kwargs.get("overdraft"))
        elif kind == "account":
            return Account(owner, number, balance)
        else:
            raise ValueError(f"Unknown account type: {kind}")

# --- Account Registry ---
class AccountRegistry:
    def __init__(self):
        self._accounts = {}

    def add(self, account):
        self._accounts[account.account_number] = account

    # O(1) Dictionary Lookup
    def find(self, account_number):
        return self._accounts.get(account_number)

    # NEW: O(log n) Binary Search Lookup
    def find_by_number(self, account_number):
        """Finds an account by number using binary search."""
        acc_numbers = sorted(list(self._accounts.keys())) # Get sorted list of keys
        
        low = 0
        high = len(acc_numbers) - 1
        
        while low <= high:
            mid = (low + high) // 2
            guess = acc_numbers[mid]
            
            if guess == account_number:
                return self._accounts[guess]
            if guess > account_number:
                high = mid - 1
            else:
                low = mid + 1
        return None

    # NEW: Leaderboard sorted by balance
    def top_by_balance(self, n):
        """Returns the top N accounts sorted by balance descending."""
        sorted_accounts = sorted(self._accounts.values(), key=lambda acc: acc.balance, reverse=True)
        return sorted_accounts[:n]

    def list_all(self):
        print("\n--- All Registered Accounts ---")
        for acc_num in sorted(self._accounts.keys()):
            self._accounts[acc_num].statement()

# --- Testing the Implementation ---
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

    print("--- 1. Configuring Bank & Creating Accounts ---")
    config = BankConfig()
    almaz_acc = AccountFactory.create("savings", "Almaz", "1002", 1500) 
    dawit_acc = AccountFactory.create("current", "Dawit", "1003", 800)
    hanna_acc = AccountFactory.create("savings", "Hanna", "1004", 5000)
    samuel_acc = AccountFactory.create("current", "Samuel", "1001", 200)

    print("\n--- 2. Setting Up Registry ---")
    registry = AccountRegistry()
    registry.add(almaz_acc)
    registry.add(dawit_acc)
    registry.add(hanna_acc)
    registry.add(samuel_acc)

    print("\n--- 3. Executing Transactions ---")
    almaz_acc.deposit(500)
    dawit_acc.withdraw(100)
    dawit_acc.deposit(200)
    hanna_acc.deposit(1000)
    samuel_acc.withdraw(50)

    print("\n--- 4. Testing Binary Search: find_by_number('1003') ---")
    found_acc = registry.find_by_number("1003")
    if found_acc:
        print("Found via Binary Search:")
        found_acc.statement()
    else:
        print("Account not found.")

    print("\n--- 5. Testing Leaderboard: top_by_balance(2) ---")
    top_2 = registry.top_by_balance(2)
    for i, acc in enumerate(top_2, 1):
        print(f"#{i}", end=" ")
        acc.statement()

    print("\n--- 6. Testing Recursive total_transactions() ---")
    # Dawit had a withdraw of 100 and a deposit of 200, total volume = 300
    total_volume = dawit_acc.total_transactions()
    print(f"Dawit's Total Transaction Volume (Recursive Calculation): {total_volume:.2f} ETB")
