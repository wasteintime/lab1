print(11 > 9)
print(21 == 9)
print(34 < 3)
print(23 > 11)
print(34 == 34)

# 1
a = 10
b = 20

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")
# 2
a = 50
b = 30

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")
# 3
a = 7
b = 7

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")
# 4
a = -5
b = 0

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")
# 5
a = 100
b = 101

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")


# 1
print(bool("Hi"))
print(bool(10))
# 2
a = "Python"
b = 0

print(bool(a))
print(bool(b))
# 3
x = ""
y = -5

print(bool(x))
print(bool(y))
# 4
text = " "
num = 1

print(bool(text))
print(bool(num))
# 5
s = "False"
n = 0

print(bool(s))
print(bool(n))


bool("abc")
bool(123)
bool(["grape", "berry", "banana"])
bool(222)
bool(['1', '2', '3'])


bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

# ========= 1. ОБЪЕКТЫ И bool() =========

class A:
    def __len__(self):
        return 0

class B:
    def __len__(self):
        return False

class C:
    def __len__(self):
        return 3

class D:
    def __len__(self):
        return 1

class E:
    def __len__(self):
        return 0


print(bool(A()))     # False
print(bool(B()))     # False
print(bool(C()))     # True
print(bool(D()))     # True

if E():
    print("E is True")
else:
    print("E is False")


# ========= 2. ФУНКЦИИ, КОТОРЫЕ ВОЗВРАЩАЮТ Boolean =========

def f1():
    return False

def f2():
    return 10 > 5

def f3():
    return 3 == 4

def f4():
    return bool(1)

def f5():
    return "a" in "apple"


print(f1())
print(f2())
print(f3())
print(f4())
print(f5())


# ========= 3. Boolean-ФУНКЦИИ В IF =========

def check():
    return False

def is_even(n):
    return n % 2 == 0

def has_length():
    return len("hi") > 0

def test():
    return 5 > 10

def login():
    return True


if check():
    print("YES")
else:
    print("NO")

if is_even(4):
    print("4 is even")

if has_length():
    print("String is not empty")

if test():
    print("Test passed")
else:
    print("Test failed")

if login():
    print("Access granted")


# ========= 4. isinstance() — ВСТРОЕННАЯ Boolean-ФУНКЦИЯ =========

print(isinstance(5, int))
print(isinstance("hello", str))
print(isinstance(3.14, float))
print(isinstance([1, 2], list))
print(isinstance(True, bool))
