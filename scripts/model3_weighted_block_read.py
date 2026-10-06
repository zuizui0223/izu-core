"""Read weighted-core columns in whole-row batches without truncation."""
import numpy as np
from scripts.model3_compressed_step import check_size
from scripts.model3_weighted_core_stream import exact_core


def read_columns(core,left,right,start,stop,*,budget):
    m=left.shape[0];k=core.shape[2]
    if (not isinstance(start,(int,np.integer)) or not isinstance(stop,(int,np.integer))
            or not 0<=start<stop<=right.shape[0]*k):
        raise ValueError('nonempty column interval within unfolding required')
    check_size(m*(stop-start),budget)
    block=np.empty((m,stop-start));cursor=start
    while cursor<stop:
        row,offset=divmod(cursor,k)
        if offset or stop-cursor<k:
            end=min(stop,(row+1)*k)
            piece=exact_core(core[:,:,offset:offset+end-cursor],left,right[row:row+1],budget=budget)
        else:
            rows=(stop-cursor)//k
            # Input request already bounds the complete block, including this piece.
            end=cursor+rows*k
            piece=exact_core(core,left,right[row:row+rows],budget=budget)
        block[:,cursor-start:end-start]=piece.reshape(m,-1)
        cursor=end
    return block
