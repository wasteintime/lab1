# "Hello" and 'Hello' are the same string
print("Hello")
print('my')
print("name")
print('is')
print("Zhanibek")

print("You can call me 'Zhan'")
print('or call me "Zhanik"')
print("but don't call me Zheka")
print('so call me please "Zhanik"')
print('or call me simply "Zhan"')

a1 = "My"
print(a1)

a2 = "surname"
print(a2)

a3 = "is"
print(a3)

a4 = "Zhumali"
print(a4)

a5 = "!!!"
print(a5)

a = """one
two 
three 
four"""
print(a) 
print("one" in a)
if "one" in a:
  print("Yes, 'one' is present.")

b1 = """I 
love 
pizza """
print(b1)
print("I" in b1)
if "I" in b1:
  print("Yes, 'I' is present.")

b2 = """I 
love 
pepsi and plov """
print(b2) 
print("pepsi" in b2)
if "cola" in b1:
  print("Yes, 'cola' is present.")

b3 = """I 
love 
cola """
print(b3) 
print("pepsi" in b3)
if "cola" in b1:
  print("Yes, 'cola' is present.")

b4 = """I 
love 
ice cream """
print(b4) 
print("love" in b4)
if "ice" in b1:
  print("Yes, 'ice' is present.")


Z = "Zhanibek"
print(Z[1])
print(Z[2])
print(Z[3])
print(Z[4])
print(Z[5])

for x in "Zhanibek":
  print(x) 
for x in "Zhumali":
  print(x) 
for x in "Love":
  print(x) 
for x in "learning":
  print(x) 
for x in "pp2":
  print(x) 


print(len(a1))
print(len(a2))
print(len(a3))
print(len(a4))
print(len(a5))

txt1 = "Stranger things!"
print("batman" not in txt1)
if "batman" not in txt1:
  print("No, 'batman' is NOT present.")
txt2 = "The best serial is soprano!"
print("movie" not in txt2)
if "movie" not in txt2:
  print("No, 'movie' is NOT present.")
txt3 = "The best movie is inception"
print("Spiderman" not in txt3)
if "Spiderman" not in txt3:
  print("No, 'Spiderman' is NOT present.")
txt4 = "I love listen music"
print("podcasts" not in txt4)
if "podcasts" not in txt4:
  print("No, 'podcasts' is NOT present.")
txt5 = "This is last example"
print("first" not in txt5)
if "first" not in txt5:
  print("No, 'first' is NOT present.")
