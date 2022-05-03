using CSV
using DataFrames
using DelimitedFiles


function get_quantile(data,quantile)
    ##compuates the quantile of the dataset, both of which are inputs
    @assert(quantile > 0)
    @assert(quantile < 1)

    ##if the data is a maskedarray, compress the data

    data=sort(data)

    i=(length(data)-1)*quantile
    index_lower=Int(floor(i))
    index_upper=Int(ceil(i))

    value = 0

    if quantile > 0.5
        while (data[index_lower] == data[index_upper] && index_lower>0)
            index_lower-= 1

        value = (data[index_lower]+data[index_upper])/2
        end
    else
        # lower
        while (data[index_lower] == data[index_upper] && (index_upper<length(data)-1))
            index_upper += 1
                
        value = (data[index_lower]+data[index_upper])/2
        end
    return value
    end
end

function real_peel(prim,box,name)
    #performs a peel operation on a real-valued column
    x=prim.x[box.yi][name]
    peels=[]
    for direction in ["upper","lower"]
        if isnan(x)
           return []
        else
            peel_alpha=prim.peel_alpha
            index=0

            if direction == "upper"
                peel_alpha=1-peel_alpha
                index=1

            box_peel = get_quantile(x,peel_alpha)

            end

            if direction == "lower"
                logical = x >= box_peel
                indices=box.yi[logical]

            elseif direction == "upper"
                logical = x <= box_peel
                indices = box.yi[logical]
        
            temp_box=copy(deepcopy(box._box_lims[-1]))
            temp_box[name][index] = box_peel
            append!(box_peel,(indices,temp_box)) ##Currently appending the () as a part of the array, not as a distinct tuple element within the array

            else
                return []

            end


        return peels

        end
    end
end

function real_paste(prim, box, name)
    #performs paste operation on a real-valued column
    #pastes to upper and lower dimension of given column
    #returns two new candidate boxes

    x = prim.x[prim.yi_remaining]
    limits=box._box_lims[-1]        #defined in PRIM_box
    init_limits = prim._box_init   #this is defined in PRIM_alg

    pastes=[]

    for direction in ["lower","upper"]
        box_paste = copy(limits)
        paste_box=copy(limits)

        if direction == "upper"
            paste_box[name][0]=paste_box[name][1]
            paste_box[name][1]=init_limts[name][1]

            indices=in_box(x,paste_box)  #defined in scenario discovery

            data=x[indices][name]

            if data.shape[0] > 0
                paste_value = get_quantile(data, prim.paste_alpha)
                
            else
                paste_value=init_limits[name][1]

            end
            @assert(paste_value >= limits[name][1])

        elseif direction == "lower"
            paste_box[name][0] = init_limits[name][0]
            paste_box[name][1] = box_paste[name][0]
            
            indices = in_box(x, paste_box)  #defined in scenario discovery
            data = x[indices][name]

            if data.shape[0] > 0
                paste_value = get_quantile(data, 1-prim.paste_alpha)
            else
                paste_value = init_limits[name][0]
            
            end

            @assert(paste_value <= limits[name][0])

        dtype=dump(box_paste[name][0])
        end
        if dtype == Int32
            paste_value=trunc(paste_value)

        end

        if direction == "upper"
            box_paste[name][1]=paste_value
        else
            box_paste[name][0]=paste_value
        end

        indices=in_box(x,box_paste)      #defined in scenario discovery
        indices=prim.yi_remaining[indices]

        push!(pastes,(indices,box_paste))
    end
    return pastes
end

#test_data=DataFrame(CSV.File("test_data.csv"))
#test_data=Matrix(test_data)
#typeof(test_data)


#answer=get_quantile(test_data,q)
#print(answer)