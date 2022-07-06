class Test:
    def __init__(self):
        print("Test OK!")
        #print(self.a)
    def call(self):
        print("You call the Test class")


class SuperTest(Test):
    def __init__(self):
        print("This is SuperTest class")
        super().__init__()
        print("SuperTest end")
        print("------------------")
    def call(self):
        super().call()
        print("You call the SuperTest class")

test1 = SuperTest()
test1.call()
