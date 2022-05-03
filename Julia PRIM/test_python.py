# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:36:06 2022

@author: mmacmill
"""
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