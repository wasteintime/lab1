#task1
def square_generator(n):
    for i in range(n + 1):
        yield i ** 2

# Usage
for square in square_generator(5):
    print(square) # 0, 1, 4, 9, 16, 25

#task2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

n = int(input("Enter n: "))
# Join the yielded strings with commas
print(",".join(even_numbers(n)))

#task3
def divisible_by_3_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# Example: range 0 to 50
for num in divisible_by_3_4(50):
    print(num)


#task4
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

# Testing with a for loop
for val in squares(3, 6):
    print(f"Yielded value: {val}")

#task5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

# Usage
for num in countdown(5):
    print(num)

