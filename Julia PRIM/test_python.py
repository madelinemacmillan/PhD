# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:36:06 2022

@author: mmacmill
"""

#methods: functions associated with class
#attributes: data associated with class
#instance variables: data that is unique for each instance (name, email, pay, raise amounts)
#class variables: variables shared among all instances of a class (number of employees, in the employee class)
#class methods: automatically pass the class as the first argument (cls)
#static methods: don't pass anything automatically, important to class, but don't depend on the class or instance
#inheritance: sub classes inherit attributes of original classes and can be modified without translating original class

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def myfunc(self):
    object_age=self.age[3]
    object_age=str(object_age)
    print("Hello my name is " + self.name+" and I am "+ object_age)

p1 = Person("John", [34,35,36,37])
p1.myfunc()

peels=[0.25]
peels.append((4,3))
print(peels)


class Employee:
    num_of_emps=0
    raise_amount=1.04
    
    def __init__(self,first,last,pay):
        self.first=first
        self.last=last
        self.pay=pay
        self.email=first+'.'+last+'@company.com'
        
        Employee.num_of_emps+=1
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
    def apply_raise(self):
        self.pay=int(self.pay * self.raise_amount)
    
    @classmethod
    
    def set_raise_amount(cls,amount):
        cls.raise_amount = amount
        
    @classmethod
    
    def from_string(cls,emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first,last,pay)
    
    @staticmethod
    
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True
    

class Developer(Employee):
    raise_amount=1.15
    
    def __init__(self,first,last,pay,prog_lang):
        super().__init__(first,last,pay)
        self.prog_lang = prog_lang
        
class Manager(Employee):
    
    def __init__(self,first,last,pay, employees=None):
        super().__init__(first,last,pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees
            
    def add_emp(self,emp):
        if emp not in self.employees:
            self.employees.append(emp)
            
    def remove_emp(self,emp):
        if emp in self.employees:
            self.employees.remove(emp)
            
    def print_emp(self):
        for emp in self.employees:
            print('-->',emp.fullname())
        


emp_1=Employee('Maddie','Macmillan',50000)
emp_2=Employee('Test','User',60000)

emp_3='John-Doe-70000'
emp_4='Steve-Smith-30000'
emp_5='Jane-Doe-90000'

dev_1=Developer('John','Doe',30000,'Python')
dev_2=Developer('Jane','Smith',90000,'Java')

man_1=Manager('Caitlin','Murphy',50000, [dev_1,dev_2,emp_1])

print(isinstance(man_1,Manager))
print(issubclass(man_1,Manager))

print(man_1.__dict__)
print(dev_1.pay)
dev_1.apply_raise()
print(dev_1.pay)






