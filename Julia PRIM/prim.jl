##mmacmill

#define different objective functions!
import DataFrames

abstract type prim_ end

struct prim <: prim_
    x
    y
    threshold::Float64
    threshold_type::String
    obj_func::Function = lenient1
    peel_alpha::Float64 = 0.05
    paste_alpha::Float64 = 0.05
    mass_min::Float64 = 0.05
    include::Array 
    exclude::Array
    coi #needs to be String or Array
end

function initialize(prim)
    if prim.x isa DataFrame
        x = Matrix(prim.x)
    elseif prim.x isa maskedarray
    else
        prim.x = Matrix(DataFrame(prim.x))
    end

    if prim.y isa String
        key=prim.y
        prim.y=prim.x[key]

        if @isdefined(exclude)==true
            exclude = push!(exclude,key)
        else
            exclude=[key]
        end
    elseif prim.y isa Function
        fun = prim.y
        prim.y = mapslices(fun,0,prim.x)
    elseif prim.y isa DataFrame || prim.y isa Array
        prim.y = prim.y.values
    elseif prim.y isa maskedarray
    else
        prim.y = Array(prim.y)
    end

    if @isdefined(prim.include) == true && prim.include isa String
        prim.include = [prim.include]
    end
    if @isdefined(prim.exclude) == true && prim.exclude isa String
        prim.exclude = [prim.exclude]
    if @isdefined(prim.include) == true
        if prim.include isa String
            prim.include = [prim.include]
        end
        drop_names = s
        prim.x = 







    


