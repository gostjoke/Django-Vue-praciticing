from django.test import TestCase

# Create your tests here.
class dog:
    def __init__(self, weight: float, hight: float):
        self.weight = weight
        self.hight = hight

    def get_hight(self, hight):
        self.hight = hight
        print("pig")

class dog2(dog):

    def __init__(self, weight: float, hight: float):
        super().__init__(weight, hight)

    def get_hight(self, hight: float):
        self.hight = hight
        print("dog")
        return self.hight
    
a = dog2(2, 5)
print(a.get_hight(3))