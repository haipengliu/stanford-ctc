import time
import numpy as np
from decoder_utils import load_data, load_nnet, decode, int_to_char,\
        collapse_seq, load_chars

if __name__ == '__main__':
    print 'Loading data'
    fnum = 1
    data_dict, alis, keys = load_data(fnum)
    print 'Loading neural net'
    rnn = load_nnet()

    data, labels = data_dict[keys[0]], np.array(alis[keys[0]],
            dtype=np.int32)

    hyp, hypScore, refScore = decode(data, labels, rnn, alpha=1.0, beta=0.0, beam=200, method='fast')

    chars = load_chars()
    if labels is not None:
        print '  labels:', collapse_seq(int_to_char(labels, chars))
    print ' top hyp:', collapse_seq(int_to_char(hyp, chars))
    print 'score:', hypScore
    #print 'ref score:', refScore
