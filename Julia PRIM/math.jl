using CSV
using DataFrames
using Statistics

#example looking at pregnancies and age

data=DataFrame(CSV.File("test_data.csv"))
test_data_matrix=Matrix(test_data)
typeof(test_data)

alpha=0.075

bmi=test_data[!,6]
blood_pressure=test_data[!,3]
preg=test_data[!,1]
age=test_data[!,8]
output=test_data[!,9]

###PEELING!!!!!!!!

function quantile(data,alpha)
    n=size(data)[1]
    n+=1
    lq=ceil(n*alpha)
    uq=floor(n*(1-alpha))
    return uq,lq
end

function temp_box(upper,lower,data,in_col)
    #col in the column number
    data=sort!(data, [in_col])
    box_uq=data[Not(upper:size(data)[1]),:]          #this subbox is MISSING the upper quantile
    box_lq=data[Not(1:lower),:]          #this subbox is MISSING the lower quantile
    return box_uq,box_lq
end

function calc_best_box(org_data,box_1_uq,box_1_lq,box_2_uq,box_2_lq,out_col)
    avg_1_uq = mean(box_1_uq[:,out_col])
    avg_1_lq = mean(box_1_lq[:,out_col])
    avg_2_uq = mean(box_2_uq[:,out_col])
    avg_2_lq = mean(box_2_lq[:,out_col])
    avg_org_data = mean(org_data[:,out_col])
    best=max(avg_1_lq,avg_1_uq,avg_2_lq,avg_2_uq,avg_org_data)
    if avg_1_lq==best
        new_box=box_1_lq
    elseif avg_1_uq==best
        new_box=box_1_uq
    elseif avg_2_lq==best
        new_box=box_2_lq
    elseif avg_2_uq==best
        new_box=box_2_uq
    elseif avg_org_data==best
        new_box=org_data
        println("The original box of this iteration was the best, PRIM should stop here")
    else
        print("Error with identifying best new box")
    end
    if mean(new_box[:,out_col]) > mean(data[:,out_col])
        new_box=new_box
    elseif mean(new_box[:,out_col]) <= mean(data[:,out_col])
        new_box=data
    else
        print("Error with determining whether the mean is greater or lower)")
    end
    return new_box
end

function coverage(box,n)
    n_b=size(box)[1]
    beta=n_b/n
    return beta
end


function peeling_iteration(data,in_1,in_2,out,alpha,beta)            #in_1 and in_2 are the numerical value of the column number of the input variables of interest
    n=size(data)[1]
    x=1
    box_beta=beta
    mean_=mean(data[:,out])
    box_mean=mean_
    println(mean_)
    new_box=0
    old_box=0
    size_new=1
    size_old=0
    while (box_beta>=beta || box_mean>=mean_) && size_old !=size_new
        if x==1 #for the first iteration, the data and new box are the same
            uq,lq=quantile(data,alpha)                            #quantile doesn't change based on values
            box_uq_1,box_lq_1 = temp_box(uq, lq, data, in_1)        #for pregnancies
            box_uq_2,box_lq_2 = temp_box(uq, lq, data, in_2)            #for age

            old_box=data
            new_box=calc_best_box(data, box_uq_1, box_lq_1, box_uq_2, box_lq_2, out)
            box_beta=coverage(new_box,n)
            x+=1
            box_mean=mean(new_box[:,out])
            size_new=size(new_box)[1]
            size_old=size(old_box)[1]
        else
        end
        
        if x != 1
            uq,lq=quantile(new_box,alpha)                            #quantile doesn't change based on values
            box_uq_1,box_lq_1 = temp_box(uq, lq, new_box, in_1)        #for pregnancies
            box_uq_2,box_lq_2 = temp_box(uq, lq, new_box, in_2)            #for age

            old_box=new_box
            new_box=calc_best_box(new_box, box_uq_1, box_lq_1, box_uq_2, box_lq_2, out)
            box_beta=coverage(new_box,n)
            box_mean=mean(new_box[:,out])
            x+=1
            size_new=size(new_box)[1]
            size_old=size(old_box)[1]
        else
        end
    end
    return new_box,box_mean,box_beta,old_box
end

#peel ends here

###PASTING!!!!!!!!


prim,box_mean,box_beta,old=peeling_iteration(data,1,8,9,0.08,0.08)

