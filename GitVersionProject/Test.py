class Student:
    # Class variable
    school_name = 'ABC School '

    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no


    @classmethod
    def printfunc(self):
        print("Hello")



def main():
    # create first object
    s1 = Student('Emma', 10)
    print(s1.name, s1.roll_no, Student.school_name)
    # access class variable

if __name__ == '__main__':
    main()

