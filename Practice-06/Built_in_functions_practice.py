from functools import reduce

# Подготовка данных
nums = [1, 5, 2, 8, 3]

# 1. Агрегаты
print(f"Len: {len(nums)}, Sum: {sum(nums)}, Max: {max(nums)}")

# 2. map() и filter()
# Квадраты чисел больше 3
squared = list(map(lambda x: x**2, filter(lambda x: x > 3, nums)))
print(f"Squared numbers > 3: {squared}")

# 3. reduce() - произведение всех чисел
product = reduce(lambda x, y: x * y, nums)
print(f"Product: {product}")

# 4. enumerate() и zip()
fruits = ["apple", "banana", "cherry"]
counts = [10, 20, 30]

print("--- Iteration with Zip & Enumerate ---")
for i, (fruit, count) in enumerate(zip(fruits, counts), 1):
    print(f"{i}. {fruit}: {count} pcs")

# 5. Сортировка и конвертация
sorted_nums = sorted(nums, reverse=True)
str_nums = str(nums) # Конвертация списка в строку
print(f"Sorted: {sorted_nums}, Type: {type(str_nums)}")