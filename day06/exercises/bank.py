from abc import ABC, abstractmethod

# --- Observer Pattern (SRP: Alerting is split out) ---
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class SMSAlert(Observer):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def update(self, message):
        print(f"[SMS to {self.phone_number}] {message}")


# --- Accounts (Observable) ---
class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self.__balance = balance
        self._observers = []

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
        self._notify(f"Deposited {amount} ETB. New balance: {self.balance:.2f} ETB")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        self._notify(f"Withdrew {amount} ETB. New balance: {self.balance:.2f} ETB")

    def statement(self):
        print(f"[Account] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")


class SavingsAccount(Account):
    def __init__(self, owner, number, balance=0, rate=0.05):
        super().__init__(owner, number, balance)
        self.rate = rate

    def add_interest(self):
        interest = self.balance * self.rate
        self.deposit(interest)

    def statement(self):
        print(f"[Savings] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")


class CurrentAccount(Account):
    def __init__(self, owner, number, balance=0, overdraft=1000):
        super().__init__(owner, number, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance - amount < -self.overdraft:
            raise ValueError("Overdraft limit exceeded")
        # Updating the parent's private balance using name mangling
        self._Account__balance -= amount
        self._notify(f"Withdrew {amount} ETB. New balance: {self.balance:.2f} ETB")

    def statement(self):
        print(f"[Current] Owner: {self.owner} | Account: {self.account_number} | Balance: {self.balance:.2f} ETB")


# --- Factory Pattern ---
class AccountFactory:
    @staticmethod
    def create(kind, owner, number, balance=0, **kwargs):
        kind = kind.lower()
        if kind == "savings":
            return SavingsAccount(owner, number, balance, rate=kwargs.get("rate", 0.05))
        elif kind == "current":
            return CurrentAccount(owner, number, balance, overdraft=kwargs.get("overdraft", 1000))
        elif kind == "account":
            return Account(owner, number, balance)
        else:
            raise ValueError(f"Unknown account type: {kind}")


# --- Testing the Implementation ---
if __name__ == "__main__":
    print("--- Creating Accounts via Factory ---")
    almaz_acc = AccountFactory.create("savings", "Almaz", "1002", 1500, rate=0.07)
    dawit_acc = AccountFactory.create("current", "Dawit", "1003", 800, overdraft=500)

    # Attach SMS alerts
    almaz_sms = SMSAlert("+251911000000")
    dawit_sms = SMSAlert("+251912000000")
    
    almaz_acc.subscribe(almaz_sms)
    dawit_acc.subscribe(dawit_sms)

    print("\n--- Processing Transactions ---")
    almaz_acc.add_interest()
    dawit_acc.withdraw(1000)

    print("\n--- Final Statements ---")
    almaz_acc.statement()
    dawit_acc.statement()
