import numpy as np

arr = np.array([[[1,2,3,4,5,6]], [[1,2,3,4,5,6]]])
print(arr.shape)
print(arr)
arr = np.reshape(arr,[2,6])
print(arr.shape)
print(arr)