# 1. Recursive sum & countdown
def total(nums):
    if not nums:
        return 0
    return nums[0] + total(nums[1:])

def count_down(n):
    if n <= 0:
        return
    print(n)
    count_down(n - 1)

# 2. Binary search
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

# 3. Merge sort
def merge_sort(items):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 4. Sort with a key
def sort_accounts(accounts):
    return sorted(accounts, key=lambda a: a[1], reverse=True)

# 5. Two pointers
def has_pair(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target: 
            return True
        elif s < target: 
            lo += 1
        else: 
            hi -= 1
    return False

if __name__ == "__main__":
    print("--- 1. Recursive ---")
    print(f"Total: {total([100, 250, 400])}")
    print("Countdown:")
    count_down(3)

    print("\n--- 2. Binary Search ---")
    balances = [100, 200, 500, 1000, 1500]
    print(f"Index of 500: {binary_search(balances, 500)}")
    print(f"Index of 300 (absent): {binary_search(balances, 300)}")

    print("\n--- 3. Merge Sort ---")
    unordered = [400, 100, 500, 250]
    print(f"Sorted: {merge_sort(unordered)}")

    print("\n--- 4. Sort with Key ---")
    accs = [("Almaz", 1500), ("Dawit", 800), ("Hanna", 5000)]
    print(f"Sorted by balance: {sort_accounts(accs)}")

    print("\n--- 5. Two Pointers ---")
    sorted_nums = [10, 20, 30, 40, 50]
    print(f"Has pair summing to 60? {has_pair(sorted_nums, 60)}")
    print(f"Has pair summing to 100? {has_pair(sorted_nums, 100)}")
