aaa = 1
bbb = 2


def fn():
    global a
    print('fn():',a)
    a = 11
    print('fn():',a)

def fn1():
    global a
    print('fn1():', a)
    a = 22
    print('fn1():', a)

class Cls:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b

# a = 1
fn()
print('main:',a)
fn1()