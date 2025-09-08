"""method overriding"""
class Parent:
    def message(self):
        print("Message from Parent")

class Child(Parent):
    def message(self):
        print("Message from Child")

child = Child()
child.message()

"""function overloading"""
class Calculator:
    def add(self, *args):
        total = 0
        for num in args:
            total += num
        return total

calc = Calculator()
print(calc.add(2, 3))          # Output: 5
print(calc.add(2, 3, 4))       # Output: 9
print(calc.add(1, 2, 3, 4, 5)) # Output: 15

"""Remove even number and double odd number in array of random numbers using list comprehession"""
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = [n * 2 for n in numbers if n % 2 != 0]
print(result)

"""Write a functions to convert tupple to list, list to set, set to tuple."""
def convert_data(data):
    if isinstance(data, tuple):
        return list(data)
    elif isinstance(data, list):
        return set(data)
    elif isinstance(data, set):
        return tuple(data)
    else:
        return "Unsupported data type"

print(convert_data((1, 2, 3)))  # Tuple to List => [1, 2, 3]
print(convert_data([1, 2, 3]))  # List to Set => {1, 2, 3}
print(convert_data({1, 2, 3}))  # Set to Tuple => (1, 2, 3)

"""Write a function that will convert list inside list to dictionary"""
def list_to_dict(lst):
    result = {}
    for key, value in lst:
        result[key] = value
    return result
# Example:
data = [['name', 'Deepak'], ['number', 23], ['class', '10th']]
print(list_to_dict(data))


"""Create a function that will sort the array of string based on the length of string."""
def sort_by_length(strings):
    return sorted(strings, key=lambda s: len(s))

# Example
names = ['deepak', 'aman', 'sam', 'naman', 'mohit']
sorted_names = sort_by_length(names)
print(sorted_names)
