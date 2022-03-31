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
    print("Hello my name is " + self.name)

p1 = Person("John", 36)
p1.myfunc()