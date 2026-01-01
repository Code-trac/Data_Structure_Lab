# consider a 1D array of size 10: insert a new element at index 4, delete an element at index 6
size = 10
# sample contents for demonstration (positions 0..6 filled, rest None)
arr = [i+1 if i < 7 else None for i in range(size)]

def insert(x):

    global size, arr
    for i in range(size):
        if arr[i] is None:
            arr[i] = x
            return
    print("Array is full")

def insert_at_index(x, index):

    global size, arr
    if index < 0 or index >= size:
        print("Index out of range")
        return
    if arr[index] is None:
        arr[index] = x
        return

    if arr[-1] is not None:
        print("Array is full, cannot insert at index")
        return
    for i in range(size - 1, index, -1):
        arr[i] = arr[i - 1]
    arr[index] = x

def display():
    global size, arr
    print("Array:", end=" ")
    for i in range(size):
        print(arr[i], end=" ")
    print()

def delete(position):

    global size, arr
    if position < 0 or position >= size:
        print("Position out of range")
        return
    if arr[position] is not None:
        arr[position] = None
    else:
        print("Position is already empty")



print("Before:")
display()

print("Insert 10 at index 4")
insert_at_index(10, 4)
display()

print("Delete element at index 6")
delete(6)
display()

print("Insert 99 (first free slot)")
insert(99)
display()

