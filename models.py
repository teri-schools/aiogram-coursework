class Person:
    def __init__(self):
        self.age = 0
        self.name = ""

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age

    def info(self):
        return f"Person: {self.name}, Age: {self.age}"


class Kavun:
    def __init__(self):
        self.weight = 0
        self.price = ""

    def set_weight(self, weight):
        self.weight = weight
        self.price = self.weight * 10

    def get_weight(self):
        return self.weight

    def get_price(self):
        return self.price

    def info(self):
        return f"Kavun: {self.weight} kg, Price: {self.price} bitkoins"
