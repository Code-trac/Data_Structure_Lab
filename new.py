class BookNode:
    def __init__(self, BookId, Title, Author, Status="avail"):
        self.BookId = BookId
        self.Title = Title
        self.Author = Author
        self.Status = Status
        self.next = None

class Stack:
    def __init__(self):
        self.items = []
    def push(self, ttype, bid):
        self.items.append((ttype, bid))
    def pop(self):
        if not self.items:
            return None
        return self.items.pop()
    def empty(self):
        return len(self.items) == 0
    def view(self):
        if not self.items:
            print("no trans")
            return
        print("recent:")
        for t, b in reversed(self.items):
            print(f"{t} {b}")

class BookList:
    def __init__(self):
        self.head = None

    def insertBook(self, id, title, author):
        if self.searchBook(id):
            print("exists")
            return
        n = BookNode(id, title, author)
        if self.head is None:
            self.head = n
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = n
        print("added")

    def delete_book(self, id):
        if self.head is None:
            print("empty")
            return
        cur = self.head
        prev = None
        while cur and cur.BookId != id:
            prev = cur
            cur = cur.next
        if cur is None:
            print("not found")
            return
        if prev is None:
            self.head = cur.next
        else:
            prev.next = cur.next
        print("deleted")

    def searchBook(self, id):
        cur = self.head
        while cur:
            if cur.BookId == id:
                return cur
            cur = cur.next
        return None

    def displayBooks(self):
        if self.head is None:
            print("no books")
            return
        print("ID\tTitle\tAuthor\tStatus")
        cur = self.head
        while cur:
            print(f"{cur.BookId}\t{cur.Title[:12]}\t{cur.Author[:10]}\t{cur.Status}")
            cur = cur.next

    def issue_book(self, id, st: Stack):
        b = self.searchBook(id)
        if not b:
            print("nf")
            return
        if b.Status == "iss":
            print("already")
            return
        b.Status = "iss"
        st.push("issue", id)
        print("issued")

    def returnBook(self, id, st: Stack):
        b = self.searchBook(id)
        if not b:
            print("nf")
            return
        if b.Status == "avail":
            print("already avail")
            return
        b.Status = "avail"
        st.push("return", id)
        print("returned")

    def undoTrans(self, st: Stack):
        if st.empty():
            print("nothing")
            return
        last = st.pop()
        if last is None:
            print("err")
            return
        ttype, bid = last
        b = self.searchBook(bid)
        if not b:
            print("book gone")
            return
        if ttype == "issue":
            b.Status = "avail"
            print("undo issue")
        elif ttype == "return":
            b.Status = "iss"
            print("undo return")
        else:
            print("unknown")

def main():
    lib = BookList()
    st = Stack()
    while True:
        print("\n1.add 2.del 3.search 4.show 5.issue 6.ret 7.undo 8.trans 9.exit")
        ch = input("cho: ").strip()
        if ch == "1":
            try:
                bid = int(input("id: ").strip())
            except:
                print("bad id"); continue
            t = input("title: ").strip()
            a = input("author: ").strip()
            lib.insertBook(bid, t, a)
        elif ch == "2":
            try:
                bid = int(input("id: ").strip())
            except:
                print("bad"); continue
            lib.delete_book(bid)
        elif ch == "3":
            try:
                bid = int(input("id: ").strip())
            except:
                print("bad"); continue
            b = lib.searchBook(bid)
            if b:
                print(b.BookId, b.Title, b.Author, b.Status)
            else:
                print("not found")
        elif ch == "4":
            lib.displayBooks()
        elif ch == "5":
            try:
                bid = int(input("id: ").strip())
            except:
                print("bad"); continue
            lib.issue_book(bid, st)
        elif ch == "6":
            try:
                bid = int(input("id: ").strip())
            except:
                print("bad"); continue
            lib.returnBook(bid, st)
        elif ch == "7":
            lib.undoTrans(st)
        elif ch == "8":
            st.view()
        elif ch == "9":
            print("bye"); break
        else:
            print("choose")

if __name__ == "__main__":
    main()
