function get_sorted_box_lims(boxes,box_init)
    #determine restricted dimensions in one or more boxes
    uncs = Set()
    for box in boxes
        us = determine_restricted_dims(box,box_init) ##DEFINED LATER
        uncs=vcat(uncs,us)
        uncs=unique(uncs)
    uncs=Array(uncs,size(uncs)[1])

    box_lim=boxes[1]
    nbl=normalize(box_lim,box_init,uncs) ##DEFINED LATER
    box_size=nbl[:,2]-nbl[:,1]

    uncs=uncs[sortperm(box_size)]
    box_lims = [box for box in boxes]

    return box_lims, uncs

function make_box(x)
    types= [v[2],k,v[1] for k, v in fieldnames(typeof(x)] #NICK, line 75 in project platypus
    types=sort(types)

    ntypes=[(k, "object" if t == Bool else t) for (_,k,t) in types] #NICK, line 79 in projecy platypus

    box=zeros((2, ), ntypes) #nick, I don't know if this is right
    names=[]
    for x in fieldnames(typeof(x))
        names=push!(names,x)
    end
    names=tuple(names)

    for name in names
        dtype=fieldnames(typeof(x))





    