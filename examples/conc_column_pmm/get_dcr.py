import math
import intersection

def get_dcr(capacity_pts, point):
    # "capacity_pts" is a list of two lists, the first for the M values for 
    # the points on the capacity curve, the second for the P values. "point" is
    # the load point. This function returns the PM Vector DCR. 
    
    pt_count=len(capacity_pts[0]) # how many points are provided
    
    Muxy=math.sqrt(sum((point[i]**2 for i in range(2)))) # the biaxial moment
    
    if Muxy==0:
        # the point is on the y axis, so get the index of the corresponding
        # capacity point on the y axis, then return the ratio
        index=0 if point[2]<0 else pt_count-1
        return point[2]/capacity_pts[1][index]
    
    vert_angle=math.atan2(point[2], Muxy) # the angle of the load point above
    # the M-M plane
    
    # binary search for the two points defining the segment of the PM diagram
    # with which the load vector intersects
    lo=0
    hi=pt_count-1
    while hi>lo:
        mid=(hi+lo+1)//2
        if math.atan2(capacity_pts[1][mid], capacity_pts[0][mid])>vert_angle:
            hi=mid-1
        else:
            lo=mid
    
    #line 1
    A = (0,0)
    B = (Muxy, point[2])
    
    #line 2
    C = (capacity_pts[0][lo], capacity_pts[1][lo])
    D = (capacity_pts[0][lo+1], capacity_pts[1][lo+1])

    # since the upper and lower endpoints have already been handled, it is
    # guaranteed that "int_pt" will not be on the y-axis
    moment_capacity=intersection.intersection((A, B), (C, D))[0]
    print("actual and capacity moment",Muxy,moment_capacity)
    return Muxy/moment_capacity