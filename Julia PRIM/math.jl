using CSV
using DataFrames
using Statistics

#example looking at pregnancies and age

data=DataFrame(CSV.File("test_data.csv"))
paste_data=DataFrame(CSV.File("test_paste.csv"))
#test_data_matrix=Matrix(test_data)
#typeof(test_data)

function quantile(data,alpha)
    n=size(data)[1]
    n+=1
    lq=ceil(n*alpha)
    uq=floor(n*(1-alpha))
    return uq,lq
end

function temp_small_box(upper,lower,data,in_col)
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
        #println("The original box of this iteration was the best, PRIM should stop here")
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
    #println(mean_)
    new_box=0
    old_box=0
    size_new=1
    size_old=0
    while (box_beta>=beta || box_mean>=mean_) && size_old !=size_new
        if x==1 #for the first iteration, the data and new box are the same
            uq,lq=quantile(data,alpha)                            #quantile doesn't change based on values
            box_uq_1,box_lq_1 = temp_small_box(uq, lq, data, in_1)        #for pregnancies
            box_uq_2,box_lq_2 = temp_small_box(uq, lq, data, in_2)            #for age

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
            box_uq_1,box_lq_1 = temp_small_box(uq, lq, new_box, in_1)        #for pregnancies
            box_uq_2,box_lq_2 = temp_small_box(uq, lq, new_box, in_2)            #for age

            old_box=copy(new_box)
            new_box=calc_best_box(old_box, box_uq_1, box_lq_1, box_uq_2, box_lq_2, out)
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
function addition(data,alpha)
    n=size(data)[1]
    b=ceil(n*alpha)
    return b
end

function temp_big_box_up(upper,org_data,box_data,in_col)
    box=copy(box_data)
    box=sort!(box, [in_col])
    org_data=sort!(org_data,[in_col])
    org_n=size(org_data)[1]
    org_range=(1:org_n)
    starting_row=0
    for i in org_range
        test_row=org_data[i,:]
        if test_row==box[1,:]
            starting_row=i
            starting_row=Int64(starting_row)
        else
        end
    end
    a=Int64(starting_row-upper)  #a should be lower, because it is moving UP in the dataset
    if a<=0
        a=1
    else
    end
    to_add=DataFrame(org_data[a:starting_row,:])
    box_up=append!(box,to_add)
    box_up=sort!(box_up, [in_col])
    return box_up
end

function temp_big_box_down(lower,org_data,box_data,in_col)
    box=copy(box_data)
    box=sort!(box, [in_col])
    org_n=size(org_data)[1]
    l=size(box)[1]
    org_range=(1:org_n)
    starting_row=0
    for i in org_range
        test_row=org_data[i,:]
        if test_row==box[l,:]
            starting_row=i
            starting_row=Int64(starting_row)
        else
        end
    end
    a=Int64(starting_row+lower)
    if a>=size(org_data)[1]
        a=size(org_data)[1]
        a=Int64(a)
    else
    end
    to_add=DataFrame(org_data[starting_row:a,:])
    box_down=append!(box,to_add)
    box_down=sort!(box_down, [in_col])
    return box_down
end

function pasting_iteration(org_data,starting_box_data,in_1,in_2,out,alpha,beta)            #in_1 and in_2 are the numerical value of the column number of the input variables of interest
    n=size(data)[1]
    
    box_beta=beta
    box_mean=mean(starting_box_data[:,out])
    mean_=mean(starting_box_data[:,out])

    x=1
    new_box=0
    old_box=0
    size_new=1
    size_old=0
    box_data=0

    while (box_beta>=beta || box_mean>=mean_) && size_old !=size_new
        if x==1
            a = addition(starting_box_data,alpha)                            #quantile doesn't change based on values
            box_up_1 = temp_big_box_up(a, org_data, starting_box_data, in_1)        #for pregnancies
            box_up_2 = temp_big_box_up(a, org_data, starting_box_data, in_2)            #for age
            box_down_1 = temp_big_box_down(a, org_data, starting_box_data, in_1)
            box_down_2 = temp_big_box_down(a, org_data, starting_box_data, in_2) 
            
            old_box = copy(starting_box_data)
            new_box = calc_best_box(old_box, box_up_1, box_up_2, box_down_1, box_down_2, out)
            box_beta = coverage(new_box,n)
            box_mean = mean(new_box[:,out])
            size_new = size(new_box)[1]
            size_old = size(old_box)[1]
            box_data = copy(new_box)
            
            x += 1
        else
            a = addition(box_data,alpha)                            #quantile doesn't change based on values
            box_up_1 = temp_big_box_up(a, org_data, box_data, in_1)        #for pregnancies
            box_up_2 = temp_big_box_up(a, org_data, box_data, in_2)            #for age
            box_down_1 = temp_big_box_down(a, org_data, box_data, in_1)
            box_down_2 = temp_big_box_down(a, org_data, box_data, in_2) 
            
            old_box = copy(box_data)
            new_box = calc_best_box(old_box, box_up_1, box_up_2, box_down_1, box_down_2, out)
            box_beta = coverage(new_box,n)
            box_mean = mean(new_box[:,out])
            size_new = size(new_box)[1]
            size_old = size(old_box)[1]
            
            box_data=copy(new_box)
            x += 1   
        end     
    end
    return new_box,box_mean,box_beta,old_box
end


###PRIM ITERATION, PASTING AND PEELING
function prim_iteration(data, in_1, in_2, out, alpha, beta)
    x = 1

    new_box_peel = 1
    new_box_paste = 0
    box_mean = 0
    box_beta = 0
    old = 0
    final_box = 0

    if new_box_peel != new_box_paste
        while new_box_peel != new_box_paste
            if x==1 
                new_box_peel,box_mean,box_beta,old = peeling_iteration(data, in_1, in_2, out, alpha, beta)
                new_box_paste,box_mean,box_beta,old = pasting_iteration(data, new_box_peel, in_1, in_2, out, alpha, beta)
                
                println(x)
                x += 1
                #println(new_box_peel)
                #println(new_box_paste)
                
            else
                new_box_peel,box_mean,box_beta,old = peeling_iteration(new_box_paste, in_1, in_2, out, alpha, beta)
                new_box_paste,box_mean,box_beta,old = pasting_iteration(data, new_box_peel, in_1, in_2, out, alpha, beta)
                println(x)
                x += 1
                
            end
        final_box=new_box_paste
        end
    else
        #final_box = new_box_paste
        #print(final_box)
    end
    return final_box
end

prim_out=prim_iteration(data,1,8,9,0.08,0.08)

#prim_peel,box_mean,box_beta,old_box=peeling_iteration(data,1,8,9,0.08,0.08);
#prim_paste,box_mean,box_beta,old=pasting_iteration(data,prim_peel,1,8,9,0.08,0.08);