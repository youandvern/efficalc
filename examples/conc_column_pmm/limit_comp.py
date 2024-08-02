import try_axis
import get_error

def limit_comp(col, guess, target):
    output=try_axis.try_axis(col, guess[0], guess[1])
    
    tot=1 # keep record of calls to "try_axis"
    while output[3]>0.99*col.PHI_COMP*col.max_pn:
        # the current phi_pn (without the 0.8) is at or almost at its
        # maximum value, which means the column is probably in full
        # compression, which must be avoided or derivatives will be zero
        guess[1]/=2
        output=try_axis.try_axis(col, guess[0], guess[1])
        tot+=1
    error=get_error.get_error(output, target, col.load_span) # update the distance from 
    # the target point
    return (output, error, guess,tot)