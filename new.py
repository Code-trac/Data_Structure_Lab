class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Linkedlist:
    def __init__(self):
        self.head = None
    
    def create(self):
        # create a circular list 10 -> 20 -> 30 -> 40 -> (back to 10)
        n1 = Node(10)
        n2 = Node(20)
        n3 = Node(30)
        n4 = Node(40)
        n5 = Node(50)
        n1.next = n2
        n2.next = n3
        n3.next = n4
        n4.next = n5
        n5.next = None
        self.head = n1        # <-- important: keep head pointing to the list
    '''
    def insert_at_begin(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            return
        
        ptr = self.head
        while ptr.next != self.head:
            ptr = ptr.next
        ptr.next = new_node
        new_node.next = self.head
        self.head = new_node
    
    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            return
        
        ptr = self.head
        while ptr.next != self.head:
            ptr = ptr.next
        ptr.next = new_node
        new_node.next = self.head

    def insert_at_position(self, data, position):
        new_node = Node(data)
        if position == 0:
            self.insert_at_begin(data)
            return
        
        ptr = self.head
        count = 0
        while count < position - 1 and ptr.next != self.head:
            ptr = ptr.next
            count += 1
        
        new_node.next = ptr.next
        ptr.next = new_node

    
    def display(self):
        if self.head is None:
            print("List is empty")
            return
        ptr = self.head
        while True:
            print(ptr.data, end=" -> ")
            ptr = ptr.next
            if ptr == self.head:
                break
        print()
    
    '''
    
    def display(self):
        if self.head is None:
            print("List is empty")
            return
        ptr = self.head
        out = []
        while True:
            out.append(str(ptr.data))
            ptr = ptr.next
            if ptr == self.head:
                break
        print(" -> ".join(out) + " -> (back to head)")
    
    def find_middle(self):
        if self.head is None:
            print("List is empty")
            return

        slow_ptr = self.head
        fast_ptr = self.head

        while (fast_ptr.next != self.head) and (fast_ptr.next.next != self.head):
            slow_ptr = slow_ptr.next
            fast_ptr = fast_ptr.next.next

        print("The middle element is:", slow_ptr.data)

ll = Linkedlist()
ll.create()
ll.display()        
ll.find_middle()    