
"""
my_sum receives a list of arguments(args) and return its sum.
"""
def my_sum(*args):
    result = 0

    # Iterating over the Python args tuple
    for x in args:
        result += x
    return result

"""
my_concatenate receives a list of named arguments(kwargs) and return
a single concatenated string
"""
def my_concatenate(**kwargs):
    result = ""
    
    # Iterating over the Python kwargs dictionary
    for arg in kwargs.values():
        result += arg + ' '
    return result.strip()