#consider a 1D array of size 10, insert a new element at index 4, delete an element at index 6

size = 10
arr = [None]*size

def insert(x):
    global size, arr
    for i in range(size):
        if arr[i] == None:
            arr[i] = x
        else:
            print("Array is full")
        return
    
def insert_at_index(x, index):
    