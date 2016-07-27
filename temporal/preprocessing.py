import numpy as np, copy

def leftShift(tup, n):
    if not tup or not n:
        return tup
    n %= len(tup)
    return tup[n:] + tup[:n]

def rightShift(tup, n):
    return leftShift(tup,len(tup)-n)
    



def pad_sequence_list(sequence_collection, pad_length,axis=0):
    padded_sequence_collection=[None]*len(sequence_collection)
    for i,seq in enumerate(sequence_collection):
        len_diff=pad_length-len(seq)
        new_seq=np.pad(seq, rightShift(((0,len_diff),)+tuple([(0,0)]*(seq.ndim-1)),axis), mode='constant', constant_values=0)
        padded_sequence_collection[i]=new_seq
    return padded_sequence_collection

def depad_sequence_list(sequence_collection, sequence_lengths, pad_length,axis=0):
    depadded_sequence_collection=[None]*len(sequence_collection)
    
    for i,seq in enumerate(sequence_collection):
        len_diff=pad_length-seq.shape[0]
        
        start=0
        end=start+sequence_lengths[i]
        
        new_seq=np.take(seq, np.arange(start,end), axis=axis)
        depadded_sequence_collection[i]=new_seq
    return depadded_sequence_collection


def pad_sequences_tensor(sequence_tensor, sequence_lengths, pad_length=None, axis=0):
    
    if pad_length is None:
        pad_length=max(sequence_lengths)
        
    sequence_collection=split_sequence_tensor(sequence_tensor,sequence_lengths,axis)
    return np.concatenate(pad_sequence_list(sequence_collection, pad_length),axis)
    
def depad_sequences_tensor(sequence_tensor, sequence_lengths, pad_length=None, axis=0, reconcatenate=True):
    
    if pad_length is None:
        pad_length=max(sequence_lengths)

    sequence_collection=split_sequence_tensor(sequence_tensor,[pad_length]*len(sequence_lengths),axis)
        
    if reconcatenate:
        return np.concatenate(depad_sequence_list(sequence_collection, sequence_lengths, pad_length, axis),axis)
    else:
        return depad_sequence_list(sequence_collection, sequence_lengths, pad_length, axis)
        
def split_sequence_tensor(sequence_tensor, orig_sequence_lengths,axis=0):
    sequence_lengths=copy.copy(orig_sequence_lengths)
    sequence_lengths.insert(0, 0)
    
    sequence_list=[None]*len(orig_sequence_lengths)
    boundaries=np.cumsum(sequence_lengths)
    
    for idx,_ in enumerate(sequence_lengths):
        if(idx==len(sequence_lengths)-1):
            break
        start=boundaries[idx]
        end=boundaries[idx+1]
        
        sequence_list[idx] = np.take(sequence_tensor, np.arange(start,end), axis=axis)
        #sequence_list[idx]=sequence_tensor[start:end,:]
    return sequence_list
    

def test_split_sequence_tensor():
    seq_list=split_sequence_tensor(np.arange(0,30).reshape(10,3),[3,3,2,2])
    tmp=1

def test_pad_concatenated_sequences():
    sequence_lengths=[3,3,2,2]
    latent_dim=3
    
    padded_seq_list = pad_sequences_tensor(np.arange(0,30).reshape(10,latent_dim),sequence_lengths,axis=0)
    depadded_seq_list = depad_sequences_tensor(sequence_tensor=padded_seq_list, 
                                              sequence_lengths=sequence_lengths, 
                                              axis=0)

    padded_seq_list2 = pad_sequences_tensor(np.arange(0,30).reshape(10,latent_dim),sequence_lengths=sequence_lengths,pad_length=5,axis=0)
    depadded_seq_list2 = depad_sequences_tensor(padded_seq_list2, 
                                              sequence_lengths, 
                                              pad_length=5,
                                              axis=0)
    
    padded_seq_list3=pad_sequences_tensor(np.arange(0,90).reshape(10,3,3),sequence_lengths,pad_length=5,axis=0)
    
    depadded_seq_list3=depad_sequences_tensor(padded_seq_list3, sequence_lengths=sequence_lengths,pad_length=5,axis=0)
    #latent_sequences=np.reshape(padded_seq_list, 
                                #[np.asarray(sequence_lengths).shape[0],
                                 #max(sequence_lengths),
                                 #latent_dim])
    

    
    tmp=1


def tests():
    #test_split_sequence_tensor()
    #for i in range(1,6):
        #shifted_tuple=rightShift((1,2,3,4,5), i)
        #print(shifted_tuple)
    test_pad_concatenated_sequences()
#tests()

