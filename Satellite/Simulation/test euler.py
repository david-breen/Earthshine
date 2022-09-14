import numpy as np 
a = np.array([[1,2,3],[4,5,6]]) 


print(a)



print(np.append(a, [7,8,9]))



print(np.append(a, [[7,8,9]],axis = 0))



print(np.append(a, [[5,5,5],[7,8,9]],axis = 1))