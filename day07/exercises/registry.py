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
        print(f"[SMS -> {self.phone_number}] {message}")

class AuditLog(Observer):
    def __init__(self, log_file="audit.log"):
        self.log_file = log_file

    def update(self, message):
        print(f"[AuditLog] Logging to {self.log_file} ...")
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

# --- Account Registry (O(1) lookups) ---
class AccountRegistry:
    def __init__(self):
        self._accounts = {}

    def add(self, account):
        self._accounts[account.account_number] = account

    def find(self, account_number):
        return self._accounts.get(account_number)

    def list_all(self):
        print("\n--- All Registered Accounts ---")
        for acc_num in sorted(self._accounts.keys()):
            self._accounts[acc_num].statement()

# --- Testing the Implementation ---
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

    print("--- 1. Configuring Bank (Singleton) ---")
    config = BankConfig()
    config.savings_rate = 0.10
    config.overdraft_limit = 2000

    print("\n--- 2. Creating Accounts (Factory) ---")
    almaz_acc = AccountFactory.create("savings", "Almaz", "1002", 1500) 
    dawit_acc = AccountFactory.create("current", "Dawit", "1003", 800)

    print("\n--- 3. Setting Up Registry ---")
    registry = AccountRegistry()
    registry.add(almaz_acc)
    registry.add(dawit_acc)

    print("\n--- 4. Setting Up Observers ---")
    audit_log = AuditLog("audit.log") 
    almaz_acc.subscribe(audit_log)
    dawit_acc.subscribe(audit_log)

    print("\n--- 5. Executing Transactions ---")
    acc = registry.find("1002") # O(1) lookup
    if acc:
        acc.deposit(500)
    
    acc2 = registry.find("1003")
    if acc2:
        acc2.withdraw(1500) # (800 - 1500 = -700, uses overdraft)

    print("\n--- 6. Testing Undo Stack ---")
    acc2.undo_last() # Reverts the 1500 withdrawal

    print("\n--- 7. Listing All Accounts ---")
    registry.list_all()
