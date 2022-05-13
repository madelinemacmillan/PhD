###PEELING!!!!!!!!

function prim_iteration(data, in_1, in_2, out, alpha, beta)
    x = 1

    new_box_peel = !
    new_box_paste = 0
    box_mean = 0
    box_beta = 0
    old = 0
    final_box = 0

    if new_box_peel != new_box_paste
        while new_box_peel != new_box_paste
            if x==1 
                new_box_peel,box_mean,box_beta,old = peeling_iteration(data, in_1, in_2, out, alpha, beta)
                new_box_paste,box_mean,box_beta,old = pasting_iteration(data,new_box_peel,in_1,in_2,out,alpha,beta)
                x+=1
                println(new_box_peel)
                println(new_box_paste)
            else
                new_box_peel,box_mean,box_beta,old = peeling_iteration(new_box_paste, in_1, in_2, out, alpha, beta)
                new_box_paste,box_mean,box_beta,old = pasting_iteration(data,new_box_peel,in_1,in_2,out,alpha,beta)
            end
        end
    else
        final_box = new_box_paste
    end
    return final_box
end

prim=prim_iteration(data,1,8,9,0.08,0.08)
