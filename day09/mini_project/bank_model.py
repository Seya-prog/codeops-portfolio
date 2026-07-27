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
        pass

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
        self.history = []

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
            return
        action, amount = self.history.pop()
        if action == "deposit":
            self.__balance -= amount
        elif action == "withdraw":
            self.__balance += amount
        self._notify(f"Account {self.account_number} ({self.owner}) | Undo {action.capitalize()} of {amount:.2f} ETB | New Balance: {self.balance:.2f} ETB")

    def total_transactions(self, history_subset=None):
        if history_subset is None:
            history_subset = self.history
        if not history_subset:
            return 0
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

    def find(self, account_number):
        return self._accounts.get(account_number)

    def find_by_number(self, account_number):
        nums = sorted(list(self._accounts.keys()))
        def binary_search(items, target):
            lo, hi = 0, len(items) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if items[mid] == target:
                    return mid
                elif items[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return -1
        i = binary_search(nums, account_number)
        return self._accounts[nums[i]] if i >= 0 else None

    def top_by_balance(self, n):
        sorted_accounts = sorted(self._accounts.values(), key=lambda acc: acc.balance, reverse=True)
        return sorted_accounts[:n]

    def list_all(self):
        print("\n--- All Registered Accounts ---")
        for acc_num in sorted(self._accounts.keys()):
            self._accounts[acc_num].statement()

    def total_transactions(self, account_number):
        account = self.find_by_number(account_number)
        if not account:
            return 0
        def _recursive_sum(history_list):
            if not history_list:
                return 0
            _, amount = history_list[0]
            return amount + _recursive_sum(history_list[1:])
        return _recursive_sum(account.history)

# --- Day 09: Trees (Branch Hierarchy) ---
class Branch:
    def __init__(self, name):
        self.name = name
        self.sub_branches = []
        self.registry = AccountRegistry()

    def add_sub_branch(self, branch):
        self.sub_branches.append(branch)

    def total_balance(self):
        """Recursively sums the balance of this branch and all its sub-branches."""
        # Sum local accounts in this branch
        current_total = sum(acc.balance for acc in self.registry._accounts.values())
        
        # Recursively add sub-branches
        for child in self.sub_branches:
            current_total += child.total_balance()
            
        return current_total

# --- Day 09: Graphs (Transfers Network) ---
def bfs(graph, start_node):
    """Breadth-First Search to find all reachable nodes in a graph."""
    visited = set()
    queue = [start_node]
    reachable = []
    
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            reachable.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
                    
    return reachable


# --- Testing the Implementation ---
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

    print("--- 1. Creating Accounts ---")
    almaz_acc = AccountFactory.create("savings", "Almaz", "1002", 1500) 
    dawit_acc = AccountFactory.create("current", "Dawit", "1003", 800)
    hanna_acc = AccountFactory.create("savings", "Hanna", "1004", 5000)
    samuel_acc = AccountFactory.create("current", "Samuel", "1001", 200)

    print("\n--- 2. Building Branch Tree ---")
    head_office = Branch("Head Office")
    
    north_region = Branch("North Region")
    south_region = Branch("South Region")
    
    branch_a = Branch("Branch A")
    branch_b = Branch("Branch B")
    branch_c = Branch("Branch C")

    # Connect the tree
    head_office.add_sub_branch(north_region)
    head_office.add_sub_branch(south_region)
    
    north_region.add_sub_branch(branch_a)
    north_region.add_sub_branch(branch_b)
    south_region.add_sub_branch(branch_c)

    # Assign accounts to branches
    branch_a.registry.add(almaz_acc)
    branch_a.registry.add(dawit_acc)
    
    branch_b.registry.add(hanna_acc)
    
    branch_c.registry.add(samuel_acc)

    print("\n--- 3. Testing Recursive Branch Total ---")
    # Total for North Region (Branch A + Branch B) = (1500 + 800) + 5000 = 7300
    print(f"North Region Total Balance: {north_region.total_balance():.2f} ETB")
    
    # Total for Head Office (All branches) = 7300 + 200 = 7500
    print(f"Head Office Total Balance (Bank Total): {head_office.total_balance():.2f} ETB")

    print("\n--- 4. Building Transfers Graph ---")
    transfers_graph = {
        "CBE-1": ["CBE-2", "CBE-3"],
        "CBE-2": ["CBE-4"],
        "CBE-3": ["CBE-4"],
        "CBE-4": ["CBE-5"],
        "CBE-5": []
    }

    print("\n--- 5. Testing BFS over Transfers Graph ---")
    reachable_from_cbe1 = bfs(transfers_graph, "CBE-1")
    print(f"Banks reachable from CBE-1: {reachable_from_cbe1}")
