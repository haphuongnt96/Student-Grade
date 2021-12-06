from StudentGrades.models import Student, Course, Grade

class Node:
    def __init__(self, info):
        self.info = info
        self.next = None
        self.prev = None
        self.key = None

class LRUCache:
    def __init__(self):
        self.max_len = 10
        self.hash_table = {}
        self.tail = None
        self.head = None

    def get(self, key, data):
        if key in self.hash_table:
            # Move node to head
            if self.head.key != key:
                n = self.deleteNode(self.hash_table[key])
                self.insert(n)
            # return node
        else:
            # Check condition to see if len(hash_table > len(max_len))
            # Y --> Evict tail node and remove from hash_table
            if len(self.hash_table) >= len(self.max_len):
                self.evict()
            # Insert node to head
            n = Node(data)
            self.insert(n)
        # return node
        self.head = n
        return n

    def evict(self):
        # Delete from hash table
        self.hash_table.del(self.tail.key)

        # Evict least recently used cache
        n = self.tail.next
        self.tail.next = None
        self.tail = n
        self.tail.prev = None

    def insert(self, node):
        # Insert node to linked list head
        self.head.next = node
        node.prev = self.head
        self.head = node
    
    def deleteNode(self, node):
        # Unsert node from linked list
        n1 = node.prev
        n2 = node.next
        n1.next = n2
        n2.prev = n1
        return node