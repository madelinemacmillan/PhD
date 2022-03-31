using CSV
using DataFrames

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

test_data=DataFrame(CSV.File("test_data.csv"))
test_data=convert(Matrix{Float64}, test_data)

function Prim(prim,box,name)
    PEEL_OPERATIONS = {"object" => categorical_peel,
    "bool" => categorical_peel,
    "int8" => discrete_peel,
    "int16" => discrete_peel,
    "int32" => discrete_peel,
    "int64" => discrete_peel,
    "uint8" => discrete_peel,
    "uint16" => discrete_peel,
    "uint32" => discrete_peel,
    "uint64" => discrete_peel,
    "float16" => real_peel,
    "float32" => real_peel,
    "float64" => real_peel}

PASTE_OPERATIONS = {"object" => categorical_paste,
     "bool" => categorical_paste,
     "int8" => discrete_peel,
     "int16" => real_paste,
     "int32" => real_paste,
     "int64" => real_paste,
     "uint8" => discrete_peel,
     "uint16" => real_paste,
     "uint32" => real_paste,
     "uint64" => real_paste,
     "float16" => real_paste,
     "float32" => real_paste,
     "float64" => real_paste}
     
     #dictionaries to determine which method to use dependent on the dtype


answer=get_quantile(test_data,.25)
print(answer)