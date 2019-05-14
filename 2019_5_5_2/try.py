class A(object):

    def __init__(self):
        self.A = "A"
        print (self.A)
        super(A, self).__init__()

class B(object):

    def __init__(self):
        self.B = "B"
        print (self.B)
        super(B, self).__init__()

class C(A, B):

    def __init__(self):
        self.C = "C"
        print (self.C)
        super(C, self).__init__()

if __name__ == '__main__':
    print ("With super() in parent __init__():")
    c = C()
    print (c.__dict__)
    print (C.__mro__)