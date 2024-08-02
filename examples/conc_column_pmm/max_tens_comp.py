import try_axis

def max_pn(col):
    steel_area=col.bar_area*(col.bars_x*2+col.bars_y*2-4)
    steel_force=steel_area*col.fy
    conc_force=(col.area-steel_area)*0.85*col.fc/1000
    return steel_force+conc_force

def min_pn(col):
    steel_area=col.bar_area*(col.bars_x*2+col.bars_y*2-4)
    return -steel_area*col.fy

def max_phi_pn(col):
    return try_axis.COMP_FACTOR*col.PHI_COMP*max_pn(col)

def min_phi_pn(col):
    return try_axis.PHI_FLEXURE*min_pn(col)