#task1
import math

degree = 15
radian = math.radians(degree)

print(f"Input degree: {degree}")
print(f"Output radian: {radian:.6f}")

#task2
height = 5
base1 = 5
base2 = 6

area = ((base1 + base2) / 2) * height

print(f"Height: {height}")
print(f"Base, first value: {base1}")
print(f"Base, second value: {base2}")
print(f"Expected Output: {area}")

#task3
import math

n_sides = 4
side_length = 25

# Formula: (n * s^2) / (4 * tan(pi/n))
area = (n_sides * side_length**2) / (4 * math.tan(math.pi / n_sides))

print(f"Input number of sides: {n_sides}")
print(f"Input the length of a side: {side_length}")
print(f"The area of the polygon is: {int(area)}")


#task4
base = 5
height = 6

area = float(base * height)

print(f"Length of base: {base}")
print(f"Height of parallelogram: {height}")
print(f"Expected Output: {area}")

