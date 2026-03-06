#task1
import re
def match_ab_zero(text):
    pattern = r'^ab*$'
    return bool(re.match(pattern, text))

# Test: "a", "ab", "abbbb" -> True | "b", "ba" -> False

#task2
import re
def match_ab_range(text):
    pattern = r'ab{2,3}'
    return bool(re.search(pattern, text))

#task3
import re
def find_snake_sequences(text):
    pattern = r'[a-z]+_[a-z]+'
    return re.findall(pattern, text)

#task4
import re
def find_capitalized(text):
    pattern = r'[A-Z][a-z]+'
    return re.findall(pattern, text)

#task5
import re
def start_a_end_b(text):
    pattern = r'a.*b$'
    return bool(re.match(pattern, text))

#task6
import re
text = "Python Exercises, or RegEx. Testing"
print(re.sub(r"[ ,.]", ":", text))
# Output: Python:Exercises::or:RegEx::Testing


#task7
import re
def snake_to_camel(text):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)

# "hello_world" -> "helloWorld"


#task8
import re
text = "PythonExercisesAndSolutions"
print(re.findall(r'[A-Z][^A-Z]*', text))
# Output: ['Python', 'Exercises', 'And', 'Solutions']


#task9
import re
def insert_spaces(text):
    return re.sub(r'(\w)([A-Z])', r'\1 \2', text)

# "PythonExercises" -> "Python Exercises"


#task10
import re
def camel_to_snake(text):
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()

# "CamelCaseString" -> "camel_case_string"
