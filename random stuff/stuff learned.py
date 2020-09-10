import time
timer = lambda: print('\nExecution time: ' + str(time.process_time_ns()))
while True:
    timer()
    print('Number to use for operation (1-100)')
    try:
        operationNum = int(input('operationNum = '))
        if not 0 < operationNum < 101:
            continue
        break
    except ValueError:
        pass

timer()

print("""
=====
Factorial Recursion
=====
""")
def factorial_recursive(n):
    # Base case: 1! = 1
    if n == 1:
        return 1
    # Recursive case: n! = n * (n-1)!
    else:
        return n * factorial_recursive(n-1)
print(factorial_recursive(operationNum))

timer()

print("""
=====
Binary Recursion
=====
""")
def binary_recursive(n):
    if len(n) == 1:
        print(n[0])
    else:
        binary_recursive(n[:len(n)//2])
        binary_recursive(n[len(n)//2:])
binary_recursive(range(0, operationNum))

timer()

print("""
=====
Tri Recursion
=====
""")
def tri_recursion(k):
    if(k>0):
        result = k+tri_recursion(k-1)
        print(result)
    else:
        result = 0
    return result
tri_recursion(operationNum)

timer()

## [Doesn't work] Old version of Binary search (might be useful later)
#def binarySearchOLD(array, index):
#    try:
#        initialize
#    except NameError:
#        initialize = 1
#        low = 0
#        high = len(array) - 1
#    if not index in array:
#        return -1
#    elif index == array[len(array)//2]:
#        del initialize
#        return (low + high)//2
#    elif index < array[len(array)//2]:
#        high -= len(array)//2 - 1
#        return binarySearchOLD(array[:len(array)//2], index)
#    else:
#        low += len(array)//2 + 1
#        return binarySearchOLD(array[len(array)//2:], index)

## Binary search attempt (working)
#def binarySearch(index, array):
#    def binarysearch_(_i, _a, _s, _e):
#        ## _i is the index variable which item is being looked for inside the _a, the array list.
#        ## _s is the beginning position of array that is not indexed, _e is the ending position.
#        if _i not in _a[_s:_e+1]: # If index is not found in the non-eliminated array, return -1
#            return -1
#        
#        _m = (_s + _e) // 2 ## _m is the middle variable position of start and end.
#        if _i == _a[_m]: ## If index is in middle of non-eliminated array, report back the position of the middle variable
#            return _m
#        elif _i < _a[_m]: ## If the index is less than the middle of the non-eliminated array, change the end variable to the middle variable
#            return binarysearch_(_i, _a, _s, _m)
#        elif _i > _a[_m]: ## If the index is more than the middle of the non-eliminated array, change the start variable to the middle variable
#            return binarysearch_(_i, _a, _m, _e)
#    _r = binarysearch_(index, array, 0, len(array))
#    _m = None
#    return _r
#import string

## Word searching test
#def wordSearch(word, array):
#    _word = word.upper()
#    _array = []
#    for item in array.sort():
#        _array.append(item.upper())
#    _r = binarySearch(_word, _array)
#    return _r
#test = ['Hello', 'What\'s up?', 'Hi']
#print(test)
#print(wordSearch('hello', test))

## Multiple items searching test
#arraylist = []
#for x in range(0,6):
#    arraylist.append(x**2)
#print(arraylist)
#_print = 0
#_printlist = []
#for y in range(0,26):
#    result = (binarySearch(y, arraylist))
#    if not result == -1:
#        if _print == 1:
#            print(str(_printlist[0]) + '-' + str(_printlist[-1]) + ' not present in array.')
#        _printlist = []
#        print(str(y) + ' present in array at index ' + str(result))
#    else:
#        _print = 1
#        _printlist.append(y)


## Clears terminal
#import os
#clear = lambda: os.system('clear')



## https://pyformat.info/ formatting