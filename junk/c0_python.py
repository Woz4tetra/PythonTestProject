import random

def is_sorted(A):
    for index in xrange(len(A) - 1):
        assert(A[index] <= A[index + 1])
    return True

def search(A, x):
    assert(is_sorted(A))
    
    lower = 0
    upper = len(A)
    while(upper - lower >= 1):
        mid = lower + (upper - lower) / 2
        if A[mid] == x: return mid
        elif A[mid] > x: upper = mid
        else:
            assert(A[mid] < x)
            lower = mid + 1
    return -1

def swap(A, index1, index2):
    temp = A[index1]
    A[index1] = A[index2]
    A[index2] = temp

def partition(A, lower, upper, pivot):
    swap(A, lower, pivot)
    left = lower + 1
    right = upper
    
    while(left < right):
        assert(lower + 1 <= left and left <= right and right <= upper)
        if A[left] <= A[lower]:  # lower is the pivot
            left += 1
        else:
            right -= 1
            swap(A, left, right)
    
    assert(left == right)
    swap(A, lower, left - 1)
    return left - 1

def quicksort(A, lower, upper):
    if (upper - lower) <= 1: return
    
    pivot = lower + (upper - lower) / 2
    
    mid = partition(A, lower, upper, pivot)
    quicksort(A, lower, mid)
    quicksort(A, mid + 1, upper)
    
    return A

class Chain(object):
    def __init__(self, data=None):
        self.data = data
        self.next = None
    
    def __str__(self):
        if self.next != None:
            return "[%s]->" % str(self.data)
        else:
            return "[%s]" % str(self.data)

class C0Dict(object):
    def __init__(self, capacity, equiv_fn, hash_fn):
        self.size = 0
        self.capacity = capacity
        self.table = [None] * capacity
        self.equiv_fn = equiv_fn
        self.hash_fn = hash_fn
    
    def is_table_expected_length(self, length):
        return len(self.table) == length
    
    def equiv(self, element1, element2):
        return self.equiv_fn(element1, element2)
    
    def hash(self, element):
        return abs(self.hash_fn(element)) % self.capacity
    
    def is_dict(self):
        return (isinstance(self, C0Dict) and
            self.capacity > 0 and
            self.size >= 0 and
            self.equiv_fn != None and
            self.hash_fn != None and
            self.is_table_expected_length(self.capacity))
    
    def lookup(self, key):
        index = self.hash(key)
        print "lookup: ", index, key
        chain = self.table[index]
        while chain != None:
            assert chain.data != None
            if self.equiv(chain.data, key):
                return chain.data
            
            chain = chain.next
        
        return None
    
    def insert(self, element):
        assert self.is_dict()
        assert element != None
        
        index = self.hash(element)
        print "lookup: ", index, element
        chain = self.table[index]
        while chain != None:
            assert chain.data != None
            if self.equiv(chain.data, element):
                chain.data = element
                return
            chain = chain.next
        
        new_chain = Chain(element)
        new_chain.next = self.table[index]
        self.table[index] = new_chain
        self.size += 1
        
        assert C0Dict.is_dict(self)
        assert element == self.lookup(element)

#length = 10
#A = [random.randint(0, 10) for _ in xrange(length)]
#quicksort(A, 0, length)
#print A
#print length / 2, search(A, length / 2)

class Struct:
    def __init__(self, string, num1, num2):
        self.string = string
        self.num1 = num1
        self.num2 = num2
    
    def __str__(self):
        return "<Struct: %s, %s, %s>" % (self.string, str(self.num1), str(self.num2))

def struct_equiv(struct1, struct2):
    return struct1.string == struct2.string

def struct_hash(struct):
    return hash(hex(id(struct.string)))

key = Struct("something", 0, 0)

c0_dict = C0Dict(10, struct_equiv, struct_hash)

c0_dict.insert(Struct("something", 1, 2))

print c0_dict.lookup(key)
