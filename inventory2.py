
'''
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def insert_from_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
    def insert_from_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                print("Item", {key}, "found in inventory")
            current = current.next
        return False
    
    def insert_from_a_given_node(self, prev_node, data):
        new_data = Node(data)
        new_data.next = prev_node.next
        prev_node.next = new_data
    
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

ll = LinkedList()

while True:
    print("\nMenu:")
    print("1. Insert item from end")
    print("2. Insert item from beginning")
    print("3. Insert item after a given node")
    print("4. Search for an item")
    print("5. Display inventory")
    print("6. Exit")
    choice = input("Enter your choice: ")
    
    
    if choice == '1':
        item = input("Enter item to insert from end: ")
        ll.insert_from_end(item)
        print(f"Inserted {item} from end.")
    elif choice == '2':
        item = input("Enter item to insert from beginning: ")
        ll.insert_from_beginning(item)
        print(f"Inserted {item} from beginning.")
    elif choice == '3':
        prev_item = input("Enter the item after which to insert: ")
        new_item = input("Enter item to insert: ")
        current = ll.head
        while current and current.data != prev_item:
            current = current.next
        if current is None:
            print(f"Item {prev_item} not found in inventory.")
        else:
            ll.insert_from_a_given_node(current, new_item)
            print(f"Inserted {new_item} after {prev_item}.")
    elif choice == '4':
        item = input("Enter item to search for: ")
        found = ll.search(item)
        if found:
            print(f"{item} found in inventory.")
        else:
            print(f"{item} not found in inventory.")
    elif choice == '5':
        print("Inventory items:")
        ll.display()
    elif choice == '6':
        print("Exiting")
        break
    else:
        print("Invalid choice. Please try again.")


'''

    
#Implementing the ticketing system using q

q = []
r = -1
f = -1

def enque(item):
    global r
    global f
    r+=1
    q.append(item)
    print(f"Ticket {item} added to the queue")

def deque():
    global r
    global f
    if f > r or f == -1:
        print("No tickets in the queue")
    else:
        item = q[f]
        f+=1
        print(f"Ticket {item} processed and removed from the queue")

def display():
    global r
    global f
    if f > r or f == -1:
        print("No tickets in the queue")
    else:
        print("Current tickets in the queue:")
        for i in range(f, r+1):
            print(q[i])

def elements_in_queue():
    global r
    global f
    if f > r or f == -1:
        print("No tickets in the queue")
    else:
        count = r - f + 1
        print(f"Number of tickets in the queue: {count}")

def isfull():
    global r
    global f
    if r - f + 1 == len(q):
        print("Queue is full")
    else:
        print("Queue is not full")

while True:
    print("\nMenu:")
    print("1. Add Ticket")
    print("2. Process Ticket")
    print("3. Display Tickets")
    print("4. Number of Tickets")
    print("5. Is Queue Full?")
    print("6. Exit")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        ticket = input("Enter ticket ID to add: ")
        enque(ticket)
    elif choice == '2':
        deque()
    elif choice == '3':
        display()
    elif choice == '4':
        elements_in_queue()
    elif choice == '5':
        isfull()
    elif choice == '6':
        print("Exiting")
        break
    else:
        print("Invalid choice. Please try again.")


    

