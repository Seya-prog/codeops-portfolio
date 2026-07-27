# 1. Build a BST
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

def in_order(node):
    if node is None:
        return
    in_order(node.left)
    print(node.value, end=" ")
    in_order(node.right)


# 2. Tree depth
def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


# 3. Graph BFS
from collections import deque

def bfs(graph, start):
    seen = {start}
    q = deque([start])
    reachable = [start]
    
    while q:
        node = q.popleft()
        for n in graph.get(node, []):
            if n not in seen:
                seen.add(n)
                q.append(n)
                reachable.append(n)
    return reachable


# 4. Graph DFS
def dfs(graph, start, seen=None, reachable=None):
    if seen is None:
        seen = set()
    if reachable is None:
        reachable = []
        
    seen.add(start)
    reachable.append(start)
    
    for n in graph.get(start, []):
        if n not in seen:
            dfs(graph, n, seen, reachable)
            
    return reachable


# 5. Priority queue
import heapq

def test_priority_queue():
    queue = []
    # (priority, task)
    heapq.heappush(queue, (3, "Pay bills"))
    heapq.heappush(queue, (1, "Emergency response"))
    heapq.heappush(queue, (5, "Watch TV"))
    heapq.heappush(queue, (2, "Go to work"))
    heapq.heappush(queue, (4, "Read a book"))
    
    results = []
    while queue:
        results.append(heapq.heappop(queue))
    return results


if __name__ == "__main__":
    print("--- 1. BST (Insert & In-Order) ---")
    root = None
    balances = [1500, 800, 5000, 200, 1000]
    for b in balances:
        root = insert(root, b)
    print("In-order traversal (sorted):")
    in_order(root)
    print("\n")

    print("--- 2. Tree Depth ---")
    print(f"Depth of the BST: {height(root)}")

    print("\n--- 3. Graph BFS ---")
    graph = {
        "Almaz": ["Dawit", "Tigist", "Samuel"],
        "Dawit": ["Almaz", "Hanna"],
        "Tigist": ["Almaz", "Samuel"],
        "Samuel": ["Almaz", "Tigist", "Hanna"],
        "Hanna": ["Dawit", "Samuel"]
    }
    print(f"BFS from Almaz: {bfs(graph, 'Almaz')}")

    print("\n--- 4. Graph DFS ---")
    print(f"DFS from Almaz: {dfs(graph, 'Almaz')}")

    print("\n--- 5. Priority Queue (Heap) ---")
    print("Tasks ordered by priority (lowest number first):")
    for priority, task in test_priority_queue():
        print(f"  Priority {priority}: {task}")
