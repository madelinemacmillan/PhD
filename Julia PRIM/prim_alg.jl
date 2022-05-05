#A class in python is replaced by a combination of structs and methods
import DataFrames

abstract type prim_ end

mutable struct prim <: prim_
    x
    y
    threshold::Float64 = None
    threshold_type::String = ">"
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
        x = Matrix(DataFrame(prim.x))
    end

    if prim.y isa String
        key=prim.y
        y=x[key]

        if @isdefined(prim.exclude)==true
            prim.exclude = push!(prim.exclude,key)
        else
            prim.exclude=[key]
        end
    elseif prim.y isa Function
        fun = prim.y
        y = mapslices(fun, 0, x) #potentially re-eval!
    elseif prim.y isa DataFrame || prim.y isa Array
        y = prim.y.values
    elseif prim.y isa maskedarray
    else
        y = Array(prim.y)
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

        drop_names = setdiff(Set(x),Set(include))  #executed differently here than how it was performed in python!
        for i in drop_names
            for j in x
                if i==j
                    delete!(x,j)
                    return x
                end
            end
        end
    end
    if @isdefined(prim.exclude) == true
        if prim.exclude isa String
            exclude=[prim.exclude]
        end

        drop_names=set(exclude)

        for i in drop_names
            for j in x
                if i==j
                    delete!(x,j)
                    return x
                end
            end
        end

        if @isdefined(prim.threshold)
            if prim.threshold isa Function
                y = mapslices(threshold, 0, y) #potentially re-eval!
            else
                new=[]
                if prim.threshold_type == "<"
                    for i in y
                        if i < prim.threshold
                            push!(new,"true")
                        else
                            push!(new,"false")
                            return new
                        end
                    end
                elseif prim.threshold == "<="
                    for i in y
                        if i <= prim.threshold
                            push!(new,"true")
                        else
                            push!(new,"false")
                            return new
                        end
                    end
                elseif prim.threshold == ">"
                    for i in y
                        if i > prim.threshold
                            push!(new,"true")
                        else
                            push!(new,"false")
                            return new
                        end
                    end
                elseif prim.threshold == ">="
                    for i in y
                        if i >= prim.threshold
                            push!(new,"true")
                        else
                            push!(new,"false")
                            return new
                        end
                    end
                end
            end
        end
    end
        #validating inputs!
    if length(size(y)) > 1
        error("y is not a 1-d array")
    end

    unique_y=unique(y)

    if length(unique_y) >2
        error("y must contain only two values-- 0/1 or False/True")
    end
    
    #omitted error in lines 210-217
    prim=Dict()
    
    prim.x=x
    prim.y=y
    prim.paste_alpha = paste_alpha
    prim.peel_alpha = peel_alpha
    prim.mass_min = mass_min
    prim.threshold = threshold 
    prim.threshold_type = threshold_type
    prim.obj_func = obj_func

    prim.yi = Array(0:size(y)[1])
    prim.n = size(prim.y)[1]
    prim.t_coi = prim.determine_coi(self.yi)    ###determine_coi defined later
    prim._box_init = make_box(prim.x)       ###make box defined later
    prim._boxes = []
    prim._update_yi_remaining()     ###update yi remaining defined later

    prim(:prim_x=>x,:prim_y=>y,:prim_paste_alpha=>paste_alpha,:prim_peel_alpha=>peel_alpha,:prim_mass_min=>mass_min,
    :prim_threshold=>prim.threshold,:prim_threshold_type=>prim.threshold_type,:prim_obj_func=prim.obj_func,:prim_yi=>prim.yi)
    return prim

#function stats(prim)

function limits(prim)
    for box in prim._boxes
        box_lims=[prim.box._box_lims[prim.box._cur_box]]
    end
    if @isdefined(prim.box_lims)==false
        box_lims = [prim._box_init]
    else 
        if 
        compared=compare(box_lims[-1],prim._box_init)


        

