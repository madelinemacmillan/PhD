function get_sorted_box_lims(boxes,box_init)
    #determine restricted dimensions in one or more boxes
    uncs = Set()
    for box in boxes
        us = determine_restricted_dims(box,box_init) ##DEFINED LATER
        uncs=vcat(uncs,us)
        uncs=unique(uncs)
    uncs=Array(uncs,shape(uncs)[1])

    box_lim=boxes[1]
    nbl=normalize(box_lim,box_init,uncs) ##DEFINED LATER
    box_size=nbl[:,2]-nbl[:,1]

    uncs=uncs[sortperm(box_size)]
    box_lims = [box for box in boxes]

    return box_lims, uncs

function make_box(x)
    types=



    