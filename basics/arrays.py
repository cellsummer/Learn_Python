import numpy as np

# working with arrays
x = [1, 2, 3.5, 4, 5.6]
print("x is" + str(x))

# when referencing, it doesn't include the last index
print("x[0:2] is " + str(x[0:2]))  # showing [1, 2]

# reference negative index
print("the last element of x is " + str(x[-1]))  # showing 5.6

# plus operator meaning concatenate
print("x + x is " + str(x + x))

# numpy arrays (it is the better choice if working with numeric arrays)
y = np.array([1, 2, 3.5, 4, 5.6])
print("y is " + str(y))
# plus operator here means add
print("y + y is " + str(y + y))
print("y * y is " + str(y * y))
print("the mean of y is " + str(np.mean(y)))

# initialize arrays
# y = np.ones(10)
# z = np.ones((2, 3))

# numpy arrays with column names and record number
