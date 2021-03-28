from dep1 import Cls
import dep2

class A(Cls):
    def fn(self):
        self.dep_fn()

def func2():
    dep2.func()

a = A()
a.fn()
func2()
