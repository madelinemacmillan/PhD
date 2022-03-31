struct Person()
    name::String
    age::Int64
end


function my_name(Person)
    print("Hello my name is " + self.name)
end


p1 = Person("John", 36)
p1.myfunc()