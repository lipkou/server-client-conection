class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def opis(self):
        return "Animal: name=" + self.name + ", age=" + str(self.age)

    def is_equal(self, other):
        return isinstance(other, Animal) and self.name == other.name and self.age == other.age


class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year

    def opis(self):
        return "Car: model=" + self.model + ", year=" + str(self.year)

    def is_equal(self, other):
        return isinstance(other, Car) and self.model == other.model and self.year == other.year


class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def opis(self):
        return "Book: title=" + self.title + ", pages=" + str(self.pages)

    def is_equal(self, other):
        return isinstance(other, Book) and self.title == other.title and self.pages == other.pages