abstract type AbstractCar end



mutable struct SportsCar <: AbstractCar  #the notation <: is indicate of a SUB type. In this case, a SportsCar is a subtype of AbstractCar
    color::String
end

struct BaseCar <: AbstractCar
    color::String
end

struct Truck <: AbstractCar
    color::String
end



function honk(car::AbstractCar) #acts as a catch all for all other sub types
    println("honk")
end

function honk(car::SportsCar)
    println("sporty honk")
    c="blue"
    car.color=c
    car.wheels=4
end

function honk(car::BaseCar)
    println("base honk")
end



sportscar=SportsCar("red")
println(sportscar.color)
honk(sportscar)
println(sportscar.color)

truck=Truck("red")
honk(truck)

